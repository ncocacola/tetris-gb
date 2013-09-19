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

def main():
    # Initialise the game engine
    pygame.init()
    # Create the window/game/b
    window = Window()

    while True:
        window.while_loop()

if __name__ == "__main__":
    main()


