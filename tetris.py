#!/usr/bin/env python

import pygame
from window import *

## http://tetris.wikia.com/wiki/Tetris_Guideline
## http://stackoverflow.com/questions/1969005/enumerations-in-python (Objects with functionality)

## Keyboard stuff: https://github.com/acchao/tetromino_andrew/
## Random Generator: http://tetris.wikia.com/wiki/Random_Generator
## Super Rotation System: http://tetris.wikia.com/wiki/SRS

if __name__ == "__main__":
    # Initialise the game engine
    pygame.init()
    # Create the window/game/b
    window = Window()

    while True:
        window.main()
        pygame.display.update()
