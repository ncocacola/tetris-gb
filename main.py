import sys
import pygame
from pygame.locals import *

# TODO Abstract away from drawing pieces -- pieces should be matrices?

def drawIBlock(surface, color, x, y):
    pygame.draw.rect(surface, color, (x, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x, y+CELL_H, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x, y+2*CELL_H, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x, y+3*CELL_H, CELL_W, CELL_H))

def drawOBlock(surface, color, x, y):
    pygame.draw.rect(surface, color, (x, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x, y+CELL_H, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y+CELL_H, CELL_W, CELL_H))

def drawZBlock(surface, color, x, y):
    pygame.draw.rect(surface, color, (x, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y+CELL_H, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+2*CELL_W, y+CELL_H, CELL_W, CELL_H))

def drawTBlock(surface, color, x, y):
    pygame.draw.rect(surface, color, (x, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+2*CELL_W, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y+CELL_H, CELL_W, CELL_H))

def drawLBlock(surface, color, x, y):
    pygame.draw.rect(surface, color, (x, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x, y+CELL_H, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+CELL_W, y, CELL_W, CELL_H))
    pygame.draw.rect(surface, color, (x+2*CELL_W, y, CELL_W, CELL_H))

# Initialise the game engine
pygame.init()

# Window size
WIDTH, HEIGHT = 200, 400
CELL_W, CELL_H = WIDTH/10, HEIGHT/20
W_SIZE   = (WIDTH, HEIGHT)
W_CENTER = (WIDTH/2, HEIGHT/2)

# Usual colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

# Create window
screen = pygame.display.set_mode(W_SIZE)
# background = pygame.image.load('game.png').convert()
pygame.display.set_caption("Tetris")

# Create clock
clock = pygame.time.Clock()

# box_x = 100
# box_y = 200
# box_dir_x = 2
# box_dir_y = 1

# Loop until quit
while True:
    # Lock the game at 50fps
    clock.tick(50)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Clear the screen
    screen.fill(BLACK)

    # Check input

    # Move objects...
    # box_x += box_dir_x
    # if box_x >= WIDTH-20:
    #     box_x = WIDTH-20
    #     box_dir_x = -2
    # elif box_x <= 0:
    #     box_x = 0
    #     box_dir_x = 2

    # box_y += box_dir_y
    # if box_y >= HEIGHT-20:
    #     box_y = HEIGHT-20
    #     box_dir_y = -4
    # elif box_y <= 0:
    #     box_y = 0
    #     box_dir_y = 4

    # box_y += box_dir_y
    # if box_y >= HEIGHT-20:
    #     box_y = HEIGHT-20

    # Draw objects...
    # screen.blit(background, (100,100))
    # pygame.draw.rect(screen, color, (x,y,width,height), thickness)
    # pygame.draw.line(screen, WHITE, (100, 0), (100, 400))
    # pygame.draw.line(screen, WHITE, (0, 200), (200, 200))

    # pygame.draw.rect(screen, RED, (box_x, 190, 20, 20))
    # pygame.draw.rect(screen, RED, (90, box_y, 20, 20))
    # drawIBlock(screen, BLUE, 0, 0)
    # drawOBlock(screen, RED, 0, 0)
    # drawZBlock(screen, WHITE, 0, 0)
    # drawTBlock(screen, GREEN, 0, 0)
    # drawLBlock(screen, RED, 0, 0)

    # Update the screen
    # print str(box_x) + ", " + str(box_y)
    pygame.display.flip()



