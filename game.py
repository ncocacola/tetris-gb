import pygame, random
from block import *
from config import *

class Game(object):
    def __init__(self):
        self.tiles = []
        self.level = 0
        self.lines = 0
        self.score = 0
        self.bag = self.new_bag()
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

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
    def merge(self, block):
        self.tiles += block.tiles

    def remove_lines(self):
        lines = []
        score = 0

        # For each line
        for line in range(ARRAY_Y):
            # Get all the Tiles on that line
            all_tiles = self.is_full(line)
            # If the line is all tiles
            if all_tiles:
                # Remove all the tiles
                map(self.tiles.remove, all_tiles)
                # Record the line
                lines.append(line)

        # For each removed line 
        for line in lines:
            for tile in self.tiles:
                # Get all the Tiles located above the line you just removed
                if tile.y < line:
                    # Move them down one notch
                    tile.y += DOWN.dy

        # Update the global score with the total
        self.lines += len(lines)
    def is_full(self, line):
        line_tiles = [tile for tile in self.tiles if tile.y == line]
        if len(line_tiles) == ARRAY_X:
            return line_tiles

    # Random Generator
    # See http://tetris.wikia.com/wiki/Random_Generator
    def new_bag(self):
        bag = Block.__subclasses__()
        random.shuffle(bag)
        return bag
    def new_block(self):
        if not self.bag:
            self.bag = self.new_bag()
        return (self.bag.pop())()

    # Getter for information
    def get_info(self):
        return (self.score, self.level, self.lines)