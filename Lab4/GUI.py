import pygame
from constants import Constants
from pygame.constants import KEYDOWN
from service import Service


class GUI:
    def __init__(self, service):
        self.__initPygame()
        self.__screen = pygame.display.set_mode((400, 400))
        self.__screen.fill(Constants.WHITE)
        self.__service = service

    def getMapSurface(self):
        return self.__service.getMapSurface()

    def __initPygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("doru exploratoru si formatia")

    def __getMapImage(self, colour = Constants.BLUE, background = Constants.WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)
        sensor.fill(Constants.PINK)

        mapSurface = self.__service.getMapSurface()
        for i in range(Constants.MAP_HEIGHT):
            for j in range(Constants.MAP_WIDTH):
                if mapSurface[i][j] == Constants.WALL_POSITION:
                    image.blit(brick, (j * 20, i * 20))
                elif mapSurface[i][j] == Constants.SENSOR_POSITION:
                    image.blit(sensor, (j * 20, i * 20))

        return image

    def __displayMap(self):
        droneImage = pygame.image.load("minune.jpg")
        pathImage = self.__getMapImage()
        pathImage.blit(droneImage, (self.__service.getDroneYCoord() * 20, self.__service.getDroneXCoord() * 20))
        self.__screen.blit(pathImage, (0, 0))
        pygame.display.update()
        return droneImage, pathImage

    def __waitForKeyboardInput(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.time.wait(1)

    def start(self):
        self.__displayMap()
        self.__waitForKeyboardInput()
        print ("Starting")

        bestSolution = self.__service.run()

        print("Largest number of visible positions = ", bestSolution.getVisiblePositions())
        print("Battery left = ", bestSolution.getBattery())
        print("Path - energy pairs = ", Service.getSolutionFromPath(bestSolution.getPath()))
