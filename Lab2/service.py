from map import Map
from drone import Drone
from constants import Constants

class Service:
    def __init__(self):
        self.__map = Map();
        self.__map.loadMap("test1.map")
        self.__drone = Drone(2, 3) #I'll place it by default on an empty position
    
    def __validCoordinates(self, xCoord, yCoord):
        return xCoord >= 0 and yCoord >= 0 and xCoord < Constants.MAP_HEIGHT and yCoord < Constants.MAP_WIDTH \
            and self.__map.getMapSurface()[xCoord][yCoord] == 0
    
    def __computeManhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def __compareGreedy(self, newX, newY, currentX, currentY, existingX, existingY, finalX, finalY):
        # h(n) = manhattan distance (n, finalPoint)
        # currentX, currentY are passed as arguments because they are needed for the arg list of roleFunction (that coord is required for A*)
        manhattanDistanceNewPoint = self.__computeManhattanDistance(newX, newY, finalX, finalY)
        manhattanDistanceExistingPoint = self.__computeManhattanDistance(existingX, existingY, finalX, finalY)
        return manhattanDistanceNewPoint > manhattanDistanceExistingPoint
    
    def __addToQueueAccordingToRule(self, toVisitList, newX, newY, currentX, currentY, finalX, finalY, ruleFunction):
        pos = 0
        while pos < len(toVisitList):
            if ruleFunction(newX, newY, currentX, currentY, toVisitList[pos][0], toVisitList[pos][1], finalX, finalY) == False:
                # the distance of the new point is smaller than some point in the queue => we add it here
                toVisitList.insert(pos, (newX, newY))
                return
            pos += 1
        toVisitList.append((newX, newY)) # the new point has the largest distance => it's the last one => add it to the end
    
    def searchGreedy(self, initialX, initialY, finalX, finalY):
        found = False
        visitedPositions = [] # holds pairs (x, y)
        leftToVisit = [] # holds pairs (x, y)
        leftToVisit.append((initialX, initialY))
        
        while not found and leftToVisit:
            crtX, crtY = leftToVisit.pop(0)
            visitedPositions.append((crtX, crtY))

            if finalX == crtX and finalY == crtY:
                found = True
                break
            
            for direction in Constants.DIRECTIONS:
                newX = crtX + direction[0]
                newY = crtY + direction[1]
                if self.__validCoordinates(newX, newY) and (newX, newY) not in visitedPositions:
                    self.__addToQueueAccordingToRule(leftToVisit, newX, newY, crtX, crtY, finalX, finalY, self.__compareGreedy)
        
        # retrace path
                    
        return visitedPositions
    
    def searchAStar(self, initialX, initialY, finalX, finalY):
        pass
    
    def getMapSurface(self):
        return self.__map.getMapSurface()
    
    def getDroneXCoord(self):
        return self.__drone.getX()
    
    def getDroneYCoord(self):
        return self.__drone.getY()