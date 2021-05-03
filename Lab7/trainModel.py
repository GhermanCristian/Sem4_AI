import torch
from netModel import Net
from constants import Constants
import matplotlib.pyplot as plt


class TrainModel:
    def __init__(self):
        self.__lossFunction = torch.nn.MSELoss()
        self.__neuralNetwork = Net(Constants.INPUT_LAYER_SIZE, Constants.HIDDEN_LAYER_SIZE, Constants.HIDDEN_LAYER_SIZE, Constants.OUTPUT_LAYER_SIZE).double()
        self.__optimizerBatch = torch.optim.SGD(self.__neuralNetwork.parameters(), lr=Constants.LEARNING_RATE)
        pairedTensor = torch.load(Constants.DATASET_FILE_NAME)
        self.__inputTensor = pairedTensor.narrow(1, 0, 2)  # just the first 2 columns
        self.__outputTensor = pairedTensor.narrow(1, 2, 1)  # just the last column

    def train(self):
        averageLossList = []
        batchCount = Constants.DATA_SIZE // Constants.BATCH_SIZE
        splitInputData = torch.split(self.__inputTensor, Constants.BATCH_SIZE)
        splitOutputData = torch.split(self.__outputTensor, Constants.BATCH_SIZE)

        for epoch in range(Constants.EPOCH_COUNT):
            lossSum = 0
            for batchIndex in range(batchCount):
                prediction = self.__neuralNetwork(splitInputData[batchIndex].double())
                loss = self.__lossFunction(prediction, splitOutputData[batchIndex])
                lossSum += loss.item()
                self.__optimizerBatch.zero_grad()
                loss.backward()
                self.__optimizerBatch.step()
            averageLossList.append(lossSum / batchCount)

            if epoch % 100 == 99:
                y_pred = self.__neuralNetwork(self.__inputTensor.double())
                loss = self.__lossFunction(y_pred, self.__outputTensor)
                print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

        plt.plot(averageLossList)
        plt.savefig("averageLoss.png")

    def saveToFile(self):
        # this should be called after train()
        torch.save(self.__neuralNetwork.state_dict(), Constants.NEURAL_NETWORK_FILE_NAME)
