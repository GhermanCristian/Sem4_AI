import pygame
from constants import Constants
from pygame.constants import KEYDOWN


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
        pygame.display.set_caption("Doru Exploratoru revine")

    def __getMapImage(self, colour=Constants.BLUE, background=Constants.WHITE):
        image = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        image.fill(background)

        mapSurface = self.__service.getMapSurface()
        for i in range(Constants.MAP_HEIGHT):
            for j in range(Constants.MAP_WIDTH):
                if mapSurface[i][j] == Constants.WALL_POSITION:
                    image.blit(brick, (j * 20, i * 20))

        return image

    def __moveDroneAlongPath(self, droneImage, pathImage, pathAsDirectionCodes):
        pathTile = pygame.Surface((20, 20))
        pathTile.fill(Constants.GREEN)

        crtPosition = (self.__service.getDroneXCoord(), self.__service.getDroneYCoord())

        for directionCode in pathAsDirectionCodes:
            pathImage.blit(pathTile, (crtPosition[1] * 20, crtPosition[0] * 20))
            pathImageCopy = pathImage.copy()
            pathImageCopy.blit(droneImage, (crtPosition[1] * 20, crtPosition[0] * 20))
            self.__screen.blit(pathImageCopy, (0, 0))
            pygame.display.update()
            pygame.time.wait(Constants.TIME_BETWEEN_MOVES)

            direction = Constants.DIRECTIONS[directionCode]
            crtPosition = (crtPosition[0] + direction[0], crtPosition[1] + direction[1])

    def __displayMap(self):
        droneImage = pygame.image.load("minune.jpg")
        pathImage = self.__getMapImage()
        pathImage.blit(droneImage, (self.__service.getDroneYCoord() * 20, self.__service.getDroneXCoord() * 20))
        self.__screen.blit(pathImage, (0, 0))
        pygame.display.update()
        return droneImage, pathImage

    def displayWithPath(self, pathAsDirectionCodes):
        droneImage, pathImage = self.__displayMap()
        # then progressively show the actual path of the drone
        self.__moveDroneAlongPath(droneImage, pathImage, pathAsDirectionCodes)
        self.__waitForKeyboardInput()

    def __waitForKeyboardInput(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            pygame.time.wait(1)

    def start(self):
        self.__displayMap()
        solutionAverages, bestIndividuals, runningTimes = self.__service.runProgram()
        self.__waitForKeyboardInput()

        bestIndividuals.sort(key=lambda elem: elem.getFitness(), reverse=True)
        for i in bestIndividuals[:5]:
            self.displayWithPath(i.getChromosome())
        return solutionAverages, runningTimes
