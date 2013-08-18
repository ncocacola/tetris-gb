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
        # Zip an unzipped version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]

    # def print_to_screen(self):


class Piece(object):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[3][1] = 1
        self.state[4][1] = 1
        # self.state[y][x]

    def merge(self, Game):
        ## REWRITE THIS FUNCTION
        # self.print_to_console()
        # print ""
        # Game.print_to_console()

        foo = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        for row in range(len(Game.state)):
            for col in range(len(Game.state[row])):
                # If there is a clash, don't do anything

                ## REWRITE THIS PART USING THE 'checklist' method, else doesn't work
                if (Game.state[row][col] == 1) and (self.state[row][col] == 1):
                    return None
                # Else, merge the two arrays
                else:
                    foo[row][col] = Game.state[row][col] + self.state[row][col]
        Game.state = foo

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
            # print "y: " + str(y) + " x: " + str(x)
            if direction == "left" and (x-1) >= MIN_X:
                print "left"
                print x-1
                checklist.append(True)
            elif direction == "right" and (x+1) <= MAX_X:
                print "right"
                print x+1
                checklist.append(True)
            elif direction == "down" and (y+1) <= MAX_Y:
                print "down"
                print y+1
                checklist.append(True)

        return (len(checklist) == 4) and all(item == True for item in checklist)
            

    def move(self, direction):
        coordinates = self.get_coordinates()

        for x, y in coordinates:
            if direction == "left":
                self.state[x][y] = 0
                self.state[x-1][y] = 1
            elif direction == "right":
                self.state[x][y] = 0
                self.state[x+1][y] = 1
            elif direction == "down":
                self.state[x][y] = 0
                self.state[x][y+1] = 1

    def print_to_console(self):
        # Zip an unzipped version of self.state (zip(*self.state))
        # Apply the list() function to each resulting tuple to get a bunch of lists
        transpose = map(list, zip(*self.state))
        for row in range(len(transpose)):
            print transpose[row]

    # def print_to_screen(self)

def process_input(event):
    if (event.type == KEYDOWN):
        if event.key == pygame.K_LEFT:
            return "left"
        elif event.key == pygame.K_RIGHT:
            return "right"
        elif event.key == pygame.K_DOWN:
            return "down"

def main():
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
        # Lock the game at 50fps
        clock.tick(50)

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
        print direction
        if newPiece.can_move(Game, direction):
            newPiece.move(direction)


        # Merge it with current game state
        ## DO THIS ONLY ONCE THE PIECE HAS FALLEN AND OVER WITH
        newPiece.merge(Game)

        # Draw game to screen
        Game.draw(screen)


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


