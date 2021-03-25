import numpy as np
from random import random
import pickle
from constants import Constants


class Map():
    def __init__(self):
        self.__n = Constants.MAP_HEIGHT
        self.__m = Constants.MAP_WIDTH
        self.__surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.15):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.__surface[i][j] = Constants.WALL_POSITION

    def __str__(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j])) + " "
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()

    def getMapSurface(self):
        return self.__surface
