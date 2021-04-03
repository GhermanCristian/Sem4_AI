from constants import Constants


class DFS:
    def __init__(self, m, initialX, initialY, finalX, finalY):
        self.__visitedPositions = []
        self.__visitedPositions.append((initialX, initialY))
        self.__distance = -1  # from source to destination
        self.__map = m
        self.__initialX, self.__initialY = initialX, initialY
        self.__finalX, self.__finalY = finalX, finalY

    def __DFS(self, crtX, crtY, crtDistance):
        if self.__distance >= 0:  # already found a solution
            return

        if self.__finalX == crtX and self.__finalY == crtY:
            self.__distance = crtDistance
            return

        for direction in Constants.DIRECTIONS:
            newX = crtX + direction[0]
            newY = crtY + direction[1]
            if (newX, newY) not in self.__visitedPositions and 0 <= newX < Constants.MAP_HEIGHT and 0 <= newY < Constants.MAP_WIDTH and \
                    self.__map[newX][newY] == Constants.EMPTY_POSITION:
                self.__visitedPositions.append((newX, newY))
                self.__DFS(newX, newY, crtDistance + 1)

    def start(self):
        self.__DFS(self.__initialX, self.__initialY, 0)
        return self.__distance
