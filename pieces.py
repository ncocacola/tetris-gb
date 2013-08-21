import pygame
from config import *

class Tile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return str((self.x, self.y))
    def __eq__(self, other):
        if isinstance(other, Tile):
            return (self.x, self.y) == (other.x, other.y)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):     # need this for comparison between Tiles in Sets
        return hash(self.__repr__())

class Tetronimo(object):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4,1)]
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

    def can_move(self, Game, direction):
        # TODO Only checks that block stays in the game boundaries
        # TODO Get it to check if other block are not obstructing
        checklist = []

        for tile in self.tiles:
            if direction == LEFT:
                checklist.append(not (tile.x <= MIN_X))
            elif direction == RIGHT:
                checklist.append(not (tile.x >= MAX_X))
            elif direction == DOWN:
                checklist.append(not (tile.y >= MAX_Y))
            elif direction == UP:
                checklist.append(not (tile.y <= MIN_Y))

        return (len(checklist) == 4) and all(item == True for item in checklist)
            
    def move(self, direction):
        for tile in self.tiles:
            if direction == LEFT:
                tile.x -= 
            elif direction == RIGHT:
                tile.x += 1
        ## Board is upside down. Down ==> Add, Up ==> Substract
            elif direction == DOWN:
                tile.y += 1
            # TODO Remove this later
            elif direction == UP: 
                tile.y -= 1

    def has_finished(self, Game):
        # If the block has reached the bottom
        if any(tile.y == MAX_Y for tile in self.tiles):
            return True
        # Elif the block has fallen on top of other blocks
        elif list(set([Tile(tile.x, (tile.y+1)) for tile in self.tiles]) & set(Game.tiles)):
            return True
        else:
            return False

        # return any(tile.y == MAX_Y for tile in self.tiles) or \
        #        list(set([Tile(tile.x, (tile.y+1)) for tile in self.tiles]) & set(Game.tiles))

    def draw(self, surface):
        for tile in self.tiles:
            pygame.draw.rect(surface, RED, (CELL_W*tile.x, CELL_H*tile.y, CELL_W, CELL_H))




class TetroI(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4, 1)]

class TetroO(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 1), Tile(2, 2)]

class TetroT(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(2, 2), Tile(3, 1)]

class TetroS(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 2), Tile(2, 1), Tile(2, 2), Tile(3, 1)]

class TetroZ(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(2, 2), Tile(3, 2)]

class TetroJ(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 2), Tile(3, 2)]

class TetroL(Tetronimo):
    def __init__(self):
        self.tiles = [Tile(3, 1), Tile(1, 2), Tile(2, 2), Tile(3, 2)]




