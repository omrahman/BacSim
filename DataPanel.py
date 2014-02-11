# Omar Rahman, andrewid: omarr

import pygame
import sys, os
from pygame.sprite import Sprite
from pygame.font import Font
from Graph import Graph

class DataPanel(object):
    def __init__(self, appScreen, petriDish, left, top, width, height):
        self.dataPanelSurface = appScreen.subsurface(pygame.Rect((left, top),
                                                             (width, height)))
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.petriDish = petriDish
        self.herbPlot = Graph(left, 100, width, height-100)
        self.herbPlot.setColor((255,160,0))
        self.predPlot = Graph(left, 100, width, height-100)
        self.predPlot.setColor((255,40,0))
        self.omniPlot = Graph(left, 100, width, height-100)
        self.omniPlot.setColor((0,0,255))
        self.grassPlot = Graph(left, 100, width, height-100)
        self.grassPlot.setColor((0,255,0))
        self.time = 0
        
    def updatePlots(self, timePassed):
        self.time += timePassed
        # updates all plots
        self.herbPlot.updateData(self.petriDish.getHerbivoreCount(),
                                            timePassed)
        self.herbPlot.plotData(self.dataPanelSurface)
        
        self.predPlot.updateData(self.petriDish.getPredatorCount(),
                                            timePassed)
        self.predPlot.plotData(self.dataPanelSurface)
        self.omniPlot.updateData(self.petriDish.getOmnivoreCount(),
                                            timePassed)
        self.omniPlot.plotData(self.dataPanelSurface)
        self.grassPlot.updateData(self.petriDish.getGrassCount() * 200,
                                            timePassed)
        self.grassPlot.plotData(self.dataPanelSurface)
        
    def blitAllData(self):
        # draws all the data variables to the data panel
        DataVariable('Herbivores', self.petriDish.getHerbivoreCount(),
                    self.dataPanelSurface, 20, 10, 100, 50).draw()
        DataVariable('Predators', self.petriDish.getPredatorCount(),
                    self.dataPanelSurface, 20, 35, 100, 50).draw()
        DataVariable('Omnivores', self.petriDish.getOmnivoreCount(),
                     self.dataPanelSurface, 20, 60, 100, 50).draw()
        DataVariable('Grass', self.petriDish.getGrassCount(),
                     self.dataPanelSurface, 20, 85, 100, 50).draw()
        DataVariable('hAvgSpeed', self.petriDish.getAvgHSpeed(),
                     self.dataPanelSurface, 20, 110, 100, 50).draw()
        DataVariable('hAvgFleeSpeed', self.petriDish.getAvgHerbFleeSpeed(),
                     self.dataPanelSurface, 20, 135, 100, 50).draw()
        DataVariable('hAvgVision', self.petriDish.getAvgHVision(),
                     self.dataPanelSurface, 20, 160, 100, 50).draw()
        DataVariable('pAvgSpeed', self.petriDish.getAvgPSpeed(),
                     self.dataPanelSurface, 20, 185, 100, 50).draw()
        DataVariable('pAvgChaseSpeed', self.petriDish.getAvgPredChaseSpeed(),
                     self.dataPanelSurface, 20, 210, 100, 50).draw()
        DataVariable('pAvgVision', self.petriDish.getAvgPredVision(),
                     self.dataPanelSurface, 20, 235, 100, 50).draw()
        DataVariable('oAvgSpeed', self.petriDish.getAvgOSpeed(),
                     self.dataPanelSurface, 20, 260, 100, 50).draw()
        DataVariable('oAvgFleeSpeed', self.petriDish.getAvgOmniFleeSpeed(),
                     self.dataPanelSurface, 20, 285, 100, 50).draw()
        DataVariable('oAvgVision', self.petriDish.getAvgOmniVision(),
                     self.dataPanelSurface, 20, 310, 100, 50).draw()
   
class DataVariable(object):
    def __init__(self, name, data, surface, left, top, width, height):
        self.name = name
        self.data = data
        self.surface = surface
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.textpos = pygame.Rect(self.left, self.top, self.width,
                                   self.height)
        self.createText()
        
    def createText(self):
        # creates the text string to be displayed
        pygame.font.init()
        self.data = str(self.data)
        string = "%s: %s" % (self.name, self.data)
        font = pygame.font.Font(None, 36)
        self.text = font.render(string, 0, (0,0,0))
        
    def draw(self):
        # blits the text string onto the given screen
        self.surface.blit(self.text, self.textpos)
      