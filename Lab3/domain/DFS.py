from constants import Constants
import random

class DFS:
    def __init__(self, m, requiredLength, initialX, initialY):
        self.__visitedPositions = []
        self.__visitedPositions.append((initialX, initialY))
        self.__predecessor = {}
        self.__predecessor[(initialX, initialY)] = None
        self.__map = m
        self.__requiredLength = requiredLength
        self.__alreadyFound = False
        self.__initialX, self.__initialY = initialX, initialY
        self.__finalX, self.__finalY = initialX, initialY
        self.__newDirections = random.sample(Constants.DIRECTIONS, 4) #otherwise everyone would have the same path every time
        
    def __DFS(self, crtX, crtY, crtLength):
        if self.__alreadyFound:
            return
        
        if self.__requiredLength == crtLength:
            if random.random() < 0.25: # we don't want to always select the first valid path, to reduce repetition
                self.__alreadyFound = True
                self.__finalX, self.__finalY = crtX, crtY
            return
        
        for direction in self.__newDirections:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if (newX, newY) not in self.__visitedPositions and 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH\
            and self.__map[newX][newY] == Constants.EMPTY_POSITION:
                self.__predecessor[(newX, newY)] = (crtX, crtY)
                self.__visitedPositions.append((newX, newY))
                self.__DFS(newX, newY, crtLength + 1)
                
    def __retracePath(self):
        pathAsDirectionCodes = []
        directionCodeDictionary = {(-1, 0) : 0, (0, 1) : 1, (1, 0) : 2, (0, -1) : 3}
        newX, newY = self.__finalX, self.__finalY
        while self.__predecessor[(newX, newY)] is not None:
            direction = (newX - self.__predecessor[(newX, newY)][0], newY - self.__predecessor[(newX, newY)][1])
            pathAsDirectionCodes.append(directionCodeDictionary[direction])
            newX, newY = self.__predecessor[(newX, newY)]
        pathAsDirectionCodes.reverse()
        return pathAsDirectionCodes        
                
    def start(self):
        self.__DFS(self.__initialX, self.__initialY, 1)
        return self.__retracePath()