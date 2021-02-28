import numpy as np
from constants import Constants

class Board():
    def __init__(self):
        self.__height = Constants.BOARD_HEIGHT
        self.__width = Constants.BOARD_WIDTH
        self.__surface = np.zeros((self.__height, self.__width))
        for i in range(self.__height):
            for j in range(self.__width):
                self.__surface[i][j] = -1
        
    def markDetectedWalls(self, e, x, y):
        # mark on this map the walls that you detect
        walls = e.readUDMSensors(x, y)
        i = x - 1
        if walls[Constants.UP] > 0:
            while ((i>=0) and (i >= x - walls[Constants.UP])):
                self.__surface[i][y] = 0
                i = i - 1
        if (i>=0):
            self.__surface[i][y] = 1
            
        i = x + 1
        if walls[Constants.DOWN] > 0:
            while ((i < self.__height) and (i <= x + walls[Constants.DOWN])):
                self.__surface[i][y] = 0
                i = i + 1
        if (i < self.__height):
            self.__surface[i][y] = 1
            
        j = y + 1
        if walls[Constants.LEFT] > 0:
            while ((j < self.__width) and (j <= y + walls[Constants.LEFT])):
                self.__surface[x][j] = 0
                j = j + 1
        if (j < self.__width):
            self.__surface[x][j] = 1
        
        j = y - 1
        if walls[Constants.RIGHT] > 0:
            while ((j >= 0) and (j >= y - walls[Constants.RIGHT])):
                self.__surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.__surface[x][j] = 1
        
    def validCoordinates(self, xCoord, yCoord):
        return xCoord >= 0 and yCoord >= 0 and xCoord < self.__height and yCoord < self.__width 
        
    def getValueOnPosition(self, xCoord, yCoord):
        if self.validCoordinates(xCoord, yCoord) == False:
            raise IndexError("Coordinates out of bounds")
        return self.__surface[xCoord][yCoord]
