from map import Map
from drone import Drone
from constants import Constants
from datetime import datetime

class Service:
    def __init__(self):
        self.__map = Map()
        self.__map.loadMap("test1.map")
        self.__drone = Drone(2, 3) #I'll place it by default on an empty position
    
    def __validCoordinates(self, xCoord, yCoord):
        return xCoord >= 0 and yCoord >= 0 and xCoord < Constants.MAP_HEIGHT and yCoord < Constants.MAP_WIDTH \
            and self.__map.getMapSurface()[xCoord][yCoord] == 0
    
    def __computeManhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def __compareFunction(self, firstPos, secondPos, positionEvaluation):
        return positionEvaluation[firstPos] <= positionEvaluation[secondPos]
    
    def __addToQueueAccordingToEvaluation(self, toVisitList, positionEvaluation, newX, newY):
        idx = 0
        while idx < len(toVisitList):
            if self.__compareFunction((newX, newY), toVisitList[idx], positionEvaluation):
                # the distance of the new point is smaller than some point in the queue => we add it here
                toVisitList.insert(idx, (newX, newY))
                return
            idx += 1
        toVisitList.append((newX, newY)) # the new point has the largest distance => it's the last one => add it to the end
    
    def __determineActualPath(self, predecessorDictionary, finalX, finalY):
        actualPath = []
        newX, newY = finalX, finalY
        while predecessorDictionary[(newX, newY)] is not None:
            actualPath.append((newX, newY))
            newX, newY = predecessorDictionary[(newX, newY)]
        actualPath.append((newX, newY))
        actualPath.reverse()
        return actualPath
    
    def __initialiazeStructures(self, initialX, initialY, finalX, finalY):
        visitedPositions = [] # holds pairs (x, y)
        leftToVisit = [] # holds pairs (x, y)
        leftToVisit.append((initialX, initialY))
        predecessorDictionary = {} # key = pair (x, y); value = pair (x, y); value = predecessor of key
        predecessorDictionary[(initialX, initialY)] = None
        distanceFromSource = {} # key = pair(x, y); value = integer
        distanceFromSource[(initialX, initialY)] = 0
        positionEvaluation = {} # key = pair(x, y); value = integer
        positionEvaluation[(initialX, initialY)] = 0 + self.__computeManhattanDistance(initialX, initialY, finalX, finalY)
        
        return visitedPositions, leftToVisit, predecessorDictionary, distanceFromSource, positionEvaluation
    
    def __printAlgorithmResults(self, searchType, searchTime, visitedPositionsCount, actualPathLength):
        print (searchType)
        print (searchTime) 
        print ("Visited: ", visitedPositionsCount)
        print ("Path length: ", actualPathLength)
        print ()
    
    def __processNeighboursGreedy(self, crtX, crtY, visitedPositions, predecessorDictionary, positionEvaluation, leftToVisit, finalX, finalY):
        for direction in Constants.DIRECTIONS:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if self.__validCoordinates(newX, newY) and (newX, newY) not in visitedPositions:
                predecessorDictionary[(newX, newY)] = (crtX, crtY)
                positionEvaluation[(newX, newY)] = self.__computeManhattanDistance(newX, newY, finalX, finalY)
                self.__addToQueueAccordingToEvaluation(leftToVisit, positionEvaluation, newX, newY)
                
    def __processNeighboursAStar(self, crtX, crtY, visitedPositions, predecessorDictionary, distanceFromSource, positionEvaluation, leftToVisit, finalX, finalY):
        for direction in Constants.DIRECTIONS:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if self.__validCoordinates(newX, newY) and (newX, newY) not in visitedPositions:
                predecessorDictionary[(newX, newY)] = (crtX, crtY)
                distanceFromSource[(newX, newY)] = distanceFromSource[(crtX, crtY)] + 1
                positionEvaluation[(newX, newY)] = distanceFromSource[(newX, newY)] + self.__computeManhattanDistance(newX, newY, finalX, finalY)
                self.__addToQueueAccordingToEvaluation(leftToVisit, positionEvaluation, newX, newY)
                
    def __processNeighboursSteepestHillClimbing(self, crtX, crtY, visitedPositions, predecessorDictionary, positionEvaluation, leftToVisit, finalX, finalY):
        bestPosition = (crtX, crtY)
        for direction in Constants.DIRECTIONS:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if self.__validCoordinates(newX, newY) and (newX, newY) not in visitedPositions:
                predecessorDictionary[(newX, newY)] = (crtX, crtY)
                positionEvaluation[(newX, newY)] = self.__computeManhattanDistance(newX, newY, finalX, finalY)
                if self.__compareFunction((newX, newY), bestPosition, positionEvaluation):
                    bestPosition = (newX, newY)
        if bestPosition != (crtX, crtY):
            leftToVisit.append(bestPosition)
    
    def __searchAlgorithm(self, initialX, initialY, finalX, finalY, searchType):
        initialTime = datetime.now()
        self.__drone.setX(initialX)
        self.__drone.setY(initialY)
        
        found = False
        visitedPositions, leftToVisit, predecessorDictionary, distanceFromSource, positionEvaluation = self.__initialiazeStructures(initialX, initialY, finalX, finalY)
        
        while not found and leftToVisit:
            crtX, crtY = leftToVisit.pop(0)
            visitedPositions.append((crtX, crtY))

            if finalX == crtX and finalY == crtY:
                found = True
                break
            
            if searchType == Constants.GREEDY_NAME:
                self.__processNeighboursGreedy(crtX, crtY, visitedPositions, predecessorDictionary, positionEvaluation, leftToVisit, finalX, finalY)
            elif searchType == Constants.A_STAR_NAME:
                self.__processNeighboursAStar(crtX, crtY, visitedPositions, predecessorDictionary, distanceFromSource, positionEvaluation, leftToVisit, finalX, finalY)
            elif searchType == Constants.STEEPEST_HILL_CLIMBING_NAME:
                self.__processNeighboursSteepestHillClimbing(crtX, crtY, visitedPositions, predecessorDictionary, positionEvaluation, leftToVisit, finalX, finalY)
        
        actualPath = []
        if found == True:
            actualPath = self.__determineActualPath(predecessorDictionary, finalX, finalY)
        
        finalTime = datetime.now()
        self.__printAlgorithmResults(searchType, finalTime - initialTime, len(visitedPositions), len(actualPath))
        return visitedPositions, actualPath
    
    def searchGreedy(self, initialX, initialY, finalX, finalY):
        return self.__searchAlgorithm(initialX, initialY, finalX, finalY, Constants.GREEDY_NAME)
    
    def searchAStar(self, initialX, initialY, finalX, finalY):
        return self.__searchAlgorithm(initialX, initialY, finalX, finalY, Constants.A_STAR_NAME)
    
    def searchHillClimbing(self, initialX, initialY, finalX, finalY):
        return self.__searchAlgorithm(initialX, initialY, finalX, finalY, Constants.STEEPEST_HILL_CLIMBING_NAME)
    
    def getMapSurface(self):
        return self.__map.getMapSurface()
    
    def getDroneXCoord(self):
        return self.__drone.getX()
    
    def getDroneYCoord(self):
        return self.__drone.getY()