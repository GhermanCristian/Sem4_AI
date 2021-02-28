from constants import Constants

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__positionStack = [] # holds pairs of the form (x, y)
        self.__positionStack.append((x, y))
        
        # holds all positions that are / have been at some point in the stack; also holds pairs of the form (x, y)
        self.__visitedPositions = [] 
        self.__visitedPositions.append((x, y))
                  
    def getVisitedPositions(self):
        return self.__visitedPositions # used to display the current path on the board             
                  
    def moveDFS(self, detectedMap): # detectedMap = board
        foundValidSuccessor = False
        newX = self.x
        newY = self.y
        
        # find the next possible move (empty position that hasn't been visited before)
        for crtDirection in Constants.DIRECTIONS:
            newX = self.x + crtDirection[0]
            newY = self.y + crtDirection[1] 
            if detectedMap.validCoordinates(newX, newY) and detectedMap.getValueOnPosition(newX, newY) == Constants.EMPTY_POSITION and (newX, newY) not in self.__visitedPositions:
                self.__positionStack.insert(0, (newX, newY))
                self.__visitedPositions.append((newX, newY))
                foundValidSuccessor = True
                break # only insert the first available one, if any
        
        if foundValidSuccessor == False: # we found a "dead end", we need to go back one position or to end the program
            if len(self.__positionStack) == 0: # end the program, there's nowhere to go back
                return False
            self.x, self.y = self.__positionStack.pop(0) # go back one positiion
        else: # we can advance, move to the position determined above
            self.x = newX
            self.y = newY
            
        return True # True = continue (false would've meant stopping the program)


        