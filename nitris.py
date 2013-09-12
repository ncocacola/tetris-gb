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

def process_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.event.post(event) #return the event if not quitting
    # Add exit with ESC/Q            

def process_input(block, game, lastEventTime):
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                block.hard_drop(game)
            elif event.key == pygame.K_UP:
                if block.can_rotate(game):
                    block.rotate()
            elif (event.key == pygame.K_LEFT):
                if block.can_move(game, LEFT):
                    block.move(LEFT)
            elif event.key == pygame.K_RIGHT:
                if block.can_move(game, RIGHT):
                    block.move(RIGHT)
            elif event.key == pygame.K_DOWN:
                if block.can_move(game, DOWN):
                    block.move(DOWN)

            lastEventTime = time.time()

    return lastEventTime

def main():
    # Initialise the game engine
    pygame.init()
    
    # Create window
    window = pygame.display.set_mode(W_SIZE)
    pygame.display.set_caption("Tetris")
    screen = pygame.Surface(G_SIZE)

    # Create clock
    clock = pygame.time.Clock()

    # Create the Game
    game = Game()
    block = game.new_block()

    lastEventTime = time.time()
    lastDropTime = time.time()

    while True:

        # Lock the game at default fps
        clock.tick(FPS)

        # Clear the screen
        screen.fill(WHITE)

        # Check if the user wants to quit
        process_quit()

        # If the piece cannot move anymore, merge and generate a new one
        if (not block.can_move(game, DOWN)):
            game.merge(block)
            block = game.new_block()
        # Else, process the keyboard input and move accordingly
        elif (time.time() - lastDropTime > DEFAULTFALLSPEED):
            block.move(DOWN)
            lastDropTime = time.time()

        lastEventTime = process_input(block, game, lastEventTime)

        # Draw the game and block to the screen
        game.draw(screen)
        block.draw(screen)

        # Process the lines
        game.remove_lines()

        # Redraw game and block to the screen (smoother line deletion)
        game.draw(screen)
        block.draw(screen)

        # Update the screen
        window.blit(screen, (40, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()


