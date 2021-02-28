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
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        brick.fill(Constants.BLUE)
        imagine.fill(Constants.WHITE)
        environmentString = str(self.__service.getEnvironment())

        for i in range(Constants.BOARD_HEIGHT):
            for j in range(Constants.BOARD_WIDTH + 1):
                if environmentString[i * (Constants.BOARD_WIDTH + 1) + j] == '1':
                    imagine.blit(brick, (j * 20, i * 20))
                
        return imagine
    
    def __createScreen(self):
        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(Constants.WHITE)
        screen.blit(self.__getEnvironmentImage(), (0, 0))
        return screen
    
    def __getBoardImage(self):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        empty = pygame.Surface((20,20))
        visited = pygame.Surface((20, 20))
        empty.fill(Constants.WHITE)
        brick.fill(Constants.BLACK)
        visited.fill(Constants.GREEN)
        imagine.fill(Constants.GRAYBLUE)
        
        for i in range(Constants.BOARD_HEIGHT):
            for j in range(Constants.BOARD_WIDTH):
                positionValue = self.__service.getBoard().getValueOnPosition(i, j)
                if positionValue == Constants.WALL:
                    imagine.blit(brick, (j * 20, i * 20))
                elif (i, j) in self.__service.getVisitedPositions():
                    imagine.blit(visited, (j * 20, i * 20))
                elif positionValue == Constants.EMPTY_POSITION:
                    imagine.blit(empty, (j * 20, i * 20))
                
        drona = pygame.image.load("minune.jpg")
        imagine.blit(drona, (self.__service.getDronePosition()[1] * 20, self.__service.getDronePosition()[0] * 20))
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
            screen.blit(self.__getBoardImage(), (400,0))
            pygame.display.update()
           
        pygame.time.wait(Constants.TIME_INTERVAL_FINAL_WAIT) # show the final table at the end
        pygame.quit()
        