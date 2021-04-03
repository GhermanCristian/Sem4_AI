from domain.ant import Ant
from domain.drone import Drone
from domain.map import Map
from constants import Constants
import random
from sensorList import SensorList


class Service:
    def __init__(self):
        self.__map = Map()
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__drone = Drone(5, 5)
        self.__sensorList = SensorList(self.__map)
        self.__placeDroneOnEmptyPosition()
        self.__pheromoneTable = [[1.0 for i in range(Constants.SENSOR_COUNT)] for j in range(Constants.SENSOR_COUNT)]
        self.__distanceTable = self.__sensorList.getDistanceBetweenSensors()

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone.getX(), self.__drone.getY()
        while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
            crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
        self.__drone.setX(crtX)
        self.__drone.setY(crtY)

    def __simulateEpoch(self, antCount, alpha, beta, q0, rho):
        ants = [Ant() for i in range(antCount)]  # normally the antCount <= sensor count
        maxPossiblePathDistance = self.__sensorList.getMaxPossibleDistance()
        # we need it in the fitness function, because the path length is inverse proportional with good fitness

        # move the ants
        for ant in ants:
            for step in range(Constants.SENSOR_COUNT - 1):
                ant.nextMove(self.__distanceTable, self.__pheromoneTable, q0, alpha, beta)

        # simulate pheromone evaporation
        for i in range(Constants.SENSOR_COUNT):
            for j in range(Constants.SENSOR_COUNT):
                self.__pheromoneTable[i][j] = (1 - rho) * self.__pheromoneTable[i][j]

        # add the pheromones produced by the last batch of ants
        newPheromones = [1.0 / ant.fitness(self.__distanceTable, maxPossiblePathDistance) for ant in ants]  # check if the order is ok
        for i in range(Constants.SENSOR_COUNT):
            currentPath = ants[i].getPath()
            for j in range(len(currentPath) - 1):
                crtSensor = currentPath[j]
                nextSensor = currentPath[j + 1]
                self.__pheromoneTable[crtSensor][nextSensor] += newPheromones[i]

        bestAnt = None
        bestFitness = 0
        for ant in ants:
            antFitness = ant.fitness(self.__distanceTable, maxPossiblePathDistance)
            if bestFitness < antFitness:
                bestFitness = antFitness
                bestAnt = ant
        return bestAnt.getPath()

    def __computePathLength(self, path):
        if not path:
            return Constants.INFINITY

        length = 0
        for i in range(len(path) - 1):
            crtSensor = path[i]
            nextSensor = path[i + 1]
            length += self.__distanceTable[crtSensor][nextSensor]
        return length

    def __chargeSensors(self, remainingBattery):
        sensors = self.__sensorList.getSensorList()
        sensors.sort(reverse=False, key=lambda s: (s.getAccessiblePositions()[-1] / s.getMaxEnergyLevel()))
        energyLevels = [0 for _ in sensors]
        i = 0
        while i < len(sensors) and remainingBattery > 0:
            currentSensorMaxEnergy = sensors[i].getMaxEnergyLevel()
            if remainingBattery > currentSensorMaxEnergy:
                remainingBattery -= currentSensorMaxEnergy
                energyLevels[i] = currentSensorMaxEnergy
            else:  # drain the entire battery
                energyLevels[i] = remainingBattery
                remainingBattery = 0
            i += 1
        return energyLevels

    def run(self):
        bestSolution = []  # the one with the lowest cost path

        print("Starting")
        for epoch in range(Constants.EPOCH_COUNT):
            currentSolution = self.__simulateEpoch(Constants.ANT_COUNT, Constants.ALPHA, Constants.BETA, Constants.Q0, Constants.RHO)
            if self.__computePathLength(currentSolution) < self.__computePathLength(bestSolution):
                bestSolution = currentSolution.copy()

        energyLevels = self.__chargeSensors(Constants.DRONE_BATTERY - self.__computePathLength(bestSolution))
        print("Best path length = ", self.__computePathLength(bestSolution))
        print("Best path = ", bestSolution)
        print("Energy = ", energyLevels)

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
