#!/usr/bin/env python

## http://tetris.wikia.com/wiki/Tetris_Guideline
## http://stackoverflow.com/questions/1969005/enumerations-in-python (Objects with functionality)

# Useful modules
import sys
# PyGame
import pygame
from pygame.locals import *
# Classes
from pieces import *
from game import *
from config import *

def process_input(event):
    # TODO do some refactoring and get rid of this 'global'
    global MOVE_TICKER

    if (event.type == KEYDOWN):
        if MOVE_TICKER == 0:
            MOVE_TICKER = MOVE_TICKER_DEFAULT
            if event.key == pygame.K_LEFT:
                return LEFT
            elif event.key == pygame.K_RIGHT:
                return RIGHT
            elif event.key == pygame.K_DOWN:
                return DOWN
            # TODO Remove this later
            elif event.key == pygame.K_UP:
                return UP
    # else:
    #     if MOVE_TICKER == 0:
    #         MOVE_TICKER = MOVE_TICKER_DEFAULT
    #         return "down"

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
    block = Block()
    # block = BlockO()

    # print block.array()
    # print block.transpose()

    # for i in range(1):
    while True:
        # Lock the game at default fps
        clock.tick(FPS)

        # Decrement MOVE_TICKER
        if MOVE_TICKER > 0:
            MOVE_TICKER -= 1

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Process keyboard input
        direction = process_input(event)

        # If the piece has reached the bottom or the top of the stack of pieces
        if block.has_finished(game):
            # Merge it with current game state
            game.merge(block)
            # Spawn a new piece
            block = Block()
        # Else, move the piece in the specified direction, if it can
        elif block.can_move(direction):
            block.move(direction)

        # Draw game to screen
        game.draw(screen)
        block.draw(screen)

        # Update the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()


