from constants import Constants
import random


class Ant:
    def __init__(self):
        self.__size = Constants.NODE_COUNT
        # self.__size = 3 * Constants.NODE_COUNT  # to get from one node to another: choose energy level, go to exit, go to next node (3 moves)
        self.__path = []  # will store the nodes indices
        self.__path.append(random.randint(0, Constants.NODE_COUNT - 1))  # place it randomly on a node!!! - ensure that we're placing on a node not on an energy level
        self.__fitness = 0  # is computed only after moving on the path
        self.__battery = Constants.DRONE_BATTERY

    def __getPossibleMoves(self, distanceTable):
        possibleMoves = []
        currentNodeIndex = self.__path[-1]

        for nextNodeIndex in range(Constants.NODE_COUNT):
            if nextNodeIndex not in self.__path and self.__battery >= distanceTable[currentNodeIndex][nextNodeIndex]:
                possibleMoves.append(nextNodeIndex)
        return possibleMoves

    def __computeProbabilityOfChoosingNextNode(self, possibleMoves, alpha, beta, distanceTable, pheromoneTable):
        currentNodeIndex = self.__path[-1]
        nextNodeProbability = [0 for i in range(self.__size)]

        for moveIndex in possibleMoves:
            distanceToNextNode = distanceTable[currentNodeIndex][moveIndex]
            pheromoneToNextNode = pheromoneTable[currentNodeIndex][moveIndex]
            probability = (distanceToNextNode ** beta) * (pheromoneToNextNode ** alpha)
            nextNodeProbability[moveIndex] = probability

        return nextNodeProbability

    def __rouletteSelection(self, nextNodeProbability):
        probabilitySum = sum(nextNodeProbability)
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
