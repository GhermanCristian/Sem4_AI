from drone import Drone
from environment import Environment
from board import Board

class Service:
    def __init__(self):
        self.__environment = Environment()
        self.__board = Board()
        self.__drone = Drone(self.__environment)
    
    def getEnvironment(self):
        return self.__environment
    
    def getBoard(self):
        return self.__board
    
    def getPositionStack(self):
        return self.__drone.getPositionStack()
    
    def getVisitedPositions(self):
        return self.__drone.getVisitedPositions()
    
    def getDroneXCoord(self):
        return self.__drone.getXCoord()
    
    def getDroneYCoord(self):
        return self.__drone.getYCoord()
    
    def droneOneStepDFS(self):
        return self.__drone.moveDFS(self.__board)
    
    def markBoardDetectedWalls(self):
        self.__board.markDetectedWalls(self.__environment, self.__drone.getXCoord(), self.__drone.getYCoord())
        
        
        