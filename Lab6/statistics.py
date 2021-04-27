from constants import Constants


class Statistics:
    def __init__(self, pointList):
        self.__pointList = pointList

    def __findOccurrencesInEachCluster(self, trueLabel):
        occurrences = [0 for _ in range(Constants.CLUSTER_COUNT)]
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
        confusionMatrix = [[0 for _ in range(Constants.CLUSTER_COUNT)] for _ in range(Constants.CLUSTER_COUNT)]
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
        for i in range(Constants.CLUSTER_COUNT):
            for j in range(Constants.CLUSTER_COUNT):
                if i != labelIndex and j != labelIndex:
                    trueNegative += confusionMatrix[i][j]
                elif i == labelIndex and j != labelIndex:
                    falsePositive += confusionMatrix[i][j]
                elif i != labelIndex and j == labelIndex:
                    falseNegative += confusionMatrix[i][j]

        return truePositive, trueNegative, falsePositive, falseNegative

    def computeMeasurements(self):
        confusionMatrix = self.__computeConfusionMatrix()
        results = []  # rows: 0 = accuracy, 1 = precision, 2 = rappel, 3 = score
        for labelIndex in range(Constants.CLUSTER_COUNT):
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
        print("Average accuracy: ", (sum(row[0] for row in results)) / Constants.CLUSTER_COUNT)
        print("Average precision: ", (sum(row[1] for row in results)) / Constants.CLUSTER_COUNT)
        print("Average rappel: ", (sum(row[2] for row in results)) / Constants.CLUSTER_COUNT)
        print("Average score: ", (sum(row[3] for row in results)) / Constants.CLUSTER_COUNT)
        print(confusionMatrix)