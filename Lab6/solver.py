import random


class Solver:
    CLUSTER_COUNT = 4

    def __init__(self):
        self.__pointList = []  # a point is of the form (label, val1, val2)
        self.__centroids = []

    def __parseLineAndAddToList(self, line):
        splitData = line.split(",")
        self.__pointList.append((splitData[0], float(splitData[1]), float(splitData[2])))

    def __parseDataset(self):
        fileDesc = open("dataset.csv", "r")
        fileDesc.readline()  # skip the first line (header)
        for line in fileDesc:
            self.__parseLineAndAddToList(line[:-1])  # remove the trailing '\n'

    def __generateInitialCentroids(self):
        for _ in range(Solver.CLUSTER_COUNT):
            self.__centroids.append((random.uniform(-9.99, 9.99), random.uniform(-9.99, 9.99)))

    def solve(self):
        self.__parseDataset()
        self.__generateInitialCentroids()

