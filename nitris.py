#!/usr/bin/env python

## http://tetris.wikia.com/wiki/Tetris_Guideline

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
                return "left"
            elif event.key == pygame.K_RIGHT:
                return "right"
            elif event.key == pygame.K_DOWN:
                return "down"
            # TODO Remove this later
            elif event.key == pygame.K_UP:
                return "up"
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
    Game = Tetris()
    Piece = Tetronimo()

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
        if Piece.has_finished(Game):
            # Merge it with current game state
            Game.merge(Piece) 
            # Spawn a new piece
            Piece = Tetronimo()
        # Else, move the piece in the specified direction, if it can
        elif Piece.can_move(Game, direction):
            Piece.move(direction)

        # Draw game to screen
        Game.draw(screen)
        Piece.draw(screen)

        # Update the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()


