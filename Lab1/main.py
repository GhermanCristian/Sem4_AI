# import the pygame module, so you can use it
import pygame
from pygame.constants import KEYDOWN
from random import randint
from drone import Drone
from environment import Environment
from board import Board
from constants import Constants

def main():
    #we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    #print(str(e))
    
    # we create the map
    m = Board() 
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")
        
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #cream drona
    d = Drone(x, y)
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800,400))
    screen.fill(Constants.WHITE)
    screen.blit(e.image(), (0,0))
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == KEYDOWN:
                # use this function instead of move
                #d.moveDSF(m)
                d.move(m)
        pygame.time.wait(1) # lowers the burden on the CPU
        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x,d.y),(400,0))
        pygame.display.update()
       
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()