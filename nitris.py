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

## TODO generalise this
# def process_input(block, game, last_event):
#     # Discrete key presses
#     for event in pygame.event.get():
#         if (event.type == pygame.KEYDOWN):
#             if (event.key == pygame.K_SPACE):
#                 block.drop_hard(game)
#             elif event.key == pygame.K_UP:
#                 if block.can_rotate(game):
#                     block.rotate()
#             elif (event.key == pygame.K_LEFT):
#                 if block.can_move(game, LEFT):
#                     block.move(LEFT)
#             elif event.key == pygame.K_RIGHT:
#                 if block.can_move(game, RIGHT):
#                     block.move(RIGHT)
#             elif event.key == pygame.K_DOWN:
#                 if block.can_move(game, DOWN):
#                     block.move(DOWN)

#             last_event = time.time()
#             break

#     # Continuous key presses
#     keystate = pygame.key.get_pressed()
#     if keystate[K_DOWN]:
#         if time.time() - last_event >= SOFT_DROP_SPEED:
#             if block.can_move(game, DOWN):
#                 block.move(DOWN)
#             block.soft_drop += 1
#             last_event = time.time()

#     return last_event

def main():
    # Initialise the game engine
    pygame.init()
    
    # Create window
    window = Window()

    # Create game surface
    board = pygame.Surface(G_SIZE)
    clock = pygame.time.Clock()

    # Create the Game
    game = Game()
    block = game.new_block()

    while True:
        clock.tick(FPS)
        board.fill(WHITE)
        game.process_quit()

        # If the block cannot move anymore, merge and generate a new one
        if (not block.can_move(game, DOWN)):
            if (block.hard_drop) or (time.time() - game.last_event > LOCK_DELAY):
                game.merge(block)
                game.score += block.soft_drop
                game.score += block.hard_drop
                block = game.new_block()
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
        window.draw_sidebar(game.get_info())
        window.draw_board(board)
        pygame.display.update()

if __name__ == "__main__":
    main()


