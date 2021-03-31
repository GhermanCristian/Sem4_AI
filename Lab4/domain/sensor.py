from constants import Constants


class Sensor:
    def __init__(self, xCoord, yCoord):
        self.__xCoord = xCoord  # the coords are valid
        self.__yCoord = yCoord
        self.__accessiblePositions = [0 for i in range(6)]  # for each energy 0 -> 5

    def __isValid(self, x, y, mapSurface):
        return 0 <= x < Constants.MAP_WIDTH and 0 <= y < Constants.MAP_HEIGHT and mapSurface[x][
            y] == Constants.EMPTY_POSITION

    def computeAccessiblePositions(self, mapSurface):
        # this should be called after all the sensors have been placed
        directions = Constants.DIRECTIONS
        blockedDirection = [False for i in range(len(directions))]
        for energy in range(1, 6):
            self.__accessiblePositions[energy] = self.__accessiblePositions[energy - 1]  # just in case we call this function multiple times
            for i in range(len(directions)):
                if not blockedDirection[i]:
                    direction = directions[i]
                    if self.__isValid(self.__xCoord + direction[0] * energy, self.__yCoord + direction[1] * energy, mapSurface):
                        self.__accessiblePositions[energy] += 1
                    else:
                        blockedDirection[i] = True

    def getAccessiblePositions(self):
        return self.__accessiblePositions

    def getX(self):
        return self.__xCoord

    def getY(self):
        return self.__yCoord
