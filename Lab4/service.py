from BFS import BFS
from domain.drone import Drone
from domain.map import Map
from constants import Constants
import random
from domain.sensor import Sensor


class Service:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone(5, 5)
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__sensorList = []
        self.__placeSensors()
        self.__placeDroneOnEmptyPosition()
        self.__distancesBetweenSensors = [[0 for i in range(Constants.SENSOR_COUNT)] for j in range(Constants.SENSOR_COUNT)]
        self.__computeDistancesBetweenSensors()

        for sensor in self.__sensorList:
            sensor.computeAccessiblePositions(self.__mapSurface)

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone.getX(), self.__drone.getY()
        while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
            crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
        self.__drone.setX(crtX)
        self.__drone.setY(crtY)

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
            self.__distancesBetweenSensors[i][i] = Constants.INFINITY
            firstX, firstY = self.__sensorList[i].getX(), self.__sensorList[i].getY()
            for j in range(i + 1, len(self.__sensorList)):
                distance = BFS(self.__mapSurface, firstX, firstY, self.__sensorList[j].getX(), self.__sensorList[j].getY()).start()
                self.__distancesBetweenSensors[i][j] = self.__distancesBetweenSensors[j][i] = distance

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
