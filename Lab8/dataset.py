import torch
import torch.nn as nn
import torch.optim as optim
import time
import os, random
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from PIL import Image
from torchvision.datasets.folder import pil_loader


def loadImageList(folderName):
    images = []
    classes = []
    for imageName in os.listdir(folderName):
        image = pil_loader(os.path.join(folderName, imageName))
        isHuman = 1
        if "non" in imageName:  # nonhuman
            isHuman = 0
        images.append(image.resize((224, 224)))
        classes.append(isHuman)
    return images, classes


class ImageClassifierDataset(Dataset):
    def __init__(self, imageList, imageClasses):
        self.__images = []
        self.__labels = []
        self.__classes = list(set(imageClasses))
        self.__classToLabel = {className: imageName for imageName, className in enumerate(self.__classes)}

        self.__imageSize = 224  # square image
        self.__transformations = transforms.Compose([
            transforms.Resize(self.__imageSize),
            transforms.CenterCrop(self.__imageSize),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        for image, imageClass in zip(imageList, imageClasses):
            self.__images.append(self.__transformations(image))
            self.__labels.append(self.__classToLabel[imageClass])

    def __getitem__(self, index):
        return self.__images[index], self.__labels[index]

    def __len__(self):
        return len(self.__images)


trainSetImages, trainSetClasses = loadImageList("images/train")
trainSet = ImageClassifierDataset(trainSetImages, trainSetClasses)
testSetImages, testSetClasses = loadImageList("images/test")
testSet = ImageClassifierDataset(testSetImages, testSetClasses)