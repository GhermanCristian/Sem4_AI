import torch
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import DataLoader
import torch.nn as nn
from dataset import ImageClassifierDataset
from simpleNet import SimpleNet


def getTrainLoader():
    trainSetImages, trainSetClasses = ImageClassifierDataset.loadImageList("images/train")
    # transformations ?
    trainSet = ImageClassifierDataset(trainSetImages, trainSetClasses)
    return DataLoader(trainSet, batch_size=8, shuffle=False, num_workers=4)


def getTestLoader():
    testSetImages, testSetClasses = ImageClassifierDataset.loadImageList("images/test")
    testSet = ImageClassifierDataset(testSetImages, testSetClasses)
    return DataLoader(testSet, batch_size=8, shuffle=False, num_workers=4)


def adjustLearningRate(epoch, optimizer):
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

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def save_models(epoch, model):
    torch.save(model.state_dict(), "myModel_{}.model".format(epoch))
    print("Checkpoint saved")


def test(model, testLoader, isCudaAvailable):
    model.eval()
    testAccuracy = 0.0
    for i, (images, labels) in enumerate(testLoader):
        if isCudaAvailable:
            images = images.cuda()
            labels = labels.cuda()

        # Predict classes using images from the test set
        outputs = model(images)
        _, prediction = torch.max(outputs.data, 1)

        testAccuracy += torch.sum(torch.eq(prediction, labels.data))

    # Compute the average acc and loss over all 75 test images
    testAccuracy = testAccuracy / 75

    return testAccuracy


def train(epochCount, model, optimizer, testLoader, trainLoader, lossFunction, isCudaAvailable):
    bestAccuracy = 0.0

    for epoch in range(epochCount):
        model.train()
        trainAccuracy = 0.0
        trainLoss = 0.0
        for i, (images, labels) in enumerate(trainLoader):
            # Move images and labels to gpu if available
            if isCudaAvailable:
                images = Variable(images.cuda())
                labels = Variable(labels.cuda())

            # Clear all accumulated gradients
            optimizer.zero_grad()
            # Predict classes using images from the test set
            outputs = model(images)
            # Compute the loss based on the predictions and actual labels
            loss = lossFunction(outputs, labels)
            # Backpropagation of the loss
            loss.backward()

            # Adjust parameters according to the computed gradients
            optimizer.step()

            trainLoss += loss.cpu().data.item() * images.size(0)
            _, prediction = torch.max(outputs.data, 1)

            trainAccuracy += torch.sum(prediction == labels.data)

        # Call the learning rate adjustment function
        adjustLearningRate(epoch, optimizer)

        # Compute the average acc and loss over all 75 training images
        trainAccuracy = trainAccuracy / 75
        trainLoss = trainLoss / 75

        # Evaluate on the test set
        testAccuracy = test(model, testLoader, isCudaAvailable)

        # Save the model if the test acc is greater than our current best
        if testAccuracy > bestAccuracy:
            save_models(epoch, model)
            bestAccuracy = testAccuracy

        # Print the metrics
        print("Epoch {}, Train Accuracy: {} , TrainLoss: {} , Test Accuracy: {}".format(epoch, trainAccuracy, trainLoss, testAccuracy))


def runProgram():
    torch.cuda.empty_cache()
    trainLoader = getTrainLoader()
    testLoader = getTestLoader()
    model = SimpleNet(2)
    lossFunction = nn.CrossEntropyLoss()
    isCudaAvailable = torch.cuda.is_available()
    #isCudaAvailable = False
    if isCudaAvailable:
        model.cuda()
    optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
    train(10, model, optimizer, testLoader, trainLoader, lossFunction, isCudaAvailable)

