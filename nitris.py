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
                block.drop_hard(game)
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

def draw_box(window, (wx, wy, ww, wh)):
    t = 3                               # 'Thickness' of the box
    # wx, wy = start[0]+1, start[1]
    # ww, wh = tuple(map(lambda x, y: x - y, end, start))

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

    return wx+8, wy+5       # Where the content of the box goes

def draw_info(game, window):
    x = 343
    score, level, lines = game.get_info()
    # x-len(str(score))*20 to align correctly according to number of digits
    window.blit(font.render(str(score), 1, BLACK), (x-(len(str(score))-1)*20, 61))
    window.blit(font.render(str(level), 1, BLACK), (x-(len(str(level))-1)*20, 141))
    window.blit(font.render(str(lines), 1, BLACK), (x-(len(str(lines))-1)*20, 201))

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

    # Create game surface
    screen = pygame.Surface(G_SIZE)

    # Create clock
    clock = pygame.time.Clock()

    # Create the Game
    game = Game()
    # block = game.new_block()
    block = BlockI()

    last_event = time.time()
    last_drop = time.time()

    while True:
        # Lock the game at default fps
        clock.tick(FPS)

        # Clear the screen
        screen.fill(WHITE)

        # Check if the user wants to quit
        process_quit()

        ### THIS WORKS BUT MAKE SURE YOU UNDERSTAND WHY
        ### MAKE SURE FOLLOWS GUIDELINES
        ### MAKE SURE YOU HAVE THE CORRECT DELAY
        # If the piece cannot move anymore, merge and generate a new one
        if (not block.can_move(game, DOWN)):
            if (block.hard_drop) or (time.time()-last_event > LOCK_DELAY):
                game.merge(block)
                block = game.new_block()
        # Else, process the keyboard input and move accordingly
        elif ((block.can_move(game, DOWN)) and (time.time() - last_drop > game.level.fall_speed)):
            block.move(DOWN)
            last_drop = time.time()

        last_event = process_input(block, game, last_event)

        # Draw the game and block to the screen
        game.draw(screen)
        block.draw(screen)

        # Process the lines
        game.remove_lines()

        # Redraw game and block to the screen (smoother line deletion)
        game.draw(screen)
        block.draw(screen)

        # Redraw everything
        ### Boxes
        score = draw_box(window, (276, 16, 112, 33))
        level = draw_box(window, (276, 116, 112, 55))
        lines = draw_box(window, (276, 176, 112, 55))
        queue = draw_box(window, (276, 251, 112, 112))
        # Draw score box
        pygame.draw.rect(window, WHITE, (263, 62, 138, 24))
        pygame.draw.line(window, WHITE, (263, 89), (400, 89), 3)
        ### Text
        window.blit(font.render("score", 1, BLACK), score)
        window.blit(font.render("level", 1, BLACK), level)
        window.blit(font.render("lines", 1, BLACK), lines)
        ### Draw the numbers
        draw_info(game, window)

        # Update score, level, lines, next piece
        # info.update()

        # Update the screen
        window.blit(screen, (40, 0))
        pygame.display.update()

if __name__ == "__main__":
    main()


