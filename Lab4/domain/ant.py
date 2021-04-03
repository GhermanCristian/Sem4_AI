from constants import Constants
import random


class Ant:
    def __init__(self):
        self.__size = Constants.SENSOR_COUNT  # size of the path through all the sensors
        self.__path = []  # will store the sensor indices
        self.__path.append(random.randint(0, Constants.SENSOR_COUNT - 1))  # place it randomly on a sensor

    def __getPossibleMoves(self):
        possibleMoves = []
        for sensorIndex in range(Constants.SENSOR_COUNT):
            if sensorIndex not in self.__path:
                possibleMoves.append(sensorIndex)
        return possibleMoves

    def __computeProbabilityOfChoosingNextSensor(self, possibleMoves, alpha, beta, distanceTable, pheromoneTable):
        currentSensorIndex = self.__path[-1]
        nextSensorProbability = [0 for i in range(self.__size)]

        for moveIndex in range(len(possibleMoves)):
            distanceToNextSensor = distanceTable[currentSensorIndex][moveIndex]
            pheromoneToNextSensor = pheromoneTable[currentSensorIndex][moveIndex]
            probability = (distanceToNextSensor ** beta) * (pheromoneToNextSensor ** alpha)
            nextSensorProbability.append(probability)

        return nextSensorProbability

    def nextMove(self, distanceTable, pheromoneTable, q0, alpha, beta):
        # q0 = probability that the ant chooses the best possible move; otherwise, all moves have a prob of being chosen
        possibleMoves = self.__getPossibleMoves()
        if not possibleMoves:
            return False

        nextSensorProbability = self.__computeProbabilityOfChoosingNextSensor(possibleMoves, alpha, beta, distanceTable, pheromoneTable)
        if random.random() < q0:
            bestProbability = max(nextSensorProbability)
            self.__path.append(nextSensorProbability.index(bestProbability))
        else:
            # all moves have a prob of being chosen (roulettte)
            # TO-DO
            pass

    def fitness(self, distanceTable, maxPossiblePathDistance):
        distance = 0
        for i in range(1, len(self.__path)):
            distance += distanceTable[self.__path[i - 1]][self.__path[i]]
        return maxPossiblePathDistance - distance

    def getPath(self):
        return self.__path
