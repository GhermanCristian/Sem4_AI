from constants import Constants
from BFS import BFS
import random
from domain.sensor import Sensor
from domain.node import Node


class NodeList:
    def __init__(self, m):
        self.__nodeList = []  # contains sensors (= entry nodes) and 'normal' nodes (= exit + energy nodes)
        self.__map = m
        self.__mapSurface = m.getMapSurface()
        self.__placeNodes()  #

        self.__distancesBetweenNodes = [[Constants.INFINITY for _ in range(Constants.NODE_COUNT)] for _ in range(Constants.NODE_COUNT)]
        self.__computeDistancesBetweenNodes()

        for node in self.__nodeList:
            if isinstance(node, Sensor):
                node.computeAccessiblePositions(self.__mapSurface)
                node.computeMaxEnergyLevel()

    def __placeExtraNodesForASensor(self, crtX, crtY):
        for _ in range(Constants.ENERGY_LEVELS + 1):  # the energy levels + the exit node
            self.__nodeList.append(Node(crtX, crtY))

    def __placeNodes(self):
        self.__nodeList.clear()  # just in case this function is called multiple times

        for _ in range(Constants.SENSOR_COUNT):  # first place the node for the sensor (entry node), then the exit + energy levels
            crtX, crtY = 0, 0
            while self.__mapSurface[crtX][crtY] != Constants.EMPTY_POSITION:
                crtX, crtY = random.randint(0, Constants.MAP_HEIGHT - 1), random.randint(0, Constants.MAP_WIDTH - 1)
            self.__map.setValueOnPosition(crtX, crtY, Constants.SENSOR_POSITION)
            self.__nodeList.append(Sensor(crtX, crtY))
            self.__placeExtraNodesForASensor(crtX, crtY)

    def __isEntryNode(self, index):
        return index % Constants.NODES_PER_SENSOR == 0

    def __isExitNode(self, index):
        return (index + 1) % Constants.NODES_PER_SENSOR == 0

    def __isEnergyNode(self, index):
        return not self.__isEntryNode(index) and not self.__isExitNode(index)

    def __getEntryNode(self, index):
        return index - index % Constants.NODES_PER_SENSOR

    def __getExitNode(self, index):
        return self.__getEntryNode(index) + Constants.NODES_PER_SENSOR - 1

    def __computeDistancesBetweenNodes(self):
        """
            to connect:
                - each entry to its own energy levels, with cost = energy level
                - each exit to all other entries, with cost = BFS
                - each energy level to its own exit, with cost = 0
        """
        for i in range(len(self.__nodeList)):
            self.__distancesBetweenNodes[i][i] = 0  # this applies to all nodes regardless of type

            if self.__isEntryNode(i):
                for energy in range(Constants.ENERGY_LEVELS):
                    self.__distancesBetweenNodes[i][i + energy + 1] = energy

            elif self.__isExitNode(i):
                # distance between sensors i, j = dist(i.exit, j.entry) = dist(j.exit, i.entry)
                firstX, firstY = self.__nodeList[i].getX(), self.__nodeList[i].getY()
                for j in range(i + 1, len(self.__nodeList)):
                    if self.__isEntryNode(j):
                        distance = BFS(self.__mapSurface, firstX, firstY, self.__nodeList[j].getX(), self.__nodeList[j].getY()).start()
                        self.__distancesBetweenNodes[i][j] = self.__distancesBetweenNodes[self.__getExitNode(j)][self.__getEntryNode(i)] = distance

            else:  # energy node
                self.__distancesBetweenNodes[i][self.__getExitNode(i)] = 0

    def getNodeList(self):
        return self.__nodeList

    def getDistanceBetweenNodes(self):
        return self.__distancesBetweenNodes
