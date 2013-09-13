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
        pygame.event.post(event) # Return the event if not quitting

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
    pygame.display.set_caption("nitris")

    # Draw sidebar
    sidebar = pygame.image.load(os.path.join(ASSETS_DIR, "sidebar.png"))
    window.blit(sidebar, (20, 0))
    window.blit(sidebar, (240, 0))
    pygame.draw.line(window, WHITE, (18, 0), (18, 400), 3)
    pygame.draw.line(window, WHITE, (261, 0), (261, 400), 3)
    # Draw box under score
    pygame.draw.line(window, WHITE, (263, 38), (400, 38), 3)
    pygame.draw.rect(window, GREY, (263, 40, 137, 17))
    pygame.draw.line(window, WHITE, (263, 58), (400, 58), 3)
    # Draw score, level, lines, queue // initialise them to 0 or next block
    def draw_box(start, end):
        t = 3                               # 'Thickness' of the box
        wx, wy = start[0]+1, start[1]
        ww, wh = tuple(map(lambda x, y: x - y, end, start))

        outer_box = [(wx-t, wy+t), (wx, wy+t), (wx, wy),
                     (wx+ww-t, wy), (wx+ww-t, wy+t), (wx+ww, wy+t),
                     (wx+ww, wy+wh-t), (wx+ww-t, wy+wh-t), (wx+ww-t, wy+wh),
                     (wx, wy+wh), (wx, wy+wh-t), (wx-t, wy+wh-t)]

        bx, by = wx+t, wy+t
        bw, bh = ww-(2*t), wh-(2*t)

        inner_box = [(bx-t, by+t), (bx, by+t), (bx, by), 
                     (bx+bw-t, by), (bx+bw-t, by+t), (bx+bw, by+t),
                     (bx+bw, by+bh-t), (bx+bw-t, by+bh-t), (bx+bw-t, by+bh), 
                     (bx, by+bh), (bx, by+bh-t), (bx-t, by+bh-t)]

        pygame.draw.polygon(window, WHITE, outer_box, 0)
        pygame.draw.polygon(window, GREY, inner_box, 3)

        return start[0]+7, start[1]+5       # Where the content of the box goes
    score = draw_box((276, 16), (388, 49))
    level = draw_box((276, 116), (388, 171))
    lines = draw_box((276, 176), (388, 231))
    queue = draw_box((276, 251), (389, 363))
    # Text
    window.blit(font.render("score", 1, BLACK), score)
    window.blit(font.render("level", 1, BLACK), level)
    window.blit(font.render("lines", 1, BLACK), lines)

    # Create game surface
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

        # Update score, level, lines, next piece
        # info.update()

        # Update the screen
        window.blit(screen, (40, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()


