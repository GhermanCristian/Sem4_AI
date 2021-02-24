import numpy as np
from constants import Constants
import pygame

class Board():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1
        
    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the wals that you detect
        wals = e.readUDMSensors(x, y)
        i = x - 1
        if wals[Constants.UP] > 0:
            while ((i>=0) and (i >= x - wals[Constants.UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i>=0):
            self.surface[i][y] = 1
            
        i = x + 1
        if wals[Constants.DOWN] > 0:
            while ((i < self.__n) and (i <= x + wals[Constants.DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1
            
        j = y + 1
        if wals[Constants.LEFT] > 0:
            while ((j < self.__m) and (j <= y + wals[Constants.LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1
        
        j = y - 1
        if wals[Constants.RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[Constants.RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1
        
        return None
        
    def image(self, x, y):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        empty = pygame.Surface((20,20))
        empty.fill(Constants.WHITE)
        brick.fill(Constants.BLACK)
        imagine.fill(Constants.GRAYBLUE)
        
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (self.surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))
                
        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y *20, x*20))
        return imagine
