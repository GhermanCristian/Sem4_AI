import torch
from netModel import Net
from constants import Constants


class TrainModel:
    def __init__(self):
        self.__lossFunction = torch.nn.MSELoss()
        self.__neuralNetwork = Net(2, 10, 1).double()
        self.__optimizerBatch = torch.optim.SGD(self.__neuralNetwork.parameters(), lr=0.02)
        pairedTensor = torch.load(Constants.DATASET_FILE_NAME)
        self.__inputTensor = pairedTensor.narrow(1, 0, 2)
        self.__outputTensor = pairedTensor.narrow(1, 2, 1)

    def train(self):
        lossList = []
        averageLossList = []
        batchCount = Constants.DATA_SIZE // Constants.BATCH_SIZE
        splitInputData = torch.split(self.__inputTensor, Constants.BATCH_SIZE)
        splitOutputData = torch.split(self.__outputTensor, Constants.BATCH_SIZE)

        for epoch in range(Constants.EPOCH_COUNT):
            for batchIndex in range(batchCount):
                prediction = self.__neuralNetwork(splitInputData[batchIndex].double())
                loss = self.__lossFunction(prediction, splitOutputData[batchIndex])
                lossList.append(loss)
                self.__optimizerBatch.zero_grad()
                loss.backward()
                self.__optimizerBatch.step()

            if epoch % 20 == 19:
                y_pred = self.__neuralNetwork(self.__inputTensor.double())
                loss = self.__lossFunction(y_pred, self.__outputTensor)
                print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    def saveToFile(self):
        #  this should be called after train()
        torch.save(self.__neuralNetwork.state_dict(), Constants.NEURAL_NETWORK_FILE_NAME)
