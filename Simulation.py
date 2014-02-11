# Omar Rahman, andrewid: omarr

import os, sys
import pygame
from PetriDish import PetriDish
from ControlPanel import ControlPanel
from DataPanel import DataPanel
from Graph import Graph
from pgu import text, gui as pgui

class Simulation(object):
    def __init__(self, petriDishLength=720, cellSize=40,
                 appWidth=1200, appHeight=810):
        self.appWidth = appWidth
        self.appHeight = appHeight
        self.petriDishWidth = petriDishLength
        self.petriDishHeight = petriDishLength
        self.cellSize = cellSize
        self.backgroundColor = (255, 255, 255)
        self.selectedBacterium = "None"
        self.appScreen = pygame.display.set_mode((self.appWidth,
                                               self.appHeight), 0, 32)
        self.petriDish = PetriDish(self.appScreen, 0, 0, self.petriDishWidth,
                                   self.petriDishHeight, self.cellSize)
        self.controlPanel = ControlPanel(self.appScreen, 
                                         0, self.petriDishHeight,
                                         self.appWidth,
                                         self.appHeight-self.petriDishHeight)
        self.dataPanel = DataPanel(self.appScreen, self.petriDish,
                                   self.petriDishWidth, 0,
                                   self.appWidth - self.petriDishHeight,
                                   self.petriDishHeight)
        self.plot = Graph(0, 0, 400, 400)
        self.clock = pygame.time.Clock()
        self.selectedBacterium = None
               
    def handleEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                mouse = pygame.mouse.get_pos()
                if (event.button == 1):
                    # check if click is in petri dish
                    if self.petriDish.rect.collidepoint(mouse):
                        # add selectedBacterium to the petri dish
                        self.petriDish.addBacterium(event,
                                                    self.selectedBacterium)
                    # check if mouse click was in the control panel
                    elif self.controlPanel.rect.collidepoint(mouse):
                        self.controlPanelEvent(mouse)
            # Keyboard events
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_r):
                    self.petriDish.reset()
                elif (event.key == pygame.K_d):
                    self.petriDish.drawData()
            # gui event
            self.gui.event(event)

    def controlPanelEvent(self, mouse):
        # get the offset of the control panel in relation to the appScreen
        # to pass into the buttonPressed method of the Button class
        x = self.controlPanel.controlPanelSurface.get_abs_offset()[0]
        y = self.controlPanel.controlPanelSurface.get_abs_offset()[1]
        if self.controlPanel.herbivoreButton.buttonPressed(mouse, x, y):
            self.selectedBacterium = 'Herbivore'
            self.controlPanel.resetAllButtons()
            self.controlPanel.herbivoreButton.buttonDepressed = True
        elif self.controlPanel.predatorButton.buttonPressed(mouse, x, y):
            self.selectedBacterium = 'Predator'
            self.controlPanel.resetAllButtons()
            self.controlPanel.predatorButton.buttonDepressed = True
        elif self.controlPanel.omnivoreButton.buttonPressed(mouse, x, y):
            self.selectedBacterium = 'Omnivore'
            self.controlPanel.resetAllButtons()
            self.controlPanel.omnivoreButton.buttonDepressed = True
        elif self.controlPanel.resetButton.buttonPressed(mouse, x, y):
            self.petriDish.reset()
        elif self.controlPanel.quitButton.buttonPressed(mouse, x, y):
            pygame.quit()
            sys.exit()
            
    def makeGUI(self, layout):
        # creates gui and adds a slider and label for adjusting grass growth
        grassLabel = pgui.Label("Grass Rate Slider", font=self.font,
                                color = (0,0,0))
        layout.add(grassLabel, 735, 618)
        grassSlider = pgui.HSlider(value=3000,min=0,max=6000,size=32,
                                   width=200,height=16)
        grassSlider.connect(pgui.CHANGE, self.petriDish.setGrassSpeed,
                            grassSlider)
        layout.add(grassSlider, 735, 600)
    
    def run(self):
        pygame.init()
        pygame.display.set_caption('Bacteria Simulator')
        self.gui = pgui.App()
        self.font = pygame.font.SysFont("default", 20)
        layout = pgui.Container()
        self.makeGUI(layout)
        self.gui.init(layout)
        # Main game loop    
        while (True):
            # Limit frame speed to 50 FPS
            self.timePassed = self.clock.tick(50)
            # Handle both mouse and key events
            self.handleEvents()
            # Redraw the background, grass, and bacteria
            self.appScreen.fill(self.backgroundColor)
            self.petriDish.draw(self.timePassed)
            # self.petriDish.drawData(self.timePassed)
            self.controlPanel.controlPanelSurface.fill((0,0,0))
            self.controlPanel.draw()
            self.dataPanel.dataPanelSurface.fill((128,128,128))
            self.dataPanel.updatePlots(self.timePassed)
            self.dataPanel.blitAllData()
            self.gui.paint(self.appScreen)
            # Display
            pygame.display.flip()

##############################################################################
# Debugging/Test functions
    def printPopulations(self, timePassed):
        self.testCounter += timePassed
        if self.testCounter > 2000:
            print "Herbivores: ", self.Herbivores
            print "Predators: ", self.Predators
            print "Omnivores: ", self.Omnivores
            self.testCounter = 0
            
app = Simulation()
app.run()
