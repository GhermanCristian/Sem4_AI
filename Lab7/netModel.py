import torch
import torch.nn.functional as F


class Net(torch.nn.Module):
    def __init__(self, inputLayerSize, hiddenLayer1Size, hiddenLayer2Size, outputLayerSize):
        super(Net, self).__init__()
        self.hiddenLayer1 = torch.nn.Linear(inputLayerSize, hiddenLayer1Size)
        self.hiddenLayer2 = torch.nn.Linear(hiddenLayer1Size, hiddenLayer2Size)
        self.output = torch.nn.Linear(hiddenLayer2Size, outputLayerSize)

    def forward(self, inputData):
        hiddenLayer1Output = F.relu(self.hiddenLayer1(inputData))
        hiddenLayer2Output = F.relu(self.hiddenLayer2(hiddenLayer1Output))
        finalOutput = self.output(hiddenLayer2Output)
        return finalOutput
