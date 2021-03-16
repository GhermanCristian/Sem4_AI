import pygame, time
from constants import Constants
from service import Service

class GUI:
    def __init__(self):
        self.__screen = pygame.display.set_mode((400,400))
        self.__screen.fill(Constants.WHITE)
        self.__service = Service()
    
    def __initPygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Doru Exploratoru revine")
    
    def __displayWithPath(self, image, path):
        mark = pygame.Surface((20,20))
        mark.fill(Constants.GREEN)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))
            
        return image
    
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
    
    def __drawDrone(self, mapImage):
        droneImage = pygame.image.load("minune.jpg")
        mapImage.blit(droneImage, (self.__service.getDroneYCoord() * 20, self.__service.getDroneXCoord() * 20))
        return mapImage
    
    def start(self):
        # define a variable to control the main loop
        running = True
         
        # main loop
        while running:
            for event in pygame.event.get(): # event handling, gets all events from the event queue
                if event.type == pygame.QUIT:
                    running = False # exit the main loop
            
            pygame.time.wait(1)
            self.__screen.blit(self.__drawDrone(self.__getMapImage()), (0, 0))
            pygame.display.update()
        
        pygame.display.flip()
        pygame.quit()
