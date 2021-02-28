from random import randint
from drone import Drone
from environment import Environment
from board import Board

class Service:
    def __init__(self):
        self.__environment = Environment()
        self.__board = Board()
        x = randint(0, 19)
        y = randint(0, 19)
        self.__drone = Drone(x, y) # we have to check that the drone is not on an occupied tile (if read sensors returns a list of 0 0 0 0)
    
    def getEnvironment(self):
        return self.__environment
    
    def getBoard(self):
        return self.__board
    
    def getVisitedPositions(self):
        return self.__drone.getVisitedPositions()
    
    def getDronePosition(self):
        return (self.__drone.x, self.__drone.y)
    
    def droneOneStepDFS(self):
        return self.__drone.moveDFS(self.__board)
    
    def markBoardDetectedWalls(self):
        self.__board.markDetectedWalls(self.__environment, self.__drone.x, self.__drone.y)
        
        
        