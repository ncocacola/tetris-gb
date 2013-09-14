#!/usr/bin/env python

## http://tetris.wikia.com/wiki/Tetris_Guideline
## http://stackoverflow.com/questions/1969005/enumerations-in-python (Objects with functionality)
## Keyboard stuff: https://github.com/acchao/tetromino_andrew/

# Useful modules
import sys, time
# PyGame
import pygame
from pygame.locals import *
# Classes
from game import *
from block import *
from config import *
from window import *

def main():
    # Initialise the game engine
    pygame.init()
    
    # Create the Game
    game = Game()
    # Create the two blocks
    block = game.new_block()
    next_block = game.new_block()
    # Create game surface
    board = pygame.Surface(G_SIZE)
    clock = pygame.time.Clock()
    # Create window
    window = Window(next_block)

    while True:
        clock.tick(FPS)
        board.fill(WHITE)
        game.process_quit()

        # Ghost mode
        block.ghost(game, board)

        # If the block cannot move anymore
        if (not block.can_move(game, DOWN)):
            if (block.hard_drop) or (time.time() - game.last_event > LOCK_DELAY):
                # Merge
                game.merge(block)
                # Scoring
                game.score += block.soft_drop
                game.score += block.hard_drop
                # Generate new blocks
                block = next_block
                next_block = game.new_block()
        # Else, process the keyboard input and move accordingly
        elif ((block.can_move(game, DOWN)) and (time.time() - game.last_drop > game.level.fall_speed)):
            block.move(DOWN)
            game.last_drop = time.time()

        game.process_input(block)

        # Remove completed lines & Update global info
        lines = game.remove_lines()
        game.update_info(lines)

        # Draw the game and block to the board
        game.draw(board)
        block.draw(board)

        # Update the window
        ## Once you have 'merged' block and game (i.e. have game.block, game.next_block),
        ## Put next_block in the tuple get_info() returns
        window.draw_sidebar(game.get_info(), next_block)
        window.draw_board(board)
        pygame.display.update()

if __name__ == "__main__":
    main()


