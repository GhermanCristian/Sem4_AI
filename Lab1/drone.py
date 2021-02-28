from constants import Constants

class Drone():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__positionStack = [] # holds pairs of the form (x, y)
        self.__positionStack.append((x, y))
        
        # holds all positions that are / have been at some point in the stack; also holds pairs of the form (x, y)
        self.__visitedPositions = [] 
        self.__visitedPositions.append((x, y))
                  
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


        