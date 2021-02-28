import pygame
from constants import Constants
from service import Service

class GUI:
    def __init__(self):
        self.__service = Service()
    
    def __initialisePygame(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Doru Exploratoru")
    
    def __getEnvironmentImage(self):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((Constants.TILE_SIZE, Constants.TILE_SIZE))
        brick.fill(Constants.BLUE)
        imagine.fill(Constants.WHITE)
        environmentString = str(self.__service.getEnvironment())

        for i in range(Constants.BOARD_HEIGHT):
            for j in range(Constants.BOARD_WIDTH + 1):
                if environmentString[i * (Constants.BOARD_WIDTH + 1) + j] == '1':
                    imagine.blit(brick, (j * Constants.TILE_SIZE, i * Constants.TILE_SIZE))
                
        return imagine
    
    def __createScreen(self):
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        screen.fill(Constants.WHITE)
        screen.blit(self.__getEnvironmentImage(), (0, 0))
        return screen
    
    def __getBoardImage(self):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((Constants.TILE_SIZE, Constants.TILE_SIZE))
        empty = pygame.Surface((Constants.TILE_SIZE, Constants.TILE_SIZE))
        visited = pygame.Surface((Constants.TILE_SIZE, Constants.TILE_SIZE))
        empty.fill(Constants.WHITE)
        brick.fill(Constants.BLACK)
        visited.fill(Constants.GREEN)
        imagine.fill(Constants.GRAYBLUE)
        
        for i in range(Constants.BOARD_HEIGHT):
            for j in range(Constants.BOARD_WIDTH):
                positionValue = self.__service.getBoard().getValueOnPosition(i, j)
                if positionValue == Constants.WALL:
                    imagine.blit(brick, (j * Constants.TILE_SIZE, i * Constants.TILE_SIZE))
                elif (i, j) in self.__service.getVisitedPositions():
                    imagine.blit(visited, (j * Constants.TILE_SIZE, i * Constants.TILE_SIZE))
                elif positionValue == Constants.EMPTY_POSITION:
                    imagine.blit(empty, (j * Constants.TILE_SIZE, i * Constants.TILE_SIZE))
                
        drona = pygame.image.load("minune.jpg")
        imagine.blit(drona, (self.__service.getDronePosition()[1] * Constants.TILE_SIZE, self.__service.getDronePosition()[0] * Constants.TILE_SIZE))
        return imagine
    
    def start(self):
        self.__initialisePygame()
        screen = self.__createScreen()
        
        running = True # define a variable to control the main loop
        while running: # main loop
            for event in pygame.event.get(): # event handling, gets all events from the event queue
                if event.type == pygame.QUIT: # only do something if the event is of type QUIT
                    running = False # change the value to False, to exit the main loop
     
            running = self.__service.droneOneStepDFS()
            
            pygame.time.wait(Constants.TIME_INTERVAL_BETWEEN_MOVES)
            self.__service.markBoardDetectedWalls()
            screen.blit(self.__getBoardImage(), (Constants.BOARD_WIDTH * Constants.BOARD_HEIGHT + Constants.SEPARATOR_SIZE,0))
            pygame.display.update()
           
        pygame.time.wait(Constants.TIME_INTERVAL_FINAL_WAIT) # show the final table at the end
        pygame.quit()
        