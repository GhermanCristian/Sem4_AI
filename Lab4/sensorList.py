from constants import Constants
from BFS import BFS
import random
from domain.sensor import Sensor


class SensorList:
    def __init__(self, m):
        self.__sensorList = []
        self.__map = m
        self.__mapSurface = m.getMapSurface()
        self.__placeSensors()

        self.__distancesBetweenSensors = [[0 for i in range(Constants.SENSOR_COUNT)] for j in range(Constants.SENSOR_COUNT)]
        self.__computeDistancesBetweenSensors()

        for sensor in self.__sensorList:
            sensor.computeAccessiblePositions(self.__mapSurface)
            sensor.computeMaxEnergyLevel()

    def __placeSensors(self):
        self.__sensorList.clear()  # just in case this function is called multiple times

        for s in range(Constants.SENSOR_COUNT):
            crtX, crtY = 0, 0
            while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
                crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
            self.__map.setValueOnPosition(crtX, crtY, Constants.SENSOR_POSITION)
            self.__sensorList.append(Sensor(crtX, crtY))

    def __computeDistancesBetweenSensors(self):
        for i in range(len(self.__sensorList)):
            self.__distancesBetweenSensors[i][i] = 0
            firstX, firstY = self.__sensorList[i].getX(), self.__sensorList[i].getY()
            for j in range(i + 1, len(self.__sensorList)):
                distance = BFS(self.__mapSurface, firstX, firstY, self.__sensorList[j].getX(), self.__sensorList[j].getY()).start()
                self.__distancesBetweenSensors[i][j] = self.__distancesBetweenSensors[j][i] = distance

    def getSensorList(self):
        return self.__sensorList

    def getDistanceBetweenSensors(self):
        return self.__distancesBetweenSensors
