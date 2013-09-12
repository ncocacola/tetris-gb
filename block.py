import copy, pygame
from config import *
from nitris import *

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
        self.tiles = []
        self.rotation = 0
    def __repr__(self):
        coordinates = []
        for tile in self.tiles:
            coordinates.append((tile.x, tile.y))
        return str(coordinates)

    # Simulate the move, check if it's valid
    def can_move(self, game, direction):
        moved_block = copy.deepcopy(self)
        moved_block.move(direction)
        return moved_block.is_valid(game)
    def can_rotate(self, game):
        rotated_block = copy.deepcopy(self)
        rotated_block.rotate()
        return rotated_block.is_valid(game)

    def move(self, direction):
        for tile in self.tiles:
            tile.x += direction.dx
            tile.y += direction.dy

    def hard_drop(self, game):
        while self.can_move(game, DOWN):
            self.move(DOWN)

    def is_valid(self, game):
        return (self.is_in_bounds() and not(self.has_conflicts(game)))

    def is_in_bounds(self):
        x_bounds = [(MIN_X <= tile.x <= MAX_X) for tile in self.tiles]
        y_bounds = [(MIN_Y <= tile.y <= MAX_Y) for tile in self.tiles]
        return not ((any(test == False for test in x_bounds) 
            or any(test == False for test in y_bounds)))
    def has_conflicts(self, game):
        return set(self.tiles).intersection(set(game.tiles))

# The 'central' tile is always the first element of the list of tiles
# See http://tetris.wikia.com/wiki/SRS
class BlockI(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(2, 1), Tile(3, 1), Tile(4, 1)]
        self.rotation = 0

    def rotate(self):
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/i.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
class BlockO(Block):
    def __init__(self):
        self.tiles = [Tile(1, 1), Tile(1, 2), Tile(2, 1), Tile(2, 2)]
        self.rotation = 0

    def rotate(self):
        pass

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/o.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/t.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/s.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/z.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/j.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))
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

    def draw(self, surface):
        for tile in self.tiles:
            block = pygame.image.load("./blocks/l.png")    # Use os.path.join instead
            surface.blit(block, (CELL_W*tile.x, CELL_H*tile.y))

