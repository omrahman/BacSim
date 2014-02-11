# Omar Rahman, andrewid: omarr

# update and change direction methods were adapted and modified from a tutorial
# by Eli Bendersky at http://eli.thegreenplace.net/2008/12/13/writing-a-game-
# in-python-with-pygame-part-i/
# Images for the bacteria were used and modified from this tutorial as well

from random import randint, choice
from math import sin, cos, radians, acos
import pygame
from pygame.sprite import Sprite
from vec2d import vec2d

class Bacterium(Sprite):
    def __init__(self, petriDish, imageFilename, initPosition, initDirection):
        Sprite.__init__(self)
        self.decayRate = 0
        self.petriDishScreen = petriDish
        self.changeDirectionCounter = 0
        self.initImage = pygame.image.load(imageFilename).convert_alpha()
        self.image = self.initImage
        self.rect = self.image.get_bounding_rect()
        # self.pos and self.direction are vec2d objects
        self.pos = vec2d(initPosition) 
        self.direction = vec2d(initDirection).normalized()

    def changeDirection(self, timePassed, otherList):
        # Turn a random degree between -45 and 45 degrees every
        # .5 to 1.0 seconds. This is the default movement.
        self.changeDirectionCounter += timePassed
        if self.changeDirectionCounter > randint(500, 1000):
            self.direction.rotate(randint(-45, 45))
            self.changeDirectionCounter = 0
           
    def update(self, timePassed, otherList):
        self.speed = self.walkSpeed
        # updates the bacterium's position and direction
        self.changeDirection(timePassed, otherList)
        # rotates the image to the appropriate direction
        self.image = pygame.transform.rotate(self.initImage,
                                             -self.direction.angle)
        # change in position is calculated and created as a vec2d object
        displacement = vec2d(self.direction.x * self.speed * timePassed,
                             self.direction.y * self.speed * timePassed)
        self.pos += displacement
        self.imageWidth, self.imageHeight = self.image.get_size()
        self.boundingRect = self.petriDishScreen.get_rect().inflate(
                        -self.imageWidth, -self.imageHeight)
        self.checkBounce()
        self.rect = self.image.get_rect().move(
            (self.pos.x - self.imageWidth / 2), 
            (self.pos.y - self.imageHeight / 2))
        
    def checkBounce(self):
        # bouncing against walls
        if (self.pos.x < self.boundingRect.left):
            self.pos.x = self.boundingRect.left
            self.direction.x *= -1
        elif (self.pos.y < self.boundingRect.top):
            self.pos.y = self.boundingRect.top
            self.direction.y *= -1
        elif (self.pos.x > self.boundingRect.right):
            self.pos.x = self.boundingRect.right
            self.direction.x *= -1
        elif (self.pos.y > self.boundingRect.bottom):
            self.pos.y = self.boundingRect.bottom
            self.direction.y *= -1
        
    def eatGrass(self):
        self.energy += 1

    def divide(self, petriDishScreen, image, Bacterium, Group):
        if (self.energy >= self.dividingEnergy):
            # picks which trait to favor
            mutationChoice = choice(('speed', 'vision'))
            # if speed is favored, increase speed and decrease vision
            if (mutationChoice == 'speed'):
                childWalkSpeed = (self.walkSpeed * 100 +
                                  randint(0, self.speedMutationFactor)) * .01
                childRadiusOfVision = (self.radiusOfVision -
                                       randint(0, self.visionMutationFactor))
            # if vision is favored, increase vision and decrease speed
            elif (mutationChoice == 'vision'):
                childWalkSpeed = (self.walkSpeed * 100 -
                                  randint(0, self.speedMutationFactor)) * .01
                childRadiusOfVision = (self.radiusOfVision +
                                       randint(0, self.visionMutationFactor))
            # if something went wrong somehow, don't change anything
            else:
                childWalkSpeed = self.walkSpeed
                childRadiusOfVision = self.radiusOfVision
            # add the child bacterium very close to the parent
            Group.add(Bacterium(self.petriDishScreen, image,
                                (self.pos.x + 3, self.pos.y + 3),
                                (choice([-1, 1]), choice([-1, 1])),
                                childWalkSpeed, childRadiusOfVision))
            # reset the parent's energy
            self.energy = self.initEnergy

    def decay(self, timePassed):
        # decay timer, decreases energy by the decayRate every second
        self.decayCounter += timePassed
        if self.decayCounter > 1000:
            self.energy -= self.decayRate
            self.decayCounter = 0
            
class Herbivore(Bacterium):
    def __init__(self, petriDishScreen, imageFilename, initPosition,
                 initDirection, walkSpeed=.18, radiusOfVision = 95):
        super(Herbivore, self).__init__(petriDishScreen, imageFilename,
                                        initPosition, initDirection)
        self.decayCounter = 0
        self.walkSpeed = walkSpeed
        self.chaseSpeed = self.walkSpeed + .12
        self.speed = self.walkSpeed
        self.initEnergy = 20
        self.energy = self.initEnergy
        self.dividingEnergy = 30
        self.decayRate = 3
        self.radiusOfVision = radiusOfVision
        self.speedMutationFactor = 1
        self.visionMutationFactor = 5

    def changeDirection(self, timePassed, predators):
        super(Herbivore, self).changeDirection(timePassed, None)
        minDistance = 10000
        for predator in predators:
            # checks for every predator in the petri dish and flees from
            # the closest one it sees
            distanceBetween = self.pos.get_distance(predator.pos)
            if ((distanceBetween < self.radiusOfVision) and
               (distanceBetween < minDistance)):
                #changes its direction to the opposite of the predator's
                self.direction = -(predator.pos - self.pos)
                # initiates chase mode
                self.speed = self.chaseSpeed    
                minDistance = distanceBetween         
        self.direction = self.direction.normalized()
    
class Predator(Bacterium):
    def __init__(self, petriDishScreen, imageFilename, initPosition,
                 initDirection, walkSpeed=.12, radiusOfVision = 100):
        super(Predator, self).__init__(petriDishScreen, imageFilename,
                                       initPosition, initDirection)
        self.decayCounter = 0
        self.walkSpeed = walkSpeed
        self.speed = self.walkSpeed
        self.chaseSpeed = self.walkSpeed + .27
        self.initEnergy = 30
        self.energy = self.initEnergy
        self.dividingEnergy = 55
        self.decayRate = 4
        self.radiusOfVision = radiusOfVision
        self.speedMutationFactor = 4
        self.visionMutationFactor = 4
        self.isTracking = False

    def changeDirection(self, timePassed, prey):
        # isTracking allows the addition of a refractory period after
        # a predator eats. isTracking is set in the bacteriaEvents of
        # the PetriDish class
        super(Predator, self).changeDirection(timePassed, None) 
        if (self.isTracking == True):
            minDistance = 10000
            for victim in prey:
                # finds the closest herbivore within radius of vision
                distanceBetween = self.pos.get_distance(victim.pos)
                if ((distanceBetween < self.radiusOfVision) and
                    (distanceBetween < minDistance)):
                    #changes direction to the direction of the victim/target
                    self.direction = victim.pos - self.pos
                    # initiates chase mode
                    self.speed = self.chaseSpeed
                    minDistance = distanceBetween
            self.direction = self.direction.normalized()

class Omnivore(Bacterium):
    def __init__(self, petriDishScreen, imageFilename, initPosition,
                 initDirection, walkSpeed=.12, radiusOfVision = 100):
        super(Omnivore, self).__init__(petriDishScreen, imageFilename,
                                       initPosition, initDirection)
        self.decayCounter = 0
        self.walkSpeed = walkSpeed
        self.speed = self.walkSpeed
        self.chaseSpeed = self.walkSpeed + .12
        self.initEnergy = 20
        self.energy = self.initEnergy
        self.dividingEnergy = 120
        self.decayRate = 5
        self.radiusOfVision = radiusOfVision
        self.speedMutationFactor = 1
        self.visionMutationFactor = 3

    def changeDirection(self, timePassed, predators):
        super(Omnivore, self).changeDirection(timePassed, None)
        minDistance = 10000
        for predator in predators:
            # checks for every predator in the petri dish and flees from
            # the closest one it sees
            distanceBetween = self.pos.get_distance(predator.pos)
            if ((distanceBetween < self.radiusOfVision) and
               (distanceBetween < minDistance)):
                #changes its direction to the opposite of the predator's
                self.direction = -(predator.pos - self.pos)
                # initiates chase mode
                self.speed = self.chaseSpeed    
                minDistance = distanceBetween         
        self.direction = self.direction.normalized()
