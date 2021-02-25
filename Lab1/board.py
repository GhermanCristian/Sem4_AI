import numpy as np
from constants import Constants
import pygame

class Board():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.__surface[i][j] = -1
        
    def markDetectedWalls(self, e, x, y):
        #   To DO
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
            while ((i < self.__n) and (i <= x + walls[Constants.DOWN])):
                self.__surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.__surface[i][y] = 1
            
        j = y + 1
        if walls[Constants.LEFT] > 0:
            while ((j < self.__m) and (j <= y + walls[Constants.LEFT])):
                self.__surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.__surface[x][j] = 1
        
        j = y - 1
        if walls[Constants.RIGHT] > 0:
            while ((j >= 0) and (j >= y - walls[Constants.RIGHT])):
                self.__surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.__surface[x][j] = 1
        
    def getValueOnPosition(self, xCoord, yCoord):
        if xCoord < 0 or yCoord < 0 or xCoord >= self.__n or yCoord >= self.__m:
            raise IndexError("Coordinates out of bounds")
        return self.__surface[xCoord][yCoord]
        
    def image(self, x, y):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        empty = pygame.Surface((20,20))
        empty.fill(Constants.WHITE)
        brick.fill(Constants.BLACK)
        imagine.fill(Constants.GRAYBLUE)
        
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (self.__surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))
                
        drona = pygame.image.load("minune.jpg")
        imagine.blit(drona, (y *20, x*20))
        return imagine
