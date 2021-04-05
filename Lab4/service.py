from domain.ant import Ant
from domain.drone import Drone
from domain.map import Map
from constants import Constants
import random
from nodeList import NodeList


class Service:
    def __init__(self):
        self.__map = Map()
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__drone = Drone(5, 5)
        self.__nodeList = NodeList(self.__map)
        self.__placeDroneOnEmptyPosition()
        self.__pheromoneTable = [[1.0 for _ in range(Constants.NODE_COUNT)] for _ in range(Constants.NODE_COUNT)]
        self.__distanceTable = self.__nodeList.getDistanceBetweenNodes()

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone.getX(), self.__drone.getY()
        while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
            crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
        self.__drone.setX(crtX)
        self.__drone.setY(crtY)

    def __selectBestAnt(self, ants):
        bestAnt = None
        bestFitness = 0
        for ant in ants:
            if bestFitness < ant.getFitness():
                bestFitness = ant.getFitness()
                bestAnt = ant
        return bestAnt

    def __simulateEpoch(self, antCount, alpha, beta, q0, rho):
        ants = [Ant() for _ in range(antCount)]

        # move the ants; remove those which don't reach the end
        for ant in ants:
            for step in range(Constants.MOVE_COUNT - 1):  # subtract 1 because we init the ant by placing it on a node, so 1 node is already taken?
                ant.nextMove(self.__distanceTable, self.__pheromoneTable, q0, alpha, beta)
            ant.computeFitness(self.__mapSurface, self.__nodeList.getNodeList())

        # simulate pheromone evaporation; it has to be done even if all ants die
        for i in range(Constants.NODE_COUNT):
            for j in range(Constants.NODE_COUNT):
                self.__pheromoneTable[i][j] *= (1 - rho)

        # add the pheromones produced by the last batch of ants
        for ant in ants:
            newPheromone = 1.0 / ant.getFitness()
            currentPath = ant.getPath()
            for i in range(len(currentPath) - 1):
                crtNode = currentPath[i]
                nextNode = currentPath[i + 1]
                self.__pheromoneTable[crtNode][nextNode] += newPheromone

        return self.__selectBestAnt(ants)

    def __updateBestSolution(self, bestSolution):
        currentSolution = self.__simulateEpoch(Constants.ANT_COUNT, Constants.ALPHA, Constants.BETA, Constants.Q0, Constants.RHO)
        if currentSolution is None:
            return bestSolution

        currentSolutionPathLength = len(currentSolution.getPath())
        if bestSolution is None or currentSolutionPathLength > len(bestSolution.getPath()) or (currentSolutionPathLength == len(bestSolution.getPath()) and currentSolution.getFitness() < bestSolution.getFitness()):
            return currentSolution  # new best solution
        return bestSolution

    def getSolutionFromPath(self, path):
        # path is of the form: entry node, energy node, exit node...
        sensorEnergyPairs = []
        for i in range(0, len(path), 3):
            sensor = self.__nodeList.getNodeList()[path[i]]
            sensorEnergyPairs.append(((sensor.getX(), sensor.getY()), path[i + 1] - path[i] - 1))
        return sensorEnergyPairs

    def run(self):
        bestSolution = None  # will be the one with the largest number of visible positions
        for epoch in range(Constants.EPOCH_COUNT):
            bestSolution = self.__updateBestSolution(bestSolution)
        return bestSolution

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getNodeList(self):
        return self.__nodeList.getNodeList()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
