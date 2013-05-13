import pygame
from pygame.locals import *

# Initialise the game engine
pygame.init()

# Window size
WIDTH, HEIGHT = 800, 600
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

# Loop until quit
running = 1
while running:
    event = pygame.event.poll()
    # Close the window
    if event.type == pygame.QUIT:
        running = 0
    # Black background
    screen.fill(BLACK)
    
    # pygame.draw.circle(screen, WHITE, W_CENTER, 100)
    # pygame.draw.line(screen, (255, 255, 255), (639, 0), (0, 0))


    # Update full display surface
    pygame.display.flip()
