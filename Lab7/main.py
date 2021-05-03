from netModel import Net
import torch
from constants import Constants
from trainModel import TrainModel


def main():
    #x = TrainModel()
    #x.train()
    #x.saveToFile()

    neuralNetwork = Net(Constants.INPUT_LAYER_SIZE, Constants.HIDDEN_LAYER_SIZE, Constants.OUTPUT_LAYER_SIZE)
    neuralNetwork.load_state_dict(torch.load(Constants.NEURAL_NETWORK_FILE_NAME))
    neuralNetwork.eval()

    inputTensor = torch.tensor([5.0, 6.0])
    print(neuralNetwork(inputTensor))


if __name__ == "__main__":
    main()
