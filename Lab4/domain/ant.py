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

    def __computeSensorEnergyPairs(self):
        # path is of the form: entry node, energy node, exit node...
        sensorEnergyPairs = []
        for i in range(0, len(self.__path), 3):
            sensorEnergyPairs.append((self.__path[i], self.__path[i + 1] - self.__path[i] - 1))
        return sensorEnergyPairs

    def __checkEmptyAndUpdateAccessibleCount(self, crtCoords, temporaryMatrix):
        if temporaryMatrix[crtCoords[0]][crtCoords[1]] == Constants.ACCESSIBLE_POSITION:
            return 0
        temporaryMatrix[crtCoords[0]][crtCoords[1]] = Constants.ACCESSIBLE_POSITION
        return 1

    def __markAndCountNewAccessible(self, temporaryMatrix, crtCoords, energy):
        newAccessible = 0

        newX = crtCoords[0] - 1  # UP
        energyCopy = energy
        while energyCopy > 0 and newX >= 0 and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX -= 1
            energyCopy -= 1

        newY = crtCoords[1] + 1  # RIGHT
        energyCopy = energy
        while energyCopy > 0 and newY < Constants.MAP_WIDTH and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY += 1
            energyCopy -= 1

        newX = crtCoords[0] + 1  # DOWN
        energyCopy = energy
        while energyCopy > 0 and newX < Constants.MAP_HEIGHT and temporaryMatrix[newX][crtCoords[1]] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((newX, crtCoords[1]), temporaryMatrix)
            newX += 1
            energyCopy -= 1

        newY = crtCoords[1] - 1  # LEFT
        energyCopy = energy
        while energyCopy > 0 and newY >= 0 and temporaryMatrix[crtCoords[0]][newY] != Constants.WALL_POSITION:
            newAccessible += self.__checkEmptyAndUpdateAccessibleCount((crtCoords[0], newY), temporaryMatrix)
            newY -= 1
            energyCopy -= 1

        return newAccessible

    def computeFitness(self, mapSurface, nodeList):
        mapCopy = mapSurface.copy()
        sensorEnergyPairs = self.__computeSensorEnergyPairs()
        self.__fitness = 0
        for pair in sensorEnergyPairs:
            sensorIndex, energy = pair
            sensor = nodeList[sensorIndex]
            res = self.__markAndCountNewAccessible(mapCopy, (sensor.getX(), sensor.getY()), energy)
            self.__fitness += res

        self.__fitness = Constants.TOTAL_EMPTY_POSITIONS - self.__fitness  # fitness is inverse proportional with the no. of visible tiles

    def getFitness(self):
        return self.__fitness

    def getVisiblePositions(self):
        return Constants.TOTAL_EMPTY_POSITIONS - self.__fitness

    def getPath(self):
        return self.__path

    def getBattery(self):
        return self.__battery
