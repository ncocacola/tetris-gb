import pygame
from config import *

class Game(object):
    def __init__(self):
        self.tiles = []
        self.level = 1
        self.lines = 0
        self.score = 0
    def __repr__(self):
        # Zip an unzipped version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.get_state()))
        return "\n".join(str(row) for row in transpose)
    def get_state(self):
        state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        for tile in self.tiles:
            state[tile.x][tile.y] = 1
        return state

    def merge(self, block):
        self.tiles += block.tiles

    def draw(self, surface):
        for tile in self.tiles:
            pygame.draw.rect(surface, BLUE, (CELL_W*tile.x, CELL_H*tile.y, CELL_W, CELL_H))
