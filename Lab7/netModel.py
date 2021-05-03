import torch
import torch.nn.functional as F


class Net(torch.nn.Module):
    def __init__(self, inputLayerSize, hiddenLayer1Size, outputLayerSize):
        super(Net, self).__init__()
        self.hiddenLayer1 = torch.nn.Linear(inputLayerSize, hiddenLayer1Size)
        self.output = torch.nn.Linear(hiddenLayer1Size, outputLayerSize)

    def forward(self, inputData):
        firstHiddenLayerOutput = F.relu(self.hiddenLayer1(inputData))
        finalOutput = self.output(firstHiddenLayerOutput)
        return finalOutput
