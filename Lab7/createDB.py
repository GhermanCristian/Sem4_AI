import torch
from constants import Constants
import numpy as np


class CreateDB:
    def __computeFunctionValues(self, tensor):
        valuesAsList = []
        for pair in tensor.numpy():  # pair is of the form (x1, x2)
            valuesAsList.append(np.sin((pair[0] + pair[1] / np.pi)))
        return torch.tensor(valuesAsList)

    def __generateInput(self):
        return (Constants.MAX_VALUE - Constants.MIN_VALUE) * torch.rand(Constants.DATA_SIZE, 2) + Constants.MIN_VALUE

    def __createTensor(self):
        inputTensor = self.__generateInput()
        outputTensor = self.__computeFunctionValues(inputTensor)
        pairedTensor = torch.column_stack((inputTensor, outputTensor))
        return pairedTensor

    def saveToFile(self):
        torch.save(self.__createTensor(), 'dataset.pt')
