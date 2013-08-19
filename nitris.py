#!/usr/bin/env python

import sys
import pygame
from pygame.locals import *
from numpy import matrix

## GLOBAL VARIABLES
# Window size
WIDTH, HEIGHT = 200, 400
CELL_W, CELL_H = WIDTH/10, HEIGHT/20
ARRAY_X, ARRAY_Y = WIDTH/20, HEIGHT/20
W_SIZE   = (WIDTH, HEIGHT)
W_CENTER = (WIDTH/2, HEIGHT/2)
MIN_X, MAX_X, MIN_Y, MAX_Y = 0, ARRAY_X-1, 0, ARRAY_Y-1

# Usual colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

# Frames per second
FPS = 50

# Move ticker
## http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
## TODO MOVE_TICKER should not be capital as it varies
MOVE_TICKER = 0
MOVE_TICKER_DEFAULT = 10 # Allow a move every 'FPS/5' (= 10) frames = every 0.2 second

class Tetris(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]    # 10 * 20 array of ints
        self.level = 1
        self.lines = 0
        self.score = 0

    def draw(self, surface):    
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                if self.state[col][row] == 1:
                    pygame.draw.rect(surface, WHITE, (CELL_W*col, CELL_H*row, CELL_W, CELL_H))


    def print_to_console(self):
        # Zip an unpacked version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]


class Piece(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[3][1] = 1
        self.state[4][1] = 1

    # Rewrite this function and use it to merge once the piece has fallen down
    # def merge(self, Game):
    #     foo = [[0]*ARRAY_Y for i in range(ARRAY_X)]
    #     for row in range(len(Game.state)):
    #         for col in range(len(Game.state[row])):
    #             # If there is a clash, don't do anything

    #             ## REWRITE THIS PART USING THE 'checklist' method, else doesn't work
    #             if (Game.state[row][col] == 1) and (self.state[row][col] == 1):
    #                 return None
    #             # Else, merge the two arrays
    #             else:
    #                 foo[row][col] = Game.state[row][col] + self.state[row][col]
    #     Game.state = foo

    def draw(self, surface):    
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                if self.state[col][row] == 1:
                    pygame.draw.rect(surface, WHITE, (CELL_W*col, CELL_H*row, CELL_W, CELL_H))

    def get_coordinates(self):
        coordinates = []
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == 1:
                    coordinates.append((row, col))
        return sorted(coordinates, key=lambda k: k[0])
        # Sort coordinates from left to right (x-coordinate)

    def can_move(self, Game, direction):
        # Only checks that piece stays in the game boundaries
        coordinates = self.get_coordinates()
        checklist = []

        for x, y in coordinates:
            if direction == "left" and (x-1) >= MIN_X:
                checklist.append(True)
            elif direction == "right" and (x+1) <= MAX_X:
                checklist.append(True)
            elif direction == "down" and (y+1) <= MAX_Y:
                checklist.append(True)
            # TODO Remove this later
            elif direction == "up" and (y-1) >= MIN_Y:
                checklist.append(True)

        return (len(checklist) == 4) and all(item == True for item in checklist)
            

    def move(self, direction):
        coordinates = self.get_coordinates()
        print coordinates

        if direction == "left":
            for x, y in coordinates:
                self.state[x][y] = 0
                self.state[x-1][y] = 1
        elif direction == "right":
            # Reverse the array to go through coordinates right-to-left
            # [::-1] ==> [start:stop:step]
            for x, y in coordinates[::-1]:
                self.state[x][y] = 0
                self.state[x+1][y] = 1
        elif direction == "down":
            for x, y in coordinates:
                self.state[x][y] = 0
                self.state[x][y+1] = 1
        # TODO Remove this later
        elif direction == "up":
            for x, y in coordinates:
               self.state[x][y] = 0
               self.state[x][y-1] = 1 

    def print_to_console(self):
        # Zip an unzipped version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]

    # def print_to_screen(self)

def process_input(event):
    # TODO do some refactoring and get rid of this 'global'
    global MOVE_TICKER

    if (event.type == KEYDOWN):
        if MOVE_TICKER == 0:
            MOVE_TICKER = MOVE_TICKER_DEFAULT
            if event.key == pygame.K_LEFT:
                # if MOVE_TICKER == 0:
                #     MOVE_TICKER = MOVE_TICKER_DEFAULT
                return "left"
            elif event.key == pygame.K_RIGHT:
                # if MOVE_TICKER == 0:
                    # MOVE_TICKER = MOVE_TICKER_DEFAULT
                return "right"
            elif event.key == pygame.K_DOWN:
                # if MOVE_TICKER == 0:
                    # MOVE_TICKER = MOVE_TICKER_DEFAULT
                return "down"
            # TODO Remove this later
            elif event.key == pygame.K_UP:
                # if MOVE_TICKER == 0:
                    # MOVE_TICKER = MOVE_TICKER_DEFAULT
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
    # background = pygame.image.load('game.png').convert()

    # Create clock
    clock = pygame.time.Clock()

    Game = Tetris()
    newPiece = Piece()

    # for i in range(1):
    while True:
        # Lock the game at default fps
        clock.tick(FPS)

        if MOVE_TICKER > 0:
            MOVE_TICKER -= 1

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Clear the screen
        screen.fill(BLACK)

        # Spawn a new piece

        ## Move piece
        # Where is it trying to go?
        # print newPiece.get_coordinates()

        direction = process_input(event)

        if (direction is not None):
            print direction
        
        if newPiece.can_move(Game, direction):
            newPiece.move(direction)


        # Merge it with current game state
        ## DO THIS ONLY ONCE THE PIECE HAS FALLEN AND OVER WITH
        # newPiece.merge(Game)

        # Draw game to screen
        Game.draw(screen)
        newPiece.draw(screen)


        # if not(mergeGamePiece(game, piece) is None):
        #     gp = mergeGamePiece(game, piece)
        # drawGame(screen, gp)
        # Move objects...
        # Draw objects...
        # screen.blit(background, (100,100)).l.

        # Update the screen
        pygame.display.flip()

if __name__ == "__main__":
    main()


