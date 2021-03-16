from map import Map
from drone import Drone
from random import randint

class Service:
    def __init__(self):
        self.__map = Map();
        #self.__map.randomMap()
        #self.__map.saveMap("test1.map")
        self.__map.loadMap("test1.map")
        #self.__drone = Drone(randint(0, 19), randint(0, 19))
        self.__drone = Drone(2, 3) #I'll place it by default on an empty position
    
    def searchAStar(self, mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO 
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y] 
        
        pass
    
    def searchGreedy(self, mapM, droneD, initialX, initialY, finalX, finalY):
        # TO DO 
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        pass
    
    def getMapSurface(self):
        return self.__map.getMapSurface()
    
    def getDroneXCoord(self):
        return self.__drone.getX()
    
    def getDroneYCoord(self):
        return self.__drone.getY()