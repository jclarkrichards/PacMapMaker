import pygame
from vector import Vector2
from constants import *

class Grid(object):
    def __init__(self):
        self.show = False
        self.color = (20,20,20)
        self.lineWidth = 1
        
    def toggle(self):
        self.show = not self.show

    def horizontalLine(self, screen, y):
        pygame.draw.line(screen, self.color, (0,y), (SCREENWIDTH, y),
                         self.lineWidth)
        
    def verticalLine(self, screen, x):
        pygame.draw.line(screen, self.color, (x,0), (x, SCREENHEIGHT),
                         self.lineWidth)

    def increaseWidth(self):
        self.lineWidth += 1

    def decreaseWidth(self):
        self.lineWidth -=  1
        if self.lineWidth == 0: self.lineWidth = 1
        
    def fade(self):
        color = list(self.color)
        color[0] -= 10
        color[1] -= 10
        color[2] -= 10
        color[0] = max(color[0], 0)
        color[1] = max(color[1], 0)
        color[2] = max(color[2], 0)
        self.color = color

    def unfade(self):
        color = list(self.color)
        color[0] += 10
        color[1] += 10
        color[2] += 10
        color[0] = min(color[0], 255)
        color[1] = min(color[1], 255)
        color[2] = min(color[2], 255)
        self.color = color
    
    def render(self, screen):
        if self.show:
            for i in range(NROWS):
                self.horizontalLine(screen, i*TILEHEIGHT)
            for i in range(NCOLS):
                self.verticalLine(screen, i*TILEWIDTH)
