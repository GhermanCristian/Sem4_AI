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

    def __moveAnts(self, ants, alpha, beta, q0):
        isAntAlive = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for step in range(Constants.SENSOR_COUNT - 1):
                successfulMoveCompletion = ant.nextMove(self.__distanceTable, self.__pheromoneTable, q0, alpha, beta)
                if not successfulMoveCompletion:
                    isAntAlive[i] = False
                    break  # no use in trying to move the ant if it has no battery left / is dead

        aliveAnts = []  # only return the ants which completed the path
        for i in range(len(ants)):
            if isAntAlive[i]:
                ants[i].computeFitness(self.__distanceTable)  # no use computing the fitness of dead ants
                aliveAnts.append(ants[i])
        return aliveAnts

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
        ants = self.__moveAnts(ants, alpha, beta, q0)

        # simulate pheromone evaporation; it has to be done even if all ants die
        for i in range(Constants.SENSOR_COUNT):
            for j in range(Constants.SENSOR_COUNT):
                self.__pheromoneTable[i][j] = (1 - rho) * self.__pheromoneTable[i][j]

        if not ants:
            return None
        # add the pheromones produced by the last batch of ants
        newPheromones = [1.0 / ant.getFitness() for ant in ants]  # TO-DO: check if the order is ok
        for i in range(len(ants)):
            currentPath = ants[i].getPath()
            for j in range(len(currentPath) - 1):
                crtSensor = currentPath[j]
                nextSensor = currentPath[j + 1]
                self.__pheromoneTable[crtSensor][nextSensor] += newPheromones[i]

        return self.__selectBestAnt(ants)

    def __chargeSensors(self, remainingBattery, accessibleSensors):
        sensors = []  # only charge the sensors that have been reached by the drone
        for i in range(len(self.__sensorList.getSensorList())):
            if i in accessibleSensors:
                sensors.append(self.__sensorList.getSensorList()[i])

        energyLevels = [0 for _ in sensors]
        if remainingBattery <= 0:
            return energyLevels

        sensors.sort(reverse=False, key=lambda s: (s.getAccessiblePositions()[-1] / s.getMaxEnergyLevel()))
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

    def __updateBestSolution(self, bestSolution):
        currentSolution = self.__simulateEpoch(Constants.ANT_COUNT, Constants.ALPHA, Constants.BETA, Constants.Q0, Constants.RHO)
        if currentSolution is None:
            return bestSolution

        currentSolutionPathLength = len(currentSolution.getPath())
        if bestSolution is None or currentSolutionPathLength > len(bestSolution.getPath()) or (currentSolutionPathLength == len(bestSolution.getPath()) and currentSolution.getFitness() < bestSolution.getFitness()):
            return currentSolution  # new best solution
        return bestSolution

    def run(self):
        bestSolution = None  # will be the one with the lowest cost path

        print("Starting")
        for epoch in range(Constants.EPOCH_COUNT):
            bestSolution = self.__updateBestSolution(bestSolution)

        energyLevels = self.__chargeSensors(Constants.DRONE_BATTERY - bestSolution.computePathLength(self.__distanceTable), bestSolution.getPath())
        print("Best battery economy = ", bestSolution.computePathLength(self.__distanceTable))
        print("Best path = ", bestSolution.getPath())
        print("Energy = ", energyLevels)

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
