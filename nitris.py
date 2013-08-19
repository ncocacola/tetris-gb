#!/usr/bin/env python

## http://tetris.wikia.com/wiki/Tetris_Guideline

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
MOVE_TICKER_DEFAULT = 10 # Allow a move every 10 frames = every 0.2 second

class Tetris(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]    # 10 * 20 array of ints
        self.level = 1
        self.lines = 0
        self.score = 0

    def merge(self, Tetronimo):
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                self.state[col][row] += Tetronimo.state[col][row]

    def draw(self, surface):    
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                if self.state[col][row] == 1:
                    pygame.draw.rect(surface, BLUE, (CELL_W*col, CELL_H*row, CELL_W, CELL_H))

    def console(self):
        # Zip an unpacked version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]

class Tetronimo(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[3][1] = 1
        self.state[4][1] = 1

    def get_coordinates(self):
        coordinates = []
        for row in range(len(self.state)):
            for col in range(len(self.state[row])):
                if self.state[row][col] == 1:
                    coordinates.append((row, col))
        return sorted(coordinates, key=lambda k: k[0])
        # Sort coordinates from left to right (x-coordinate)

    def can_move(self, Game, direction):
        # TODO Only checks that piece stays in the game boundaries
        # TODO Get it to check if other piece are not obstructing
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

    def has_finished(self, Game):
        coordinates = self.get_coordinates()

        # If the piece has reached the bottom
        if any(y == MAX_Y for y in [y for x, y in coordinates]):
            return True
        # Elif the piece has fallen on top of other blocks
        elif any(Game.state[x][y+1] == 1 for x, y in coordinates):
            return True
        # Return False in the default case
        else:
            return False

    def draw(self, surface):    
        for col in range(len(self.state)):
            for row in range(len(self.state[col])):
                if self.state[col][row] == 1:
                    pygame.draw.rect(surface, BLUE, (CELL_W*col, CELL_H*row, CELL_W, CELL_H))
    
    def console(self):
        # Zip an unzipped version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]

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


