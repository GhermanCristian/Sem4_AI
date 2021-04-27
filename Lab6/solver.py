import random
import math


class Solver:
    CLUSTER_COUNT = 4

    def __init__(self):
        self.__pointList = []  # a point is of the form [xCoord, yCoord, trueLabel, centroidIndex=predictedLabel]
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
        minDistance = 40
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
                # we don't want to end up with < 4 clusters, so when we get a cluster with 0 points, we just reposition the
                # centroid by default to (0, 0) and continue from there
                self.__centroids[centroidIndex][0] = self.__centroids[centroidIndex][1] = 0
                hasChanged = True
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

    def __findOccurrencesInEachCluster(self, trueLabel):
        occurrences = [0 for _ in range(Solver.CLUSTER_COUNT)]
        for point in self.__pointList:
            if point[2] == trueLabel:
                occurrences[point[3]] += 1
        return occurrences

    def __rearrangeClusters(self):
        labelToIndex = {"A": None, "B": None, "C": None, "D": None}

        for trueLabel in labelToIndex.keys():
            occurrences = self.__findOccurrencesInEachCluster(trueLabel)
            """
            if a label appears in a cluster that has already been assigned, try the next-best cluster;
            this usually happens when we have just 3 clusters (which technically should no longer happen), or when
            we have 3 large clusters and a very small one (and we have 2 labels who are in majority in the same cluster)
            """
            while occurrences.index(max(occurrences)) in labelToIndex.values():
                occurrences[occurrences.index(max(occurrences))] = -1  # basically mark it as removed
            labelToIndex[trueLabel] = occurrences.index(max(occurrences))

        return labelToIndex

    def __computeConfusionMatrix(self):
        confusionMatrix = [[0 for _ in range(Solver.CLUSTER_COUNT)] for _ in range(Solver.CLUSTER_COUNT)]
        labelToIndex = self.__rearrangeClusters()
        for point in self.__pointList:
            trueLabel = labelToIndex[point[2]]
            predictedLabel = point[3]
            confusionMatrix[predictedLabel][trueLabel] += 1

        return confusionMatrix

    def __computeMeasurementsSpecificLabel(self, labelIndex, confusionMatrix):
        """
        for each label, i = label's index:
            true positive = m[i][i]
            true negative = sum(m[j][k]), j, k != i -> the matrix without the current line and column
            false positive = sum(m[i][j]), j != i -> just the current row (without position [i][i])
            false negative = sum(m[j][i]), j != i -> just the current column (without position [i][i])
        """
        truePositive = confusionMatrix[labelIndex][labelIndex]

        trueNegative, falsePositive, falseNegative = 0, 0, 0
        for i in range(Solver.CLUSTER_COUNT):
            for j in range(Solver.CLUSTER_COUNT):
                if i != labelIndex and j != labelIndex:
                    trueNegative += confusionMatrix[i][j]
                elif i == labelIndex and j != labelIndex:
                    falsePositive += confusionMatrix[i][j]
                elif i != labelIndex and j == labelIndex:
                    falseNegative += confusionMatrix[i][j]

        return truePositive, trueNegative, falsePositive, falseNegative

    def __computeMeasurements(self):
        confusionMatrix = self.__computeConfusionMatrix()
        results = []  # rows: 0 = accuracy, 1 = precision, 2 = rappel, 3 = score
        for labelIndex in range(Solver.CLUSTER_COUNT):
            truePositive, trueNegative, falsePositive, falseNegative = self.__computeMeasurementsSpecificLabel(labelIndex, confusionMatrix)
            accuracy = (truePositive + trueNegative) / (truePositive + trueNegative + falsePositive + falseNegative)
            precision = truePositive / (truePositive + falsePositive)
            rappel = truePositive / (truePositive + falseNegative)
            score = 2 * precision * rappel / (precision + rappel)
            results.append((accuracy, precision, rappel, score))
            print("===================")
            print("Accuracy: ", accuracy)
            print("Precision: ", precision)
            print("Rappel: ", rappel)
            print("Score: ", score)

        print("===================")
        print("Average accuracy: ", (sum(row[0] for row in results)) / Solver.CLUSTER_COUNT)
        print("Average precision: ", (sum(row[1] for row in results)) / Solver.CLUSTER_COUNT)
        print("Average rappel: ", (sum(row[2] for row in results)) / Solver.CLUSTER_COUNT)
        print("Average score: ", (sum(row[3] for row in results)) / Solver.CLUSTER_COUNT)
        print(confusionMatrix)

    def solve(self):
        self.__parseDataset()
        self.__generateInitialCentroids()
        while self.__doOneIteration():
            pass
        self.__computeMeasurements()
