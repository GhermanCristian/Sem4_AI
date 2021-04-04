from constants import Constants
import random


class Ant:
    def __init__(self):
        self.__size = Constants.SENSOR_COUNT  # size of the path through all the sensors
        self.__path = []  # will store the sensor indices
        self.__path.append(random.randint(0, Constants.SENSOR_COUNT - 1))  # place it randomly on a sensor
        self.__fitness = 0  # is computed only after moving on the path
        self.__battery = Constants.DRONE_BATTERY

    def __getPossibleMoves(self, distanceTable):
        possibleMoves = []
        currentSensorIndex = self.__path[-1]

        for nextSensorIndex in range(Constants.SENSOR_COUNT):
            if nextSensorIndex not in self.__path and self.__battery >= distanceTable[currentSensorIndex][nextSensorIndex]:
                possibleMoves.append(nextSensorIndex)
        return possibleMoves

    def __computeProbabilityOfChoosingNextSensor(self, possibleMoves, alpha, beta, distanceTable, pheromoneTable):
        currentSensorIndex = self.__path[-1]
        nextSensorProbability = [0 for i in range(self.__size)]

        for moveIndex in possibleMoves:
            distanceToNextSensor = distanceTable[currentSensorIndex][moveIndex]
            pheromoneToNextSensor = pheromoneTable[currentSensorIndex][moveIndex]
            probability = (distanceToNextSensor ** beta) * (pheromoneToNextSensor ** alpha)
            nextSensorProbability[moveIndex] = probability

        return nextSensorProbability

    def __rouletteSelection(self, nextSensorProbability):
        probabilitySum = sum(nextSensorProbability)
        partialSums = [nextSensorProbability[0] / probabilitySum]
        for i in range(1, len(nextSensorProbability)):
            partialSums.append(partialSums[i - 1] + nextSensorProbability[i] / probabilitySum)

        r = random.random()
        position = 0
        while r > partialSums[position]:
            position += 1
        return position

    def nextMove(self, distanceTable, pheromoneTable, q0, alpha, beta):
        # q0 = probability that the ant chooses the best possible move; otherwise, all moves have a prob of being chosen
        possibleMoves = self.__getPossibleMoves(distanceTable)
        if not possibleMoves:
            return False  # the move wasn't completed successfully

        nextSensorProbability = self.__computeProbabilityOfChoosingNextSensor(possibleMoves, alpha, beta, distanceTable, pheromoneTable)
        if random.random() < q0:
            bestProbability = max(nextSensorProbability)
            selectedSensor = nextSensorProbability.index(bestProbability)
        else:
            selectedSensor = self.__rouletteSelection(nextSensorProbability)
        self.__battery -= distanceTable[self.__path[-1]][selectedSensor]
        self.__path.append(selectedSensor)

        return True  # the move was completed successfully

    def computePathLength(self, distanceTable):
        length = 0
        for i in range(1, len(self.__path)):
            length += distanceTable[self.__path[i - 1]][self.__path[i]]
        return length

    def computeFitness(self, distanceTable):
        self.__fitness = self.computePathLength(distanceTable)

    def getFitness(self):
        return self.__fitness

    def getPath(self):
        return self.__path
