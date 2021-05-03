from netModel import Net
import torch
from constants import Constants
from trainModel import TrainModel


def runExamples(neuralNetwork):
    inputTensorList = [
        torch.tensor([5.0, 6.0]),  # 0.5864
        torch.tensor([0.0, 0.0]),  # 0
        torch.tensor([-1.0, 1.0]),  # -0.6301
        torch.tensor([3.0, -1.0]),  # 0.4438
        torch.tensor([5.0, 0.0]),  # −0.9589
        torch.tensor([0.0, 1.0]),  # 0.3129
        torch.tensor([1, 3.1415926]),  # 0.9092
        torch.tensor([0, -6.0]),  # −0.9430
        torch.tensor([0, -3.1415926])  # −0.8414
    ]
    for inputTensor in inputTensorList:
        print(neuralNetwork(inputTensor).item())


def main():
    x = TrainModel()
    x.train()
    x.saveToFile()

    neuralNetwork = Net(Constants.INPUT_LAYER_SIZE, Constants.HIDDEN_LAYER_SIZE, Constants.HIDDEN_LAYER_SIZE, Constants.OUTPUT_LAYER_SIZE)
    neuralNetwork.load_state_dict(torch.load(Constants.NEURAL_NETWORK_FILE_NAME))
    neuralNetwork.eval()

    runExamples(neuralNetwork)


if __name__ == "__main__":
    main()
