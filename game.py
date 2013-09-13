import pygame, random
from block import *
from config import *

class Game(object):
    def __init__(self):
        self.tiles = []
        self.level = Level(0)
        self.lines = 0
        self.score = 0
        self.bag = self.new_bag()

        # Timers
        self.last_event = time.time()
        self.last_drop = time.time()

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

    # Graphic stuff
    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
    def merge(self, block):
        self.tiles += block.tiles

    # Logic-ish stuff
    def remove_lines(self):
        lines = []

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

        # Return how many lines you removed
        return len(lines)
    def is_full(self, line):
        line_tiles = [tile for tile in self.tiles if tile.y == line]
        if len(line_tiles) == ARRAY_X:
            return line_tiles
    def update_info(self, lines):
        if lines > 0:
            self.lines += lines
            self.score += self.level.points[lines]
            if self.lines >= (self.level.n + 1)*10:
                self.level = Level(self.level.n + 1)

    # Random Generator (http://tetris.wikia.com/wiki/Random_Generator)
    def new_bag(self):
        bag = Block.__subclasses__()
        random.shuffle(bag)
        return bag
    def new_block(self):
        if not self.bag:
            self.bag = self.new_bag()
        return (self.bag.pop())()

    # Keyboard stuff (https://github.com/acchao/tetromino_andrew/)
    def process_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Return the event if not quitting
            pygame.event.post(event) 
    def process_input(self, block):
        # Discrete key presses
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    block.drop_hard(self)
                elif event.key == pygame.K_UP:
                    if block.can_rotate(self):
                        block.rotate()
                elif (event.key == pygame.K_LEFT):
                    if block.can_move(self, LEFT):
                        block.move(LEFT)
                elif event.key == pygame.K_RIGHT:
                    if block.can_move(self, RIGHT):
                        block.move(RIGHT)
                elif event.key == pygame.K_DOWN:
                    if block.can_move(self, DOWN):
                        block.move(DOWN)
                self.last_event = time.time()
                break
        # Continuous key presses
        keystate = pygame.key.get_pressed()
        if keystate[K_DOWN]:
            if time.time() - self.last_event >= SOFT_DROP_SPEED:
                if block.can_move(self, DOWN):
                    block.move(DOWN)
                block.soft_drop += 1
                self.last_event = time.time()

    # Getter for information
    def get_info(self):
        return (self.score, self.level, self.lines)