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

class Block(object):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4,1)]
        self.rotation = 0
    def __repr__(self):
        coordinates = []
        for tile in self.tiles:
            coordinates.append((tile.x, tile.y))
        return str(coordinates)

    def can_move(self, direction):
        # TODO Only checks that block stays in the game boundaries
        # TODO Get it to check if other block are not obstructing
        # e.g. if you try to hit a block sideways

        ## TODO rewrite this as such
            # If I move r/l/u/d, do I intersect with any tiles from game?
                # or hit a wall?
        checklist = []

        for tile in self.tiles:
            if direction == LEFT:
                checklist.append(not (tile.x <= MIN_X))
            elif direction == RIGHT:
                checklist.append(not (tile.x >= MAX_X))
            elif direction == DOWN:
                checklist.append(not (tile.y >= MAX_Y))
            elif direction == UP:   # TODO change this to check you can rotate
                checklist.append(not (tile.y <= MIN_Y))

        return (len(checklist) == 4) and all(item == True for item in checklist)
    def move(self, direction):
        for tile in self.tiles:
            tile.x += direction.dx
            tile.y += direction.dy

    # def can_rotate(self):

    def hard_drop(self, game):
        while not self.has_finished(game):
            self.move(DOWN)
    def has_finished(self, game):
        # If the block has reached the bottom
        if any(tile.y == MAX_Y for tile in self.tiles):
            return True
        # Elif the block has fallen on top of other blocks
        elif list(set([Tile(tile.x, (tile.y+1)) for tile in self.tiles]) & set(game.tiles)):
            return True

        # return any(tile.y == MAX_Y for tile in self.tiles) or \
        #        list(set([Tile(tile.x, (tile.y+1)) for tile in self.tiles]) & set(Game.tiles))

        return False
    def draw(self, surface):
        for tile in self.tiles:
            pygame.draw.rect(surface, RED, (CELL_W*tile.x, CELL_H*tile.y, CELL_W, CELL_H))

# The 'central' tile is always the first element of the list of tiles
# See http://tetris.wikia.com/wiki/SRS
class BlockI(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4, 1)]
        self.rotation = 0

    def rotate(self):
        print self.rotation
        if self.rotation == 0:
            x, y = self.tiles[0].x+2, self.tiles[0].y-1
            self.tiles = [Tile(x, y), Tile(x, y+1), Tile(x, y+2), Tile(x, y+3)]
            self.rotation = 1
        elif self.rotation == 1:
            x, y = self.tiles[0].x-2, self.tiles[0].y+2
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x+2, y), Tile(x+3, y)]
            self.rotation = 2
        elif self.rotation == 2:
            x, y = self.tiles[0].x+1, self.tiles[0].y-2
            self.tiles = [Tile(x, y), Tile(x, y+1), Tile(x, y+2), Tile(x, y+3)]
            self.rotation = 3
        elif self.rotation == 3:
            x, y = self.tiles[0].x-1, self.tiles[0].y+1
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x+2, y), Tile(x+3, y)]
            self.rotation = 0
class BlockO(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 1), Tile(2, 2)]
        self.rotation = 0

    def rotate(self):
        pass
class BlockT(Block):
    def __init__(self):
        self.tiles = [Tile(2, 2), Tile(1, 2), Tile(2, 1), Tile(3, 2)]
        self.rotation = 0

    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(x, y), Tile(x, y-1), Tile(x, y+1), Tile(x+1, y)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x+1, y), Tile(x, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(x, y), Tile(x, y-1), Tile(x, y+1), Tile(x-1, y)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x+1, y), Tile(x, y-1)]
            self.rotation = 0
class BlockS(Block):
    def __init__(self):
        self.tiles = [Tile(2, 2), Tile(1, 2), Tile(2, 1), Tile(3, 1)]
        self.rotation = 0

    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x, y-1), Tile(x+1, y+1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x, y+1), Tile(x-1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x, y+1), Tile(x-1, y-1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x, y-1), Tile(x+1, y-1)]
            self.rotation = 0
class BlockZ(Block):
    def __init__(self):
        self.tiles = [Tile(2, 2), Tile(1, 1), Tile(2, 1), Tile(3, 2)]
        self.rotation = 0

    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x, y+1), Tile(x+1, y-1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x, y+1), Tile(x+1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(x, y), Tile(x-1, y), Tile(x, y-1), Tile(x-1, y+1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x, y-1), Tile(x-1, y-1)]
            self.rotation = 0
class BlockJ(Block):
    def __init__(self):
        self.tiles = [Tile(2, 2), Tile(1, 1), Tile(1, 2), Tile(3, 2)]
        self.rotation = 0

    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(x, y), Tile(x, y+1), Tile(x, y-1), Tile(x+1, y-1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x-1, y), Tile(x+1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(x, y), Tile(x, y-1), Tile(x, y+1), Tile(x-1, y+1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x-1, y), Tile(x-1, y-1)]
            self.rotation = 0
class BlockL(Block):
    def __init__(self):
        self.tiles = [Tile(2, 2), Tile(1, 2), Tile(3, 2), Tile(3, 1)]
        self.rotation = 0

    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(x, y), Tile(x, y+1), Tile(x, y-1), Tile(x+1, y+1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x-1, y), Tile(x-1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(x, y), Tile(x, y-1), Tile(x, y+1), Tile(x-1, y-1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(x, y), Tile(x+1, y), Tile(x-1, y), Tile(x+1, y-1)]
            self.rotation = 0
