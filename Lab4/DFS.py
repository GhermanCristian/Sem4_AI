from constants import Constants


class DFS:
    def __init__(self, m, initialX, initialY, finalX, finalY):
        self.__visitedPositions = []
        self.__visitedPositions.append((initialX, initialY))
        self.__predecessor = {(initialX, initialY): None}
        self.__map = m
        self.__alreadyFound = False
        self.__initialX, self.__initialY = initialX, initialY
        self.__finalX, self.__finalY = finalX, finalY

    def __DFS(self, crtX, crtY):
        if self.__alreadyFound:
            return

        if self.__finalX == crtX and self.__finalY == crtY:
            self.__alreadyFound = True
            return

        for direction in Constants.DIRECTIONS:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if (newX, newY) not in self.__visitedPositions and 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH and self.__map[newX][newY] == Constants.EMPTY_POSITION:
                self.__predecessor[(newX, newY)] = (crtX, crtY)
                self.__visitedPositions.append((newX, newY))
                self.__DFS(newX, newY)

    def __retracePath(self):
        pathAsDirectionCodes = []

        directionCodeDictionary = {}
        for i in range(len(Constants.DIRECTIONS)):
            directionCodeDictionary[Constants.DIRECTIONS[i]] = i

        newX, newY = self.__finalX, self.__finalY
        while self.__predecessor[(newX, newY)] is not None:
            direction = (newX - self.__predecessor[(newX, newY)][0], newY - self.__predecessor[(newX, newY)][1])
            pathAsDirectionCodes.append(directionCodeDictionary[direction])
            newX, newY = self.__predecessor[(newX, newY)]
        pathAsDirectionCodes.reverse()
        return pathAsDirectionCodes

    def start(self):
        self.__DFS(self.__initialX, self.__initialY)
        return self.__retracePath()