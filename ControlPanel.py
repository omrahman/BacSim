# Omar Rahman, andrewid: omarr

import pygame
import sys, os
from pygame.sprite import Sprite
from pygame.rect import Rect
from DataPanel import DataPanel, DataVariable

class ControlPanel(object):
    def __init__(self, appScreen, left, top, width, height):
        self.controlPanelSurface = appScreen.subsurface(
            pygame.Rect((left, top), (width, height)))
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.herbivoreButton = Button('Herbivore_Button.png',
                                      'Herbivore_Depressed.png', (0, 0))
        bWidth = self.herbivoreButton.rect.width
        bHeight = self.herbivoreButton.rect.height
        self.predatorButton = Button('Predator_Button.png',
                                     'Predator_Depressed.png',
                                     (bWidth, 0))
        self.omnivoreButton = Button('Omnivore_Button.png',
                                     'Omnivore_Depressed.png',
                                     (bWidth * 2, 0))
        self.resetButton = Button('Reset_Button.png',
                                  'Reset_Button.png', (bWidth * 5, 0))
        self.quitButton = Button('Quit_Button.png',
                                 'Quit_Button.png', (bWidth * 6, 0))
        self.rect = Rect(left, top, width, height)
        
    def draw(self):
        # draws all the buttons to the control panel
        self.herbivoreButton.draw(self.controlPanelSurface)
        self.predatorButton.draw(self.controlPanelSurface)
        self.omnivoreButton.draw(self.controlPanelSurface)
        self.resetButton.draw(self.controlPanelSurface)
        self.quitButton.draw(self.controlPanelSurface)
        
    def resetAllButtons(self):
        self.herbivoreButton.reset()
        self.predatorButton.reset()
        self.omnivoreButton.reset()
        self.resetButton.reset()
        self.quitButton.reset()
               
class Button(Sprite):
    # button class that takes in an image with a button pressed handler and
    # draw methods
    def __init__(self, buttonImage, dbuttonImage, (top, left)):
        pygame.sprite.Sprite.__init__(self)
        # Load unpressed button image and convert
        self.image = pygame.image.load(buttonImage).convert_alpha()
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (top, left)
        self.colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(self.colorkey)
        # Load depressed button image and convert
        self.dimage = pygame.image.load(dbuttonImage).convert_alpha()
        self.drect = self.dimage.get_bounding_rect()
        self.drect.topleft = (top, left)
        self.dcolorkey = self.dimage.get_at((0,0))
        self.dimage.set_colorkey(self.dcolorkey)
        self.buttonDepressed = False

    def buttonPressed(self, mouse, x=0, y=0):
        # x and y are offsets; if there are none, assume none exist
        left = x + self.rect.left
        top = y + self.rect.top
        width = self.rect.width
        height = self.rect.height
        self.newRect = Rect(left, top, width, height)
        # checks if the mouse point collides with the button's rect 
        if (self.newRect.collidepoint(mouse) == True):
            self.buttonDepressed = not(self.buttonDepressed)
            return True
        else:
            return False
        
    def reset(self):
        self.buttonDepressed = False
        
    def draw(self, screen):
        # draws the button onto the given screen given the coordinates of the
        # top left of the button
        if self.buttonDepressed == False:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.dimage, self.rect.topleft)