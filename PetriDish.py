# Omar Rahman, andrewid: omarr

import pygame
from decimal import *
from pygame.rect import Rect
from random import randint, choice
from Bacteria import Bacterium, Herbivore, Predator, Omnivore
from Grass import Grass
from Graph import Graph

class PetriDish:
    def __init__(self, appScreen, left, top, width, height, cellSize):
        """Initialize variables related to the petri dish."""
        self.petriDishScreen = appScreen.subsurface(
            pygame.Rect((left, top), (width, height)))
        self.cellSize = cellSize
        self.rows = height / cellSize
        self.cols = width / cellSize
        self.petriDish = [([None]*self.cols) for row in xrange(self.rows)]
        self.Grass = pygame.sprite.Group()
        self.createPetriDish()
        self.herbivoreImage = 'orangecreep.png'
        self.predatorImage = 'redcreep.png'
        self.omnivoreImage = 'darkbluebacterium.png'
        self.Herbivores = pygame.sprite.Group()
        self.Predators = pygame.sprite.Group()
        self.Omnivores = pygame.sprite.Group()
        self.rect = Rect(left, top, width, height)
        self.predatorEatCounter = 0
        self.currentBacterium = None

    def createPetriDish(self):
        """Creates the petri dish as a 2d list of Grass objects."""
        self.totalGrass = 0
        self.grassCount = 0
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                left = col * self.cellSize
                top  = row * self.cellSize
                self.petriDish[row][col] = Grass(self.cellSize, left, top)
                self.petriDish[row][col].setBoundaries(row, col, self.cellSize)
                self.Grass.add(self.petriDish[row][col])
        
    def draw(self, timePassed):
        """Updates and draws all events of the petri dish."""
        self.bacteriaEvents(timePassed)
        self.Grass.update(timePassed)
        self.Grass.draw(self.petriDishScreen)
        self.Herbivores.update(timePassed, self.Predators)
        self.Herbivores.draw(self.petriDishScreen)
        self.Predators.update(timePassed, self.Herbivores)
        self.Predators.draw(self.petriDishScreen)
        self.Omnivores.update(timePassed, self.Predators)
        self.Omnivores.draw(self.petriDishScreen)

    def reset(self):
        """Reset the petri dish by emptying the groups
        and creating a new petri dish."""
        self.Herbivores.empty()
        self.Predators.empty()
        self.Omnivores.empty()
        self.createPetriDish()

    def addBacterium(self, event, selectedBacterium):
        """Adds a new bacterium at event coordinates (a mouseclick)."""
        self.selectedBacterium = selectedBacterium
        if (selectedBacterium == 'Herbivore'):
            newHerbivore = Herbivore(self.petriDishScreen, self.herbivoreImage,
                            (event.pos[0], event.pos[1]),
                            (choice([-1, 1]), choice([-1, 1])))
            self.Herbivores.add(newHerbivore)
            
        elif (selectedBacterium == 'Predator'):
            newPredator = Predator(self.petriDishScreen, self.predatorImage,
                (event.pos[0], event.pos[1]),
                (choice([-1, 1]), choice([-1, 1])))
            self.Predators.add(newPredator)
            
        elif (selectedBacterium == 'Omnivore'):
            newOmnivore = Omnivore(self.petriDishScreen, self.omnivoreImage,
                (event.pos[0], event.pos[1]),
                (choice([-1, 1]), choice([-1, 1])))
            self.Omnivores.add(newOmnivore)
            
        else:
            print "No bacterium selected"

    def bacteriaEvents(self, timePassed):
        """Handles all eating, decaying, and dividing events."""
        self.predatorEvents(timePassed)
        self.herbivoreEvents(timePassed)
        self.omnivoreEvents(timePassed)
          
    def predatorEvents(self, timePassed):
        # Predator events
        for predator in self.Predators:
            # Predator eating Herbivore
            self.predatorEatCounter += timePassed
            # predator latency in eating, wait 500ms after eating to
            # eat again
            if (self.predatorEatCounter > 500):
                predator.isTracking = True
                for herbivore in pygame.sprite.spritecollide(
                    predator, self.Herbivores, True):
                    predator.energy += herbivore.energy / 3 * 2
                    self.predatorEatCounter = 0
            else:
                predator.isTracking = False
            # Predator eating Omnivore
            for omnivore in pygame.sprite.spritecollide(
                predator, self.Omnivores, True):  
                predator.energy += omnivore.energy / 3 * 2
            # Predator decay
            predator.decay(timePassed)
            # Predator death
            if predator.energy <= 0:
                self.Predators.remove(predator)
            # Predator division
            predator.divide(self.petriDishScreen, self.predatorImage,
                            Predator, self.Predators)
            
    def herbivoreEvents(self, timePassed):
        # Herbivore events
        for herbivore in self.Herbivores:
            for grass in pygame.sprite.spritecollide(
                herbivore, self.Grass, False):
                if grass.getEnergy() > 0: herbivore.energy += 1
                grass.beEaten()
                grass.counter = 0
            # Herbivore division
            herbivore.divide(self.petriDishScreen, self.herbivoreImage,
                             Herbivore, self.Herbivores)
            # Herbivore decay
            herbivore.decay(timePassed)
            # Herbivore death
            if herbivore.energy <= 0:
                self.Herbivores.remove(herbivore)
                
    def omnivoreEvents(self, timePassed):
        # Omnivore events
        for omnivore in self.Omnivores:
            for grass in pygame.sprite.spritecollide(omnivore, self.Grass,
                                                     False):
                if grass.getEnergy() > 0: omnivore.energy += 1
                grass.beEaten()
                grass.counter = 0
            for herbivore in pygame.sprite.spritecollide(omnivore,
                                                         self.Herbivores,
                                                         True):
                omnivore.energy += herbivore.energy / 3 * 2
            omnivore.divide(self.petriDishScreen, self.omnivoreImage,
                            Omnivore, self.Omnivores)
            omnivore.decay(timePassed)
            if omnivore.energy <= 0:
                self.Omnivores.remove(omnivore)
        
    def getHerbivoreCount(self):
        return len(self.Herbivores)
    
    def getPredatorCount(self):
        return len(self.Predators)
    
    def getOmnivoreCount(self):
        return len(self.Omnivores)
    
    def setGrassSpeed(self, value):
        # Sets each grass object's speed; subtraction used so that higher
        # numbers are faster and lower numbers are slower 
        for grass in self.Grass:
            grass.speed = 6000 - value.value
            
    def getAvgHSpeed(self):
        # returns the average herbivore speed 
        getcontext().prec = 3
        speedSum = 0
        for herbivore in self.Herbivores:
            speedSum += herbivore.walkSpeed
        if self.getHerbivoreCount() > 0:
            return Decimal(speedSum) / self.getHerbivoreCount()
        else:
            return 0
        
    def getAvgHVision(self):
        # returns the average radius of vision of all the herbivores
        getcontext().prec = 3
        visionSum = 0
        for herbivore in self.Herbivores:
            visionSum += herbivore.radiusOfVision
        if self.getHerbivoreCount() > 0:
            return Decimal(visionSum) / self.getHerbivoreCount()
        else:
            return 0
        
    def getAvgPredVision(self):
        # returns the average radius of vision of all the predators
        getcontext().prec = 3
        visionSum = 0
        for predator in self.Predators:
            visionSum += predator.radiusOfVision
        if self.getPredatorCount() > 0:
            return Decimal(visionSum) / self.getPredatorCount()
        else:
            return 0
        
    def getAvgOmniVision(self):
        # returns the average radius of vision of all the omnivores
        getcontext().prec = 3
        visionSum = 0
        for omnivore in self.Omnivores:
            visionSum += omnivore.radiusOfVision
        if self.getOmnivoreCount() > 0:
            return Decimal(visionSum) / self.getOmnivoreCount()
        else:
            return 0
        
    def getAvgPSpeed(self):
        # returns the average speed of all the predators
        getcontext().prec = 3
        speedSum = 0
        for predator in self.Predators:
            speedSum += predator.walkSpeed
        if self.getPredatorCount() > 0:
            return Decimal(speedSum) / self.getPredatorCount()
        else:
            return 0
        
    def getAvgOSpeed(self):
        # returns the average speed of all the omnivores
        getcontext().prec = 3
        speedSum = 0
        for omnivore in self.Omnivores:
            speedSum += omnivore.walkSpeed
        if self.getOmnivoreCount() > 0:
            return Decimal(speedSum) / self.getOmnivoreCount()
        else:
            return 0
    
    def getAvgPredChaseSpeed(self):
        # returns the averages chasing speed of all the predators
        getcontext().prec = 3
        speedSum = 0
        for predator in self.Predators:
            speedSum += predator.chaseSpeed
        if self.getPredatorCount() > 0:
            return Decimal(speedSum) / self.getPredatorCount()
        else:
            return 0
        
    def getAvgHerbFleeSpeed(self):
        # returns the average fleeing speed of all the herbivores
        getcontext().prec = 3
        speedSum = 0
        for herbivore in self.Herbivores:
            speedSum += herbivore.chaseSpeed
        if self.getHerbivoreCount() > 0:
            return Decimal(speedSum) / self.getHerbivoreCount()
        else:
            return 0
        
    def getAvgOmniFleeSpeed(self):
        # returns the average fleeing speed of all the omnivores
        getcontext().prec = 3
        speedSum = 0
        for omnivore in self.Omnivores:
            speedSum += omnivore.chaseSpeed
        if self.getOmnivoreCount() > 0:
            return Decimal(speedSum) / self.getOmnivoreCount()
        else:
            return 0
        
    def getGrassCount(self):
        # returns the percentage of grass remaining in the petri dish
        getcontext().prec = 3
        self.totalGrass = 0
        self.grassCount = 0
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                self.totalGrass += self.petriDish[row][col].maxEnergy
                self.grassCount += self.petriDish[row][col].getEnergy()
        return (Decimal(self.grassCount) / self.totalGrass)
    
##############################################################################
# Debugging / Test functions

    def drawData(self):
        """Prints the data in the command line"""
        self.hCount = len(self.Herbivores)
        self.pCount = len(self.Predators)
        self.oCount = len(self.Omnivores)
        print "Herbivores: ", self.hCount
        print "Predators: ", self.pCount
        print "Omnivores: ", self.oCount