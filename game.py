import random, time

import block
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
        def get_state(self):
            state = [[0]*ARRAY_SIZE[1] for i in range(ARRAY_SIZE_[0])]
            for tile in self.tiles:
                state[tile.x][tile.y] = 1
            return state

        # zip(*self.state): Zip an unzipped version of self.state
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.get_state()))
        return "\n".join(str(row) for row in transpose)

    def draw(self, board):
        for tile in self.tiles:
            tile.draw(board)
        self.block.draw(board)

    # Logic
    def advance(self):
        # If the block cannot move anymore, update state and spawn new block
        if not (self.block.can_move(self, DOWN)):
            if (self.block.hard_points) or (time.time() - self.last_event > LOCK_DELAY):
                self.update_state()
                self.new_round()
        # Else, process the keyboard input and move accordingly
        elif ((self.block.can_move(self, DOWN)) and (time.time() - self.last_drop > self.level.fall_speed)):
            self.block.move(DOWN)
            self.last_drop = time.time()
    def update_state(self):
        def remove_lines():
            def is_full(line):
                line_tiles = [tile for tile in self.tiles if tile.y == line]
                if len(line_tiles) == ARRAY_SIZE[0]:
                    return line_tiles

            lines = []

            # For each line
            for line in range(ARRAY_SIZE[1]):
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
        self.score += self.block.soft_points
        self.score += self.block.hard_points
        self.score += self.level.points[removed_lines]

        # Update lines/level
        self.lines += removed_lines
        if self.lines >= (self.level.n + 1)*10:
            self.level = Level(self.level.n + 1)
    def new_round(self):
        # Generate new blocks
        self.block = self.next_block
        self.next_block = self.new_block() 

    # Random Generator
    def new_block_bag(self):
        bag = block.Block.__subclasses__()
        random.shuffle(bag)
        return bag
    def new_block(self):
        if not self.block_bag:
            self.block_bag = self.new_block_bag()
        return (self.block_bag.pop())()

    # Game over
    def over(self):
        if not (self.block.can_move(self, DOWN)):
            if (self.block.hard_points) or (time.time() - self.last_event > LOCK_DELAY):
                for tile in self.tiles:
                    if tile.y == 1:
                        return OVER
