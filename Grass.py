# Omar Rahman, andrewid: omarr

import pygame
from random import randint, choice
from pygame.sprite import Sprite

class Grass(Sprite):
    def __init__(self, cellSize, left, top, energy=5):
        Sprite.__init__(self)
        self.cellSize = cellSize
        self.grass = pygame.Surface((self.cellSize, self.cellSize))
        self.maxEnergy = 5
        self.energy = energy
        self.speed = 2000
        self.image = pygame.Surface((cellSize,cellSize))
        self.image.fill((0,175,0))
        self.rect = pygame.Rect(left, top, cellSize, cellSize)
 
    def grow(self):
        # grass grow method
        if (self.energy < self.maxEnergy):
            self.energy += 1
        
    def beEaten(self):
        # grass be eaten method
        if (self.energy > 0):
            self.energy -= 1
        
    def setEnergy(self, energy):
        self.energy = energy
        
    def getEnergy(self):
        return self.energy

    def setGrassAlpha(self):
        # sets the shade of green of the grass based on its energy level
        self.image.fill((0,175,0))
        if self.energy == 0:
            self.image.set_alpha(0)
        elif self.energy == 1:
            self.image.set_alpha(50)
        elif self.energy == 2:
            self.image.set_alpha(100)
        elif self.energy == 3:
            self.image.set_alpha(150)
        elif self.energy == 4:
            self.image.set_alpha(200)
        elif self.energy == 5:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def setBoundaries(self, row, col, cellSize):
        # sets the boundaries of the particular grass object on the screen
        self.left = col * cellSize
        self.top = row * cellSize
        self.right = self.left + cellSize
        self.bottom = self.top + cellSize
        
    def getLeftBound(self):
        return self.left
    
    def getTopBound(self):
        return self.top
    
    def getRightBound(self):
        return self.right
    
    def getBottomBound(self):
        return self.bottom
    
    counter = 0
    
    def update(self, time_passed):
        # updates the grass every self.speed milliseconds
        self.setGrassAlpha()
        self.counter += time_passed
        if self.counter > self.speed:
            self.grow()
            self.counter = 0
