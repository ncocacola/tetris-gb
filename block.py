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
    def rotate(self):
        ## TODO improve this to implement SRS
        ## Can you get it to play with the Tiles directly?

        # Convert current position to a 4*4 array
        # Transpose and mirror the array
        new_state = map(list, zip(*self.array()))[::-1]
        new_tiles = []

        # Get translation factor
        translation = (min([tile.x for tile in self.tiles]), min([tile.y for tile in self.tiles]))
        # Convert back to tiles
        for x in range(len(new_state)):
            for y in range(len(new_state[x])):
                if new_state[x][y] == 1:
                    # Apply translation factor back
                    new_tiles.append(Tile(x + translation[0], y + translation[1]))

        # Apply the new Tiles to self.tiles
        self.tiles = new_tiles
    def array(self):
        translation = (min([tile.x for tile in self.tiles]), min([tile.y for tile in self.tiles]))
        state = [[0]*4 for i in range(4)]
        for tile in self.tiles:
            x = tile.x - translation[0]
            y = tile.y - translation[1]
            state[x][y] = 1
        return state

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

class BlockI(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4, 1)]

class BlockO(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 1), Tile(2, 2)]

    def rotate(self):
        pass

class BlockT(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(2, 2), Tile(3, 1)]
class BlockS(Block):
    def __init__(self):
        self.tiles = [Tile(1, 2), Tile(2, 1), Tile(2, 2), Tile(3, 1)]
class BlockZ(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(2, 2), Tile(3, 2)]
class BlockJ(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 2), Tile(3, 2)]
class BlockL(Block):
    def __init__(self):
        self.tiles = [Tile(3, 1), Tile(1, 2), Tile(2, 2), Tile(3, 2)]
