import pygame
from random import randint
from drone import Drone
from environment import Environment
from board import Board
from constants import Constants

def initialisePygame():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Doru Exploratoru")

def main():
    e = Environment() #we create the environment
    
    m = Board() # we create the map
    initialisePygame()
        
    # we position the drone somewhere in the area
    # TO-DO: check that the drone is not positioned on an occupied tile (if read sensors returns a list of 0 0 0 0)
    x = randint(0, 19)
    y = randint(0, 19)
    d = Drone(x, y)
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800,400))
    screen.fill(Constants.WHITE)
    screen.blit(e.image(), (0,0))
    
    running = True # define a variable to control the main loop
     
    while running: # main loop
        for event in pygame.event.get(): # event handling, gets all event from the event queue
            if event.type == pygame.QUIT: # only do something if the event is of type QUIT
                running = False # change the value to False, to exit the main loop
 
        running = d.moveDFS(m)
        pygame.time.wait(Constants.TIME_INTERVAL_BETWEEN_MOVES)
        pygame.time.wait(1) # lowers the burden on the CPU, not sure if needed now that we have the wait between moves
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x, d.y, d.getVisitedPositions()), (400,0))
        pygame.display.update()
       
    pygame.time.wait(Constants.TIME_INTERVAL_FINAL_WAIT) # show the final table at the end
    pygame.quit()
     
if __name__=="__main__":
    main()