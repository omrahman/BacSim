# Omar Rahman, andrewid: omarr

import pygame
from pygame import Surface
from random import randint

class Graph(Surface):
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.data = []
        self.yRange = height
        self.xRange = width
        self.gSpeed = 250
        self.counter = 0
        
    def setColor(self, (r,g,b)):
        # sets the color of the plot
        self.color = (r,g,b)
        
    def setGraphSpeed(self, speed):
        # sets the update speed in milliseconds
        self.gSpeed = speed
        
    def updateData(self, value, time_passed):
        # updates the data every self.speed milliseconds
        self.counter += time_passed
        if self.counter > self.gSpeed:
            self.data.append(value)
            # if the length of the data list exceeds the width of the graph,
            # pop off the first data value; this is the key to the scrolling
            # of the graph
            if (len(self.data) >= self.width-self.width / 5):
                self.data.pop(0)
            self.counter = 0
    
    def createXList(self):
        # creates the list of x data values based on the length of the data
        # list
        xAxisSpacing = int(float(self.width) / self.xRange)
        self.xList = []
        for xValue in xrange(len(self.data)):
            self.xList += [xValue * xAxisSpacing]
            
    def createYList(self):
        # creates a list of y data values adjusted for the height of the
        # graph based on the length of the data list
        yAxisSpacing = int(float(self.height) / self.yRange)
        self.yList = []
        for yValue in self.data:
            self.yList += [(self.height - yValue)]
                
    def plotData(self, screen):
        self.createXList()
        self.createYList()
        # zip the x's and y's together to form a list of points
        self.points = zip(self.xList, self.yList)
        for i in xrange(len(self.points) - 1):
            # connect all the points with lines of the chosen color
            pygame.draw.line(screen, self.color, self.points[i],
                             self.points[i+1], 3)
        # draws the base line of the graph
        pygame.draw.line(screen, (0,0,0), (0,620), (500,620), 3)
        