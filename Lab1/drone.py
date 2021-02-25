import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.getValueOnPosition(self.x - 1, self.y) == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.getValueOnPosition(self.x + 1, self.y)==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT]and detectedMap.getValueOnPosition(self.x, self.y - 1)==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.getValueOnPosition(self.x, self.y + 1)==0:
                self.y = self.y + 1
                  
    def moveDSF(self, detectedMap):
        pass
        # TO DO!
        # rewrite this function in such a way that you perform an automatic 
        # mapping with DFS