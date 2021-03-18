class Drone():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        
    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def setX(self, newX):
        self.__x = newX
        
    def setY(self, newY):
        self.__y = newY