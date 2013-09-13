## GLOBAL VARIABLES

import os, pygame

# Useful classes
class Direction(object):
    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy
    def __str__(self):
        return self.name

class BlockType(object):
    def __init__(self, name, image):
        self.name = name
        self.image = pygame.image.load(image)
    def __str__(self):
        return self.name

class Level(object):
    def __init__(self, n):
        if 0 <= n <= 20:
            self.n = n
        elif n > 20:
            self.n = 20
        self.fall_speed = FPR[self.n]/FPS
        self.points = map(lambda x: x*(self.n + 1), [0, 40, 100, 300, 1200])
    def __str__(self):
        return str(self.n)

# Directories
ASSETS_DIR = os.path.join(".", "assets")
BLOCKS_DIR = os.path.join(ASSETS_DIR, "blocks")

# Directions (NB: Board is upside down: Down ==> Add, Up ==> Substract)
LEFT = Direction("left", -1, 0)
RIGHT = Direction("right", 1, 0)
DOWN = Direction("down", 0, 1)

# BlockTypes
## Use os.path.join instead
I = BlockType("I", os.path.join(BLOCKS_DIR, "I.png"))
J = BlockType("J", os.path.join(BLOCKS_DIR, "J.png"))
L = BlockType("L", os.path.join(BLOCKS_DIR, "L.png"))
O = BlockType("O", os.path.join(BLOCKS_DIR, "O.png"))
S = BlockType("S", os.path.join(BLOCKS_DIR, "S.png"))
T = BlockType("T", os.path.join(BLOCKS_DIR, "T.png"))
Z = BlockType("Z", os.path.join(BLOCKS_DIR, "Z.png"))

# Colours
BLACK = (  0,   0,   0)
# BLACK = (53, 53, 53)
WHITE = (255, 255, 255)
# WHITE = (248, 248, 248)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
GREY  = (96, 96, 96)

# Window size
W_WIDTH, W_HEIGHT = 400, 400            # Remove two rows at the end (they should be hidden)
WIDTH, HEIGHT = 200, 400                # Rename these
G_X_POSITION, G_Y_POSITION = 40, 0      # w.r.t to the main window
CELL_W, CELL_H = WIDTH/10, HEIGHT/20
ARRAY_X, ARRAY_Y = 10, 20
W_SIZE   = (W_WIDTH, W_HEIGHT)
G_SIZE   = (WIDTH, HEIGHT)
W_CENTER = (W_WIDTH/2, W_HEIGHT/2)
MIN_X, MAX_X, MIN_Y, MAX_Y = 0, ARRAY_X-1, 0, ARRAY_Y-1

# Frames per second/Frames per row
FPS = 59.37
FPR = [53, 49, 45, 41, 37, 33, 28, 22, 17, 11, 10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3]

# Move ticker
## http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
## TODO MOVE_TICKER should not be capital as it varies
MOVE_TICKER = 0
MOVE_TICKER_DEFAULT = 10 # Allow a move every 10 frames = every 0.2 second

# Gameplay speeds
SOFT_DROP_SPEED = 1/(FPS/3)       # Soft Drop = 1 row per 3 frames
LOCK_DELAY = 0.5

# Font
pygame.font.init()
font = pygame.font.Font("./assets/fonts/tetris-gb.ttf", 20)

