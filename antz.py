#!/usr/bin/env python

import logging
import tkinter as tk
from threading import Thread
import time
from PIL import Image, ImageTk

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
    def __init__(self, size=100, graphical=None):
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.graphical = graphical
        image = Image.open("Ant.png").resize((20,20))
        self.antImage = ImageTk.PhotoImage(image)
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y] = Cell()

    def refresh(self):
        if self.graphical is not None:
            logging.info("Refreshing GUI")
            for x in range(self.size):
                for y in range(self.size):
                    if self.grid[x][y].ant is not None:
                        self.graphical[x][y].config(image = self.antImage)
                    else:
                        self.graphical[x][y].config(text = str(self.grid[x][y]))

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

def environmentInit():
    logging.basicConfig(level=logging.INFO)
    logging.info("Environment initialising")
    env = Environment(10)
    env.print()
    newAnt = env.spawnAnt(0,0)
    env.print()
    for i in range(10):
        newAnt.move(1,1)
        env.print()
        print("\n")

class AsyncEnv(Thread):
    def __init__(self, grid):
        super().__init__()

        self.counter = 0

        self.environment = Environment(10, grid)

        logging.info("Environment initialising")
        
        self.ants = []
    
    def spawnAnt(self, x=0, y=0):
        self.ants += [self.environment.spawnAnt(x,y)]

    def run(self):
        self.spawnAnt()
        while(True):
            for ant in self.ants:
                ant.move(1,1)
            self.environment.refresh()
            logging.info("Step: {0}".format(self.counter))
            self.counter += 1
            self.environment.print()
            time.sleep(1)

def main():
    logging.basicConfig(level=logging.INFO)
    rows = 10
    cols = 10
    window = tk.Tk()
    window.geometry("700x700")

    all_entries = []
    for r in range(rows):
        entries_row = []
        for c in range(cols):
            e = tk.Label(window, width=3, height=3, borderwidth=2, relief="solid", text = '0')
            e.grid(row=r, column=c)
            entries_row.append(e)
        all_entries.append(entries_row)

    env_thread = AsyncEnv(all_entries)
    env_thread.start()

    window.mainloop()        

if __name__ == "__main__":
    main()

    