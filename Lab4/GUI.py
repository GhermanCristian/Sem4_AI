import pygame
from constants import Constants
from pygame.constants import KEYDOWN
from domain.sensor import Sensor


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

    def __getMapImage(self, mapSurface, colour = Constants.BLUE, background = Constants.WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        sensor = pygame.Surface((20, 20))
        accessible = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)
        sensor.fill(Constants.PINK)
        accessible.fill(Constants.GREEN)

        for i in range(Constants.MAP_HEIGHT):
            for j in range(Constants.MAP_WIDTH):
                if mapSurface[i][j] == Constants.WALL_POSITION:
                    image.blit(brick, (j * 20, i * 20))
                elif mapSurface[i][j] == Constants.SENSOR_POSITION:
                    image.blit(sensor, (j * 20, i * 20))
                elif mapSurface[i][j] == Constants.ACCESSIBLE_POSITION:
                    image.blit(accessible, (j * 20, i * 20))

        return image

    def __displayMap(self, mapSurface):
        droneImage = pygame.image.load("minune.jpg")
        pathImage = self.__getMapImage(mapSurface)
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

    def __restoreSensorsOnMap(self, mapSurface, nodeList):
        for node in nodeList:
            if isinstance(node, Sensor):
                mapSurface[node.getX()][node.getY()] = Constants.SENSOR_POSITION

    def start(self):
        self.__displayMap(self.__service.getMapSurface())
        self.__waitForKeyboardInput()
        print ("Starting")

        bestSolution = self.__service.run()
        if bestSolution is None:  # this can happen (battery is not enough even for the traversal of the sensors, let alone charging them)
            print ("No solution could be found")
            return

        print("Largest number of visible positions = ", bestSolution.getVisiblePositions())
        print("Battery left = ", bestSolution.getBattery())
        print("Sensor - energy pairs = ", self.__service.getSolutionFromPath(bestSolution.getPath()))

        self.__waitForKeyboardInput()
        mapWithChargedSensors = bestSolution.computeFitness(self.__service.getMapSurface(), self.__service.getNodeList())
        self.__restoreSensorsOnMap(mapWithChargedSensors, self.__service.getNodeList())
        self.__displayMap(mapWithChargedSensors)
        self.__waitForKeyboardInput()
