from constants import Constants
from random import randint

class Drone():
    def __init__(self, environment):
        self.__x = 0
        self.__y = 0
        self.__findEmptyInitialPosition(environment)
        self.__positionStack = [] # holds pairs of the form (x, y)
        self.__positionStack.append((self.__x, self.__y))
        
        # holds all positions that are / have been at some point in the stack; also holds pairs of the form (x, y)
        self.__visitedPositions = [] 
        self.__visitedPositions.append((self.__x, self.__y))
                  
    def __validPosition(self, xCoord, yCoord):
        return xCoord >= 0 and yCoord >= 0 and xCoord < Constants.BOARD_HEIGHT and yCoord < Constants.BOARD_WIDTH 
    
    def __findEmptyInitialPosition(self, environment):
        while True:
            self.__x = randint(0, Constants.BOARD_HEIGHT - 1)
            self.__y = randint(0, Constants.BOARD_WIDTH - 1)
            print (self.__x, self.__y)
            
            # we read the sensors for the first tile in each direction, then we check if there's a wall on the tile in its opposite
            # direction (so our tile); we have the relation that UP + DOWN = LEFT + RIGHT = 3
            # we need to check all 4 to ensure that we have one that's 'inside'
            for directionIndex in range(4):
                direction = Constants.DIRECTIONS[directionIndex]
                if self.__validPosition(self.__x + direction[0], self.__y + direction[1]):
                    resultArray = environment.readUDMSensors(self.__x + direction[0], self.__y + direction[1])
                    if resultArray[3 - directionIndex] != 0: # there's no wall on the current position
                        return         
                  
    def getPositionStack(self):
        return self.__positionStack              
                  
    def getVisitedPositions(self):
        return self.__visitedPositions # used to display the current path on the board
    
    def getXCoord(self):
        return self.__x
    
    def getYCoord(self):
        return self.__y  
                  
    def moveDFS(self, detectedMap): # detectedMap = board
        newX = self.__x
        newY = self.__y
        
        # find the next possible move (empty position that hasn't been visited before)
        for crtDirection in Constants.DIRECTIONS:
            newX = self.__x + crtDirection[0]
            newY = self.__y + crtDirection[1] 
            if detectedMap.validCoordinates(newX, newY) and detectedMap.getValueOnPosition(newX, newY) == Constants.EMPTY_POSITION and (newX, newY) not in self.__visitedPositions:
                self.__positionStack.insert(0, (self.__x, self.__y))
                self.__x = newX # we can advance, move to the position determined above
                self.__y = newY
                self.__visitedPositions.append((newX, newY))
                return True # only insert the first available one, if any
        
        # we found a "dead end", we need to go back one position or to end the program
        if len(self.__positionStack) == 0: # end the program, there's nowhere to go back
            return False

        self.__x, self.__y = self.__positionStack.pop(0) # go back one positiion
        return True # True = continue (false would've meant stopping the program)


        