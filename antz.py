#!/usr/bin/env python

import logging
import tkinter as tk
from threading import Thread
import time
from turtle import color
from PIL import Image, ImageTk
import random
from antzElements import Ant, Cell, Environment

size = 30
antsNumber = 5

class AsyncEnv(Thread):
    def __init__(self, grid):
        super().__init__()
        self.counter = 0
        self.environment = Environment(size)
        self.grid = grid
        logging.info("Environment initialising")
        self.running = False
    
    def spawnAnt(self, x=0, y=0):
        self.environment.spawnAnt(x,y)

    def paintHelper(self, x, y):
        colour = "white"
        if str(self.environment.grid[x][y]) == "A":
            colour = "red"
        self.grid[x][y].config(text = str(self.environment.grid[x][y]), bg=colour)

    #if x and y are not given, refresh the whole grid
    def refresh(self, x = None, y = None):
        logging.info("Refreshing GUI")
        if x is not None and y is not None:
            self.paintHelper(x,y)
        else:
            for x in range(self.environment.size):
                for y in range(self.environment.size):
                    self.paintHelper(x,y)

    def run(self):
        self.running = True
        for i in range(antsNumber):
            self.spawnAnt(random.randint(0,size-1),random.randint(0,size-1))
        while(self.running):
            for key, ant in self.environment.ants.items():
                deltaX = random.randint(-1, 1)
                deltaY = random.randint(-1, 1)
                oldX = ant.x
                oldY = ant.y
                ant.move(deltaX,deltaY)
                self.refresh(ant.x, ant.y)
                self.refresh(oldX, oldY)
            self.counter += 1
            time.sleep(.5)

def main():
    logging.basicConfig(level=logging.INFO)
    rows = size
    cols = size
    window = tk.Tk()
    window.geometry("700x700")

    all_entries = []
    for r in range(rows):
        entries_row = []
        for c in range(cols):
            e = tk.Label(window, width=1, height=1, borderwidth=1, relief="solid", text = '0')
            e.grid(row=r, column=c)
            entries_row.append(e)
        all_entries.append(entries_row)

    env_thread = AsyncEnv(all_entries)
    env_thread.start()

    window.mainloop()        

if __name__ == "__main__":
    main()

    