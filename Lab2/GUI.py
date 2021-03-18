import pygame
from constants import Constants
from service import Service
from pygame.constants import KEYDOWN

class GUI:
    def __init__(self):
        self.__initPygame()
        self.__screen = pygame.display.set_mode((400,400))
        self.__screen.fill(Constants.WHITE)
        self.__service = Service()
    
    def __initPygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Doru Exploratoru revine")
    
    def __getMapImage(self, colour = Constants.BLUE, background = Constants.WHITE):
        image = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(colour)
        image.fill(background)
        
        mapSurface = self.__service.getMapSurface()
        for i in range(Constants.MAP_HEIGHT):
            for j in range(Constants.MAP_WIDTH):
                if (mapSurface[i][j] == 1):
                    image.blit(brick, (j * 20, i * 20))
                
        return image
    
    def __moveDroneAlongPath(self, droneImage, pathImage, actualPath):
        pathTile = pygame.Surface((20,20))
        pathTile.fill(Constants.GREEN)
        
        for position in actualPath:
            pathImage.blit(pathTile, (position[1] * 20, position[0] * 20))
            pathImageCopy = pathImage.copy()
            pathImageCopy.blit(droneImage, (position[1] * 20, position[0] * 20))
            self.__screen.blit(pathImageCopy, (0, 0))
            pygame.display.update()
            pygame.time.wait(Constants.TIME_BETWEEN_MOVES)
    
    def __displayWithPath(self, visitedPositions, actualPath):
        droneImage = pygame.image.load("minune.jpg")
        
        visitedTile = pygame.Surface((20,20))
        visitedTile.fill(Constants.RED)
        pathImage = self.__getMapImage()
        
        # show all the visited positions
        for position in visitedPositions:
            pathImage.blit(visitedTile, (position[1] * 20, position[0] * 20))
        pathImage.blit(droneImage, (self.__service.getDroneYCoord() * 20, self.__service.getDroneXCoord() * 20))
        self.__screen.blit(pathImage, (0, 0))
        pygame.display.update()
        
        # then progressively show the actual path of the drone
        self.__moveDroneAlongPath(droneImage, pathImage, actualPath)
    
    def __waitForKeyboardInput(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.time.wait(1)
    
    def __runAlgorithm(self, searchAlgorithm, initialX, initialY, finalX, finalY):
        visitedPositions, actualPath = searchAlgorithm(initialX, initialY, finalX, finalY)
        self.__displayWithPath(visitedPositions, actualPath)
        self.__waitForKeyboardInput()
    
    def start(self):
        self.__runAlgorithm(self.__service.searchGreedy, 2, 3, 19, 19)
        self.__runAlgorithm(self.__service.searchAStar, 2, 3, 19, 19)
        self.__runAlgorithm(self.__service.searchHillClimbing, 2, 3, 3, 13) # finds the path
        self.__runAlgorithm(self.__service.searchHillClimbing, 2, 3, 19, 19) # doesn't find the path

        pygame.quit()
