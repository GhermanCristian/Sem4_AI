class Gene:
    def __init__(self, directionCode):
        # each gene is the code for a direction (UP = 0, DOWN = 2, LEFT = 1, RIGHT = 3)
        self.__directionCode = directionCode

    def setDirectionCode(self, newDirectionCode):
        self.__directionCode = newDirectionCode

    def getDirectionCode(self):
        return self.__directionCode
