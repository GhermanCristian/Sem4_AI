class Gene:
    def __init__(self, directionCode):
        self.__directionCode = directionCode
        
    def setDirectionCode(self, newDirectionCode):
        self.__directionCode = newDirectionCode
        
    def getDirectionCode(self):
        return self.__directionCode