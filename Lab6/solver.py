import random
import math


class Solver:
    CLUSTER_COUNT = 4

    def __init__(self):
        self.__pointList = []  # a point is of the form [xCoord, yCoord, currentLabel, centroidIndex]
        self.__centroids = []  # only the coordinates

    def __parseLineAndAddToList(self, line):
        splitData = line.split(",")
        self.__pointList.append([float(splitData[1]), float(splitData[2]), splitData[0], None])

    def __parseDataset(self):
        fileDesc = open("dataset.csv", "r")
        fileDesc.readline()  # skip the first line (header)
        for line in fileDesc:
            self.__parseLineAndAddToList(line[:-1])  # remove the trailing '\n'

    def __generateInitialCentroids(self):
        for _ in range(Solver.CLUSTER_COUNT):
            self.__centroids.append([random.uniform(-9.99, 9.99), random.uniform(-9.99, 9.99)])

    def __computeEuclidianDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def __getClosestCentroidIndex(self, currentPoint):
        minDistance = 20
        closestCentroid = None
        for centroid in self.__centroids:
            currentDistance = self.__computeEuclidianDistance(currentPoint, centroid)
            if currentDistance < minDistance:
                minDistance = currentDistance
                closestCentroid = centroid
        return self.__centroids.index(closestCentroid)

    def __clusterDataAroundCentroids(self):
        for point in self.__pointList:
            point[3] = self.__getClosestCentroidIndex(point)

    def __recomputeCentroids(self):
        # for each centroid we want to compute the average of the coordinates of the points in its cluster
        # so we store the coord sum and count => avg = sum / count
        coordSum = [[0, 0] for _ in range(Solver.CLUSTER_COUNT)]
        count = [0 for _ in range(Solver.CLUSTER_COUNT)]
        for point in self.__pointList:
            centroidIndex = point[3]
            coordSum[centroidIndex][0] += point[0]
            coordSum[centroidIndex][1] += point[1]
            count[centroidIndex] += 1

        hasChanged = False
        for centroidIndex in range(Solver.CLUSTER_COUNT):
            if count[centroidIndex] == 0:
                continue
            if self.__centroids[centroidIndex][0] != coordSum[centroidIndex][0] / count[centroidIndex]:
                self.__centroids[centroidIndex][0] = coordSum[centroidIndex][0] / count[centroidIndex]
                hasChanged = True
            if self.__centroids[centroidIndex][1] != coordSum[centroidIndex][1] / count[centroidIndex]:
                self.__centroids[centroidIndex][1] = coordSum[centroidIndex][1] / count[centroidIndex]
                hasChanged = True

        return hasChanged

    def __doOneIteration(self):
        # cluster the data around the centroids
        # recompute the centroids as the means of their clusters
        self.__clusterDataAroundCentroids()
        hasChanged = self.__recomputeCentroids()
        if not hasChanged:
            return False
        clusterSize = [0 for _ in range(Solver.CLUSTER_COUNT)]
        for point in self.__pointList:
            clusterSize[point[3]] += 1
        return True

    def solve(self):
        self.__parseDataset()
        self.__generateInitialCentroids()
        for _ in range(20):
            if not self.__doOneIteration():  # no changes in this iteration
                break
