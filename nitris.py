#!/usr/bin/env python

## http://tetris.wikia.com/wiki/Tetris_Guideline
## http://stackoverflow.com/questions/1969005/enumerations-in-python (Objects with functionality)

# Useful modules
import sys
# PyGame
import pygame
from pygame.locals import *
# Classes
from game import *
from block import *
from config import *

def process_input(event, block, game):
    # TODO do some refactoring and get rid of this 'global'
    global MOVE_TICKER

    if (event.type == KEYDOWN):
        if event.key == pygame.K_SPACE:
            block.hard_drop(game)

    if MOVE_TICKER == 0:
        MOVE_TICKER = MOVE_TICKER_DEFAULT

        # If a key was pressed, check that the piece can move
        # in the specified direction, and move it accordingly
        if (event.type == KEYDOWN):
            if event.key == pygame.K_LEFT:
                if block.can_move(LEFT):
                    block.move(LEFT)
            elif event.key == pygame.K_RIGHT:
                if block.can_move(RIGHT):
                    block.move(RIGHT)
            elif event.key == pygame.K_DOWN:
                if block.can_move(DOWN):
                    block.move(DOWN)
            elif event.key == pygame.K_UP:
                block.rotate()
            # elif event.key == pygame.K_SPACE:
            #     block.hard_drop(game)
        # Else, move the block down once
        else:
            block.move(DOWN)

    elif MOVE_TICKER > 0:
        MOVE_TICKER -= 1

def main():
    # TODO do some refactoring and get rid of this 'global'
    global MOVE_TICKER

    # Initialise the game engine
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode(W_SIZE)
    pygame.display.set_caption("Tetris")

    # Create clock
    clock = pygame.time.Clock()

    # Create the Game
    game = Game()
    block = game.new_block()
    # block = BlockO()

    while True:
        # Lock the game at default fps
        clock.tick(FPS)

        # Clear the screen
        screen.fill(WHITE)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # If the piece has reached the bottom or the top of the stack of pieces
        if block.has_finished(game):
            # Merge it with current game state
            game.merge(block)
            # Spawn a new piece
            block = game.new_block()
        # If not, process the keyboard input and move accordingly
        else:
            process_input(event, block, game)

        # Draw the game and block to the screen
        game.draw(screen)
        block.draw(screen)

        # Process the lines
        game.process_lines()

        # Redraw game and block to the screen (smoother line deletion)
        game.draw(screen)
        block.draw(screen)

        # Update the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()


