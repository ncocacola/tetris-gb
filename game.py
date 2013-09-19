import pygame, random
from block import *
from config import *

class Game(object):
    def __init__(self):
        # State variables
        self.tiles = []
        self.level = Level(0)
        self.lines = 0
        self.score = 0

        # Current/next block
        self.block_bag = self.new_block_bag()
        self.block = self.new_block()
        self.next_block = self.new_block()

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

    def advance(self):
        # If the block cannot move anymore
        if not (self.block.can_move(self, DOWN)):
            if (self.block.hard_drop) or (time.time() - self.last_event > LOCK_DELAY):
                self.update_state()
                self.new_round()
        # Else, process the keyboard input and move accordingly
        elif ((self.block.can_move(self, DOWN)) and (time.time() - self.last_drop > self.level.fall_speed)):
            self.block.move(DOWN)
            self.last_drop = time.time()
    def new_round(self):
        # Generate new blocks
        self.block = self.next_block
        self.next_block = self.new_block() 

    # Graphic stuff
    def draw(self, board):
        for tile in self.tiles:
            tile.draw(board)
        self.block.draw(board)
        

    # Logic-ish stuff
    # Rethink/rewrite this
    def update_state(self):
        def remove_lines():
            def is_full(line):
                line_tiles = [tile for tile in self.tiles if tile.y == line]
                if len(line_tiles) == ARRAY_X:
                    return line_tiles

            lines = []

            # For each line
            for line in range(ARRAY_Y):
                # Get all the Tiles on that line
                all_tiles = is_full(line)
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

        # Merge the block into the game
        self.tiles += self.block.tiles

        # Remove lines
        removed_lines = remove_lines()

        # Update score
        self.score += self.block.soft_drop
        self.score += self.block.hard_drop
        self.score += self.level.points[removed_lines]

        # Update lines/level
        self.lines += removed_lines
        if self.lines >= (self.level.n + 1)*10:
            self.level = Level(self.level.n + 1)
    # Rename this to 'redraw'?
    # def update_draw(self, board):
    #     # Redraw the game and block to the board
    #     self.draw(board)
    #     self.block.draw(board)

    # Random Generator (http://tetris.wikia.com/wiki/Random_Generator)
    def new_block_bag(self):
        bag = Block.__subclasses__()
        random.shuffle(bag)
        return bag
    def new_block(self):
        if not self.block_bag:
            self.block_bag = self.new_block_bag()
        return (self.block_bag.pop())()

    # Game over?
    def check_over(self, block):
        if not (block.can_move(self, DOWN)):
            for tile in self.tiles:
                if tile.y == 1:
                    self.state = OVER

