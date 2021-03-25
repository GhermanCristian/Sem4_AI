from constants import Constants


class PathFixer:
    def __init__(self, startingPoint, directionCodes, m):
        self.__startingPoint = startingPoint
        self.__directionCodes = directionCodes
        self.__map = m
        self.__visitedPositions = []
        self.__visitedPositions.append(startingPoint)

    def __validPosition(self, newX, newY):
        return 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH and \
               self.__map[newX][newY] == Constants.EMPTY_POSITION and (newX, newY) not in self.__visitedPositions

    def fixPath(self):
        crtX, crtY = self.__startingPoint
        validPathDirectionCodes = []
        for directionCode in self.__directionCodes:
            direction = Constants.DIRECTIONS[directionCode]

            if self.__validPosition(crtX + direction[0], crtY + direction[1]):
                crtX += direction[0]
                crtY += direction[1]
                self.__visitedPositions.append((crtX, crtY))
                validPathDirectionCodes.append(directionCode)

        return validPathDirectionCodes
