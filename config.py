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
LEFT = Direction("left", -1, 0)
RIGHT = Direction("right", 1, 0)
DOWN = Direction("down", 0, 1)
UP = Direction("up", 0, -1)         # TODO Remove this later

# Colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

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

# Frames per second
FPS = 50

# Move ticker
## http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
## TODO MOVE_TICKER should not be capital as it varies
MOVE_TICKER = 0
MOVE_TICKER_DEFAULT = 10 # Allow a move every 10 frames = every 0.2 second

# Gameplay speeds
SOFTDROPSPEED = 0.08
LATERALSPEED = 0.15
DEFAULTFALLSPEED = 1