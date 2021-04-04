from constants import Constants
from BFS import BFS
import random
from domain.sensor import Sensor


class NodeList:
    def __init__(self, m):
        self.__nodeList = []
        self.__map = m
        self.__mapSurface = m.getMapSurface()
        self.__placeSensors()  #

        self.__distancesBetweenNodes = [[0 for _ in range(Constants.NODE_COUNT)] for _ in range(Constants.NODE_COUNT)]
        self.__computeDistancesBetweenNodes()

        for node in self.__nodeList:
            node.computeAccessiblePositions(self.__mapSurface)
            node.computeMaxEnergyLevel()

    def __placeSensors(self):
        self.__nodeList.clear()  # just in case this function is called multiple times

        for _ in range(Constants.NODE_COUNT):
            crtX, crtY = 0, 0
            while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
                crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
            self.__map.setValueOnPosition(crtX, crtY, Constants.SENSOR_POSITION)
            self.__nodeList.append(Sensor(crtX, crtY))

    def __computeDistancesBetweenNodes(self):
        for i in range(len(self.__nodeList)):
            self.__distancesBetweenNodes[i][i] = 0
            firstX, firstY = self.__nodeList[i].getX(), self.__nodeList[i].getY()
            for j in range(i + 1, len(self.__nodeList)):
                distance = BFS(self.__mapSurface, firstX, firstY, self.__nodeList[j].getX(), self.__nodeList[j].getY()).start()
                self.__distancesBetweenNodes[i][j] = self.__distancesBetweenNodes[j][i] = distance

    def getNodeList(self):
        return self.__nodeList

    def getDistanceBetweenNodes(self):
        return self.__distancesBetweenNodes
