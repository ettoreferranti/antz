#!/usr/bin/env python

import logging
import uuid

class Ant:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.environment = environment
        self.id = uuid.uuid4()

    def __moveHelper__(self, position, delta):
        newValue = position + delta
        if newValue >= self.environment.size:
            return self.environment.size - 2
        elif newValue < 0:
            return 1
        else:
            return newValue

    def move(self, deltaX, deltaY):
        newX = self.__moveHelper__(self.x, deltaX)
        newY = self.__moveHelper__(self.y, deltaY)
        self.environment.grid[self.x][self.y].removeAnt(self.id)
        self.environment.grid[self.x][self.y].increasePheromone()
        self.environment.grid[newX][newY].addAnt(self)
        self.x = newX
        self.y = newY
        logging.info("Ant moved by ({0},{1}) to ({2},{3})".format(deltaX, deltaY, self.x, self.y))
        
class Cell:
    def __init__(self, pheromone = 0, ant = None):
        self.nest = False
        self.food = 0
        self.pheromone = pheromone
        self.ants = {}

    def increasePheromone(self):
        self.pheromone += 1

    def decreasePheromone(self):
        if self.pheromone > 0:
            self.pheromone -= 1

    def increaseFood(self):
        self.food += 1

    def decreaseFood(self):
        if self.food > 0:
            self.food -= 1

    def addAnt(self, ant):
        self.ants[ant.id] = ant

    def removeAnt(self, id):
        self.ants.pop(id)
    
    def __str__(self):
        if len(self.ants) == 0:
            return str(self.pheromone)
        else:
            return "A"
        
class Environment:
    def __init__(self, size=100):
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y] = Cell()
        self.ants = {}

    def spawnAnt(self, x, y):
        newAnt = Ant(x, y, self)
        self.grid[x][y].addAnt(newAnt)
        self.ants[newAnt.id] = newAnt
        logging.info("Ant {0} created in ({1},{2})".format(newAnt.id, x,y))
        return newAnt

    def killAnt(self, ant):
        self.ants.pop(ant.id)
        self.grid[ant.x][ant.y].removeAnt(ant.id)

    def print(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.grid[x][y], end=" ")
            print()
        print()