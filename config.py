import os, pygame

# Useful classes
class Tile(object):
    def __init__(self, type_, x, y):
        self.type = type_
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
            surface.blit(self.type.ghost, (CELL_W*self.x, CELL_H*self.y))
        else:
            surface.blit(self.type.image, (CELL_W*self.x, CELL_H*self.y))
class Direction(object):
    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy
    def __str__(self):
        return self.name
class BlockType(object):
    def __init__(self, name, image, ghost):
        self.name = name
        self.image = pygame.image.load(image)
        self.ghost = pygame.image.load(ghost)
    def __str__(self):
        return self.name
class Level(object):
    def __init__(self, n):
        def limit(n):
            if n > 20:
                return 20
            return n
        self.n = n
        self.fall_speed = FPR[limit(self.n)]/FPS
        self.points = [x*(self.n + 1) for x in [0, 40, 100, 300, 1200]]
        # self.points = map(lambda x: x*(self.n + 1), [0, 40, 100, 300, 1200])
    def __str__(self):
        return str(self.n)

# Dimensions -- (WIDTH, HEIGHT)
ARRAY_SIZE = (10, 22)
WINDOW_SIZE = (400, 400)                # Remove two rows at the top (they should be hidden)
BOARD_SIZE = (200, 440)
CELL_W, CELL_H = (20, 20)
MAX_X, MAX_Y = [a-1 for a in ARRAY_SIZE]

# Colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREY  = (96, 96, 96)

# Directories
ASSETS_DIR = os.path.join(".", "assets")
BLOCKS_DIR = os.path.join(ASSETS_DIR, "blocks")
GHOSTS_DIR = os.path.join(ASSETS_DIR, "ghosts")

# Bricks
BRICKS = pygame.image.load(os.path.join(ASSETS_DIR, "bricks.png"))

# Font
pygame.font.init()
font = pygame.font.Font(os.path.join(ASSETS_DIR, "fonts/tetris-gb.ttf"), 20)

# Music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(ASSETS_DIR, "music/tetris-gb.wav"))

# Game States
SPLASH = "splash"
PLAY = "play"
PAUSE = "pause"
OVER = "over"

# Frames per second/Frames per row (for fall speeds)
FPS = 59.37
FPR = [53, 49, 45, 41, 37, 33, 28, 22, 17, 11, 10, 9, 8, 7, 6, 6, 5, 5, 4, 4, 3]

# Gameplay speeds
SOFT_DROP_SPEED = 1/(FPS/3)       # Soft Drop = 1 row per 3 frames
LOCK_DELAY = 0.5

# Directions (NB: Board is upside down: Down ==> Add, Up ==> Substract)
LEFT = Direction("left", -1, 0)
RIGHT = Direction("right", 1, 0)
DOWN = Direction("down", 0, 1)

# BlockTypes
I = BlockType("I", os.path.join(BLOCKS_DIR, "I.png"), os.path.join(GHOSTS_DIR, "I.png"))
J = BlockType("J", os.path.join(BLOCKS_DIR, "J.png"), os.path.join(GHOSTS_DIR, "J.png"))
L = BlockType("L", os.path.join(BLOCKS_DIR, "L.png"), os.path.join(GHOSTS_DIR, "L.png"))
O = BlockType("O", os.path.join(BLOCKS_DIR, "O.png"), os.path.join(GHOSTS_DIR, "O.png"))
S = BlockType("S", os.path.join(BLOCKS_DIR, "S.png"), os.path.join(GHOSTS_DIR, "S.png"))
T = BlockType("T", os.path.join(BLOCKS_DIR, "T.png"), os.path.join(GHOSTS_DIR, "T.png"))
Z = BlockType("Z", os.path.join(BLOCKS_DIR, "Z.png"), os.path.join(GHOSTS_DIR, "Z.png"))
