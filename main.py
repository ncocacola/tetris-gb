import pygame
from pygame.locals import *

# Initialise Pygame modules
pygame.init()

# Create window
screen = pygame.display.set_mode((640,480))

# Loop until quit
running = 1
while running:
    event = pygame.event.poll()
    # Close the window
    if event.type == pygame.QUIT:
        running = 0
    # Black background
    screen.fill((0,0,0))
    pygame.display.flip()