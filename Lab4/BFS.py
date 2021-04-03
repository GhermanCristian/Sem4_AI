from constants import Constants


class BFS:
    def __init__(self, m, initialX, initialY, finalX, finalY):
        self.__distance = {(initialX, initialY): 0}
        self.__map = m
        self.__initialX, self.__initialY = initialX, initialY
        self.__finalX, self.__finalY = finalX, finalY
        self.__toVisitQueue = []
        self.__toVisitQueue.append((self.__initialX, self.__initialY))

    def __BFS(self, crtX, crtY):
        while self.__toVisitQueue:
            crtX, crtY = self.__toVisitQueue.pop(0)
            for direction in Constants.DIRECTIONS:
                newX = crtX + direction[0]
                newY = crtY + direction[1]
                if 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH and self.__map[newX][newY] != Constants.WALL_POSITION \
                        and (newX, newY) not in self.__distance:
                    self.__distance[(newX, newY)] = self.__distance[(crtX, crtY)] + 1
                    self.__toVisitQueue.append((newX, newY))
                    if newX == self.__finalX and newY == self.__finalY:
                        return self.__distance[(self.__finalX, self.__finalY)]

        return -1

    def start(self):
        return self.__BFS(self.__initialX, self.__initialY)