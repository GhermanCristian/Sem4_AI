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

        for node in self.__nodeList:
            if isinstance(node, Sensor):
                node.computeAccessiblePositions(self.__mapSurface)
                node.computeMaxEnergyLevel()

        self.__distancesBetweenNodes = [[Constants.INFINITY for _ in range(Constants.NODE_COUNT)] for _ in range(Constants.NODE_COUNT)]
        self.__computeDistancesBetweenNodes()

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

    @staticmethod
    def isEntryNode(index):
        return index % Constants.NODES_PER_SENSOR == 0

    @staticmethod
    def isExitNode(index):
        return (index + 1) % Constants.NODES_PER_SENSOR == 0

    @staticmethod
    def isEnergyNode(index):
        return not NodeList.isEntryNode(index) and not NodeList.isExitNode(index)

    @staticmethod
    def getEntryNode(index):
        return index - index % Constants.NODES_PER_SENSOR

    @staticmethod
    def getExitNode(index):
        return NodeList.getEntryNode(index) + Constants.NODES_PER_SENSOR - 1

    def __computeDistancesBetweenNodes(self):
        """
            to connect:
                - each entry to its own energy levels, with cost = energy level
                - each exit to all other entries, with cost = BFS
                - each energy level to its own exit, with cost = 0
        """
        for i in range(len(self.__nodeList)):
            self.__distancesBetweenNodes[i][i] = 0  # this applies to all nodes regardless of type

            if NodeList.isEntryNode(i):  # entry node = sensor
                sensor = self.__nodeList[i]
                for energy in range(Constants.ENERGY_LEVELS):
                    # each sensor has a max 'non-wasteful' energy level (everything above that is wasteful)
                    # so we block the paths which try to access those energy levels
                    if energy <= sensor.getMaxEnergyLevel():
                        self.__distancesBetweenNodes[i][i + energy + 1] = energy
                    else:
                        self.__distancesBetweenNodes[i][i + energy + 1] = Constants.INFINITY

            elif NodeList.isExitNode(i):
                # distance between sensors i, j = dist(i.exit, j.entry) = dist(j.exit, i.entry)
                firstX, firstY = self.__nodeList[i].getX(), self.__nodeList[i].getY()
                for j in range(i + 1, len(self.__nodeList)):
                    if NodeList.isEntryNode(j):
                        distance = BFS(self.__mapSurface, firstX, firstY, self.__nodeList[j].getX(), self.__nodeList[j].getY()).start()
                        self.__distancesBetweenNodes[i][j] = self.__distancesBetweenNodes[NodeList.getExitNode(j)][NodeList.getEntryNode(i)] = distance

            else:  # energy node
                self.__distancesBetweenNodes[i][NodeList.getExitNode(i)] = 0

    def getNodeList(self):
        return self.__nodeList

    def getDistanceBetweenNodes(self):
        return self.__distancesBetweenNodes
