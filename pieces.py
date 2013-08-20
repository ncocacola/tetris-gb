import pygame
from config import *

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

class TetroI(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[3][1] = 1
        self.state[4][1] = 1

class TetroO(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[1][2] = 1
        self.state[2][1] = 1
        self.state[2][2] = 1

class TetroT(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[2][2] = 1
        self.state[3][1] = 1

class TetroS(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][2] = 1
        self.state[2][1] = 1
        self.state[2][2] = 1
        self.state[3][1] = 1

class TetroZ(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[2][1] = 1
        self.state[2][2] = 1
        self.state[3][2] = 1

class TetroJ(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[1][1] = 1
        self.state[1][2] = 1
        self.state[2][2] = 1
        self.state[3][2] = 1

class TetroL(Tetronimo):
    def __init__(self):
        self.state = [[0]*ARRAY_Y for i in range(ARRAY_X)]
        self.state[3][1] = 1
        self.state[1][2] = 1
        self.state[2][2] = 1
        self.state[3][2] = 1






