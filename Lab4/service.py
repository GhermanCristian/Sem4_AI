from domain.drone import Drone
from domain.map import Map
from constants import Constants
import random


class Service:
    def __init__(self):
        self.__map = Map()
        self.__drone = Drone(5, 5)
        self.__map.loadMap("test1.map")
        self.__mapSurface = self.__map.getMapSurface()
        self.__placeSensors()
        self.__placeDroneOnEmptyPosition()

    def __placeDroneOnEmptyPosition(self):
        crtX, crtY = self.__drone.getX(), self.__drone.getY()
        while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
            crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
        self.__drone.setX(crtX)
        self.__drone.setY(crtY)

    def __placeSensors(self):
        for s in range(Constants.SENSOR_COUNT):
            crtX, crtY = 0, 0
            while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
                crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
            self.__map.setValueOnPosition(crtX, crtY, Constants.SENSOR_POSITION)

    def getMapSurface(self):
        return self.__map.getMapSurface()

    def getDroneXCoord(self):
        return self.__drone.getX()

    def getDroneYCoord(self):
        return self.__drone.getY()
