from constants import Constants
import random


class Ant:
    def __init__(self):
        self.__size = Constants.MOVE_COUNT
        self.__path = []  # will store the nodes indices
        self.__path.append(self.__selectRandomSensor())  # place it randomly on a sensor, not an exit / energy level
        self.__fitness = 0  # is computed only after moving on the path
        self.__battery = Constants.DRONE_BATTERY

    def __selectRandomSensor(self):
        """
            the nodes are distributed as follows, where n = NODES_PER_SENSOR:
            nk: sensor = entry node
            [nk + 1, nk + ENERGY_LEVELS + 1]: energy levels
            nk + ENERGY_LEVELS + 2: exit node
        """
        randomValue = random.randint(0, Constants.SENSOR_COUNT - 1)
        return randomValue * Constants.NODES_PER_SENSOR

    def __getPossibleMoves(self, distanceTable):
        possibleMoves = []
        currentNodeIndex = self.__path[-1]
        neighbourDistances = distanceTable[currentNodeIndex]

        for nextNodeIndex in range(Constants.NODE_COUNT):  # len(neighbourDistance) = Constants.NODE_COUNT
            if nextNodeIndex != currentNodeIndex and neighbourDistances[nextNodeIndex] != Constants.INFINITY and\
                    nextNodeIndex not in self.__path and self.__battery >= neighbourDistances[nextNodeIndex]:
                possibleMoves.append(nextNodeIndex)
        return possibleMoves

    def __computeProbabilityOfChoosingNextNode(self, possibleMoves, alpha, beta, distanceTable, pheromoneTable):
        currentNodeIndex = self.__path[-1]
        nextNodeProbability = [0 for _ in range(Constants.NODE_COUNT)]

        for moveIndex in possibleMoves:
            distanceToNextNode = distanceTable[currentNodeIndex][moveIndex]
            pheromoneToNextNode = pheromoneTable[currentNodeIndex][moveIndex]
            probability = ((distanceToNextNode + 0.001) ** beta) * (pheromoneToNextNode ** alpha)
            nextNodeProbability[moveIndex] = probability

        return nextNodeProbability

    def __rouletteSelection(self, nextNodeProbability):
        probabilitySum = sum(nextNodeProbability)

        if probabilitySum == 0:
            return random.randint(0, len(nextNodeProbability) - 1)

        partialSums = [nextNodeProbability[0] / probabilitySum]
        for i in range(1, len(nextNodeProbability)):
            partialSums.append(partialSums[i - 1] + nextNodeProbability[i] / probabilitySum)

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

        nextNodeProbability = self.__computeProbabilityOfChoosingNextNode(possibleMoves, alpha, beta, distanceTable, pheromoneTable)
        if random.random() < q0:
            bestProbability = max(nextNodeProbability)
            selectedNode = nextNodeProbability.index(bestProbability)
        else:
            selectedNode = self.__rouletteSelection(nextNodeProbability)

        self.__battery -= distanceTable[self.__path[-1]][selectedNode]
        self.__path.append(selectedNode)

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
