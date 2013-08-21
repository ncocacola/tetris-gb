## GLOBAL VARIABLES

# Useful classes
class Direction(object):
    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy
    def __str__(self):
        return self.name

# Directions (NB: Board is upside down: Down ==> Add, Up ==> Substract)
# http://stackoverflow.com/questions/1969005/enumerations-in-python (Objects with functionality)
LEFT = Direction("left", -1, 0)
RIGHT = Direction("right", 1, 0)
DOWN = Direction("down", 0, 1)
UP = Direction("up", 0, -1)         # TODO Remove this later

# Step
STEP = 1

# Window size
WIDTH, HEIGHT = 200, 400
CELL_W, CELL_H = WIDTH/10, HEIGHT/20
ARRAY_X, ARRAY_Y = WIDTH/20, HEIGHT/20
W_SIZE   = (WIDTH, HEIGHT)
W_CENTER = (WIDTH/2, HEIGHT/2)
MIN_X, MAX_X, MIN_Y, MAX_Y = 0, ARRAY_X-1, 0, ARRAY_Y-1

# Usual colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

# Frames per second
FPS = 50

# Move ticker
## http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
## TODO MOVE_TICKER should not be capital as it varies
MOVE_TICKER = 0
MOVE_TICKER_DEFAULT = 10 # Allow a move every 10 frames = every 0.2 second