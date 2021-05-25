import torch
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import DataLoader
import torch.nn as nn
from torchvision.transforms import transforms
from constants import Constants
from dataset import ImageClassifierDataset
from simpleNet import SimpleNet


class Train:
    def __init__(self):
        self.__trainLoader = self.__getTrainLoader()
        self.__testLoader = self.__getTestLoader()
        self.__model = SimpleNet(2)
        # self.__isCudaAvailable = torch.cuda.is_available()
        self.__isCudaAvailable = False
        if self.__isCudaAvailable:
            self.__model.cuda()
        self.__optimizer = Adam(self.__model.parameters(), lr=0.001, weight_decay=0.0001)
        self.__lossFunction = nn.CrossEntropyLoss()

    def __getTrainLoader(self):
        trainSetImages, trainSetClasses = ImageClassifierDataset.loadImageList("images/train")
        trainTransformations = transforms.Compose([
            transforms.Resize((Constants.IMAGE_SIZE, Constants.IMAGE_SIZE)),
            transforms.RandomHorizontalFlip(),
            # transforms.RandomCrop(32, padding=4),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        trainSet = ImageClassifierDataset(trainSetImages, trainSetClasses, trainTransformations)
        return DataLoader(trainSet, batch_size=Constants.BATCH_SIZE, shuffle=True, num_workers=4)

    def __getTestLoader(self):
        testSetImages, testSetClasses = ImageClassifierDataset.loadImageList("images/test")
        testTransformations = transforms.Compose([
            transforms.Resize((Constants.IMAGE_SIZE, Constants.IMAGE_SIZE)),
            transforms.CenterCrop(Constants.IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        testSet = ImageClassifierDataset(testSetImages, testSetClasses, testTransformations)
        return DataLoader(testSet, batch_size=Constants.BATCH_SIZE, shuffle=False, num_workers=4)

    def __adjustLearningRate(self, epoch):
        lr = 0.001

        if epoch > 180:
            lr = lr / 1000000
        elif epoch > 150:
            lr = lr / 100000
        elif epoch > 120:
            lr = lr / 10000
        elif epoch > 90:
            lr = lr / 1000
        elif epoch > 60:
            lr = lr / 100
        elif epoch > 30:
            lr = lr / 10

        for param_group in self.__optimizer.param_groups:
            param_group["lr"] = lr

    def __save_models(self, epoch):
        torch.save(self.__model.state_dict(), "myModel_{}.model".format(epoch))
        print("Checkpoint saved")

    def __test(self):
        self.__model.eval()
        testAccuracy = 0.0
        for i, (images, labels) in enumerate(self.__testLoader):
            if self.__isCudaAvailable:
                images = images.cuda()
                labels = labels.cuda()

            outputs = self.__model(images)  # Predict classes using images from the test set
            _, prediction = torch.max(outputs.data, 1)

            testAccuracy += torch.sum(torch.eq(prediction, labels.data))

        testAccuracy = testAccuracy / 75  # 75 test images
        return testAccuracy

    def __train(self, epochCount):
        bestAccuracy = 0.0

        for epoch in range(epochCount):
            self.__model.train()
            trainAccuracy = 0.0
            trainLoss = 0.0
            for i, (images, labels) in enumerate(self.__trainLoader):
                if self.__isCudaAvailable:  # Move images and labels to gpu if available
                    images = Variable(images.cuda())
                    labels = Variable(labels.cuda())

                self.__optimizer.zero_grad()  # Clear all accumulated gradients
                outputs = self.__model(images)  # Predict classes using images from the test set
                loss = self.__lossFunction(outputs, labels)  # Compute the loss based on the predictions and actual labels
                loss.backward()  # Backpropagation of the loss
                self.__optimizer.step()  # Adjust parameters according to the computed gradients

                trainLoss += loss.cpu().data.item() * images.size(0)
                _, prediction = torch.max(outputs.data, 1)

                trainAccuracy += torch.sum(prediction == labels.data)

            self.__adjustLearningRate(epoch)

            trainAccuracy = trainAccuracy / 75  # 75 training images
            trainLoss = trainLoss / 75

            testAccuracy = self.__test()  # Evaluate on the test set
            if testAccuracy > bestAccuracy:  # Save the model if the test acc is greater than our current best
                self.__save_models(epoch)
                bestAccuracy = testAccuracy

            # Print the metrics
            print("Epoch {}, Train Accuracy: {} , TrainLoss: {} , Test Accuracy: {}".format(epoch, trainAccuracy, trainLoss, testAccuracy))

    def runProgram(self):
        torch.cuda.empty_cache()
        self.__train(Constants.EPOCH_COUNT)

