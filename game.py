import pygame
from config import *

class Tetris(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]    # 10 * 20 array of ints
        self.level = 1
        self.lines = 0
        self.score = 0

    def merge(self, Tetronimo):
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                self.state[col][row] += Tetronimo.state[col][row]

    def draw(self, surface):    
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                if self.state[col][row] == 1:
                    pygame.draw.rect(surface, BLUE, (CELL_W*col, CELL_H*row, CELL_W, CELL_H))

    def console(self):
        # Zip an unpacked version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]