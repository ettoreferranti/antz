#!/usr/bin/env python

import logging

class Ant:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.environment = environment

    def __moveHelper__(self, position, delta):
        newValue = position + delta
        if newValue >= self.environment.size:
            return self.environment.size - 1
        elif newValue < 0:
            return 0
        else:
            return newValue

    def move(self, deltaX, deltaY):
        newX = self.__moveHelper__(self.x, deltaX)
        newY = self.__moveHelper__(self.y, deltaY)

        if self.environment.grid[newX][newY].ant is None:
            self.environment.grid[self.x][self.y].ant = None
            self.environment.grid[self.x][self.y].increasePheromone()
            self.environment.grid[newX][newY].ant = self
            self.x = newX
            self.y = newY
            logging.info("Ant moved by ({0},{1}) to ({2},{3})".format(deltaX, deltaY, self.x, self.y))
        else:
            logging.warning("Ant cannot move to ({0},{1}) because another ant is already there".format(newX, newY))
        
class Cell:
    def __init__(self, pheromone = 0, ant = None):
        self.pheromone = pheromone
        self.ant = ant

    def increasePheromone(self):
        self.pheromone += 1

    def decreasePheromone(self):
        if self.pheromone > 0:
            self.pheromone -= 1

    def __str__(self):
        if self.ant is None:
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

    def spawnAnt(self, x, y):
        if self.grid[x][y].ant is None:
            newAnt = Ant(x, y, self)
            self.grid[x][y].ant = newAnt
            logging.info("Ant created in ({0},{1})".format(x,y))
            return newAnt
        else:
            logging.warning("Cannot create ant in ({0},{1}), there's already an ant there".format(x,y))
            return None


    def print(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.grid[x][y], end=" ")
            print()
        print()

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Application started")
    env = Environment(10)
    env.print()
    newAnt = env.spawnAnt(0,0)
    env.print()
    for i in range(10):
        newAnt.move(1,1)
        env.print()
        print("\n")

if __name__ == "__main__":
    main()

    