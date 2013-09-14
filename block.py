import copy, pygame
from config import *
from nitris import *

class Tile(object):
    def __init__(self, block, x, y):
        self.block = block
        self.x = x
        self.y = y
    def __repr__(self):
        return str((self.x, self.y))
    def __eq__(self, other):
        if isinstance(other, Tile):
            return ((self.x, self.y) == (other.x, other.y))
        return False
    def __hash__(self):     # need this for comparison between Tiles in Sets
        return hash(self.__repr__())

    def draw(self, surface, ghost=False):
        if ghost:
            surface.blit(self.block.ghost, (CELL_W*self.x, CELL_H*self.y))
        else:
            surface.blit(self.block.image, (CELL_W*self.x, CELL_H*self.y))

class Block(object):
    def __init__(self):
        self.create_tiles()
        self.rotation = 0
        self.hard_drop = 0
        self.soft_drop = 0
    def __repr__(self):
        coordinates = []
        for tile in self.tiles:
            coordinates.append((tile.x, tile.y))
        return str(coordinates)

    # Graphic stuff
    def draw(self, surface, ghost=False):
        for tile in self.tiles:
            tile.draw(surface, ghost)

    # Check various things
    def is_valid(self, game):
        return (self.is_in_bounds() and not(self.has_conflicts(game)))
    def is_in_bounds(self):
        x_bounds = [(MIN_X <= tile.x <= MAX_X) for tile in self.tiles]
        y_bounds = [(MIN_Y <= tile.y <= MAX_Y) for tile in self.tiles]
        return not ((any(test == False for test in x_bounds) 
            or any(test == False for test in y_bounds)))
    def has_conflicts(self, game):
        return set(self.tiles).intersection(set(game.tiles))

    # Simulate the move, check if it's valid
    ## TODO generalise this with "Action" (see process_input())
    def can_move(self, game, direction):
        # block = self.copy()
        block = copy.deepcopy(self)
        block.move(direction)
        return block.is_valid(game)
    def can_rotate(self, game):
        # block = self.copy()
        block = copy.deepcopy(self)
        block.rotate()
        return block.is_valid(game)

    # Actions
    def move(self, direction):
        for tile in self.tiles:
            tile.x += direction.dx
            tile.y += direction.dy
    def drop_hard(self, game):
        while self.can_move(game, DOWN):
            self.move(DOWN)
            self.hard_drop += 2
    def ghost(self, game, board):
        # Copy the block (deep copy won't work)
        ghost_block = type(self)()
        ghost_block.tiles=[]
        for tile in self.tiles:
            ghost_block.tiles.append(Tile(tile.block, tile.x, tile.y))
        ghost_block.drop_hard(game)
        ghost_block.draw(board, True)

# The 'central' tile is always the first element of the list of tiles
# See http://tetris.wikia.com/wiki/SRS
## TODO, origin = center tile, generate other tiles from center tile
class BlockI(Block):
    def create_tiles(self):
        self.tiles = [Tile(I, 3, 1), Tile(I, 4, 1), Tile(I, 5, 1), Tile(I, 6, 1)]
    def rotate(self):
        if self.rotation == 0:
            x, y = self.tiles[0].x+2, self.tiles[0].y-1
            self.tiles = [Tile(I, x, y), Tile(I, x, y+1), Tile(I, x, y+2), Tile(I, x, y+3)]
            self.rotation = 1
        elif self.rotation == 1:
            x, y = self.tiles[0].x-2, self.tiles[0].y+2
            self.tiles = [Tile(I, x, y), Tile(I, x+1, y), Tile(I, x+2, y), Tile(I, x+3, y)]
            self.rotation = 2
        elif self.rotation == 2:
            x, y = self.tiles[0].x+1, self.tiles[0].y-2
            self.tiles = [Tile(I, x, y), Tile(I, x, y+1), Tile(I, x, y+2), Tile(I, x, y+3)]
            self.rotation = 3
        elif self.rotation == 3:
            x, y = self.tiles[0].x-1, self.tiles[0].y+1
            self.tiles = [Tile(I, x, y), Tile(I, x+1, y), Tile(I, x+2, y), Tile(I, x+3, y)]
            self.rotation = 0
class BlockO(Block):
    def create_tiles(self):
        self.tiles = [Tile(O, 4, 1), Tile(O, 4, 2), Tile(O, 5, 1), Tile(O, 5, 2)]
    def rotate(self):
        pass
class BlockT(Block):
    def create_tiles(self):
        self.tiles = [Tile(T, 4, 2), Tile(T, 3, 2), Tile(T, 4, 1), Tile(T, 5, 2)]
    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(T, x, y), Tile(T, x, y-1), Tile(T, x, y+1), Tile(T, x+1, y)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(T, x, y), Tile(T, x-1, y), Tile(T, x+1, y), Tile(T, x, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(T, x, y), Tile(T, x, y-1), Tile(T, x, y+1), Tile(T, x-1, y)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(T, x, y), Tile(T, x-1, y), Tile(T, x+1, y), Tile(T, x, y-1)]
            self.rotation = 0
class BlockS(Block):
    def create_tiles(self):
        self.tiles = [Tile(S, 4, 2), Tile(S, 3, 2), Tile(S, 4, 1), Tile(S, 5, 1)]
    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(S, x, y), Tile(S, x+1, y), Tile(S, x, y-1), Tile(S, x+1, y+1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(S, x, y), Tile(S, x+1, y), Tile(S, x, y+1), Tile(S, x-1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(S, x, y), Tile(S, x-1, y), Tile(S, x, y+1), Tile(S, x-1, y-1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(S, x, y), Tile(S, x-1, y), Tile(S, x, y-1), Tile(S, x+1, y-1)]
            self.rotation = 0
class BlockZ(Block):
    def create_tiles(self):
        self.tiles = [Tile(Z, 4, 2), Tile(Z, 3, 1), Tile(Z, 4, 1), Tile(Z, 5, 2)]
    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(Z, x, y), Tile(Z, x+1, y), Tile(Z, x, y+1), Tile(Z, x+1, y-1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(Z, x, y), Tile(Z, x-1, y), Tile(Z, x, y+1), Tile(Z, x+1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(Z, x, y), Tile(Z, x-1, y), Tile(Z, x, y-1), Tile(Z, x-1, y+1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(Z, x, y), Tile(Z, x+1, y), Tile(Z, x, y-1), Tile(Z, x-1, y-1)]
            self.rotation = 0
class BlockJ(Block):
    def create_tiles(self):
        self.tiles = [Tile(J, 4, 2), Tile(J, 3, 1), Tile(J, 3, 2), Tile(J, 5, 2)]
    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(J, x, y), Tile(J, x, y+1), Tile(J, x, y-1), Tile(J, x+1, y-1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(J, x, y), Tile(J, x+1, y), Tile(J, x-1, y), Tile(J, x+1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(J, x, y), Tile(J, x, y-1), Tile(J, x, y+1), Tile(J, x-1, y+1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(J, x, y), Tile(J, x+1, y), Tile(J, x-1, y), Tile(J, x-1, y-1)]
            self.rotation = 0
class BlockL(Block):
    def create_tiles(self):
        self.tiles = [Tile(L, 4, 2), Tile(L, 3, 2), Tile(L, 5, 2), Tile(L, 5, 1)]
    def rotate(self):
        x, y = self.tiles[0].x, self.tiles[0].y
        if self.rotation == 0:
            self.tiles = [Tile(L, x, y), Tile(L, x, y+1), Tile(L, x, y-1), Tile(L, x+1, y+1)]
            self.rotation = 1
        elif self.rotation == 1:
            self.tiles = [Tile(L, x, y), Tile(L, x+1, y), Tile(L, x-1, y), Tile(L, x-1, y+1)]
            self.rotation = 2
        elif self.rotation == 2:
            self.tiles = [Tile(L, x, y), Tile(L, x, y-1), Tile(L, x, y+1), Tile(L, x-1, y-1)]
            self.rotation = 3
        elif self.rotation == 3:
            self.tiles = [Tile(L, x, y), Tile(L, x+1, y), Tile(L, x-1, y), Tile(L, x+1, y-1)]
            self.rotation = 0
