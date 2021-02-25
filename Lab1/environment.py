import numpy as np, random, pickle, pygame
from constants import Constants

class Environment():
    # no getters and setters on the env / board
    def __init__(self):
        self.__height = 20
        self.__width = 20
        self.__surface = np.zeros((self.__height, self.__width))
    
    def randomMap(self, fill = Constants.BOARD_FILL_PERCENTAGE):
        for i in range(self.__height):
            for j in range(self.__width):
                if random() <= fill :
                    self.__surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.__height):
            for j in range(self.__width):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string
                
    def readUDMSensors(self, x,y):
        readings=[0,0,0,0]
        # UP 
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[Constants.UP] = readings[Constants.UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__height) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[Constants.DOWN] = readings[Constants.DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__width) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[Constants.LEFT] = readings[Constants.LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[Constants.RIGHT] = readings[Constants.RIGHT] + 1
     
        return readings
    
    def saveEnvironment(self, numFile):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__height = dummy.__n
            self.__width = dummy.__m
            self.__surface = dummy.__surface
            f.close()
        
    def image(self, colour = Constants.BLUE, background = Constants.WHITE):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(self.__height):
            for j in range(self.__width):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                
        return imagine
 