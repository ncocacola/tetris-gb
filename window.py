import pygame, time, os
import pyglet
from pygame.locals import *
from config import *

class Window(object):
    def __init__(self, next_block):
        # Create the window
        self.surface = pygame.display.set_mode(W_SIZE)
        pygame.display.set_caption("nitris")

        # Start music
        self.play_music()

        # Draw elements
        self.draw_bricks()
        self.draw_sidebar((0, 0, 0), next_block)

    # Music stuff
    def play_music(self):
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, "music/tetris-gb.mid"))
        pygame.mixer.music.play(-1)

    # Drawing stuff
    def draw_board(self, board):
        self.surface.blit(board, (40, 0))
    def draw_paused(self):
        paused = pygame.Surface(G_SIZE)
        paused.fill(WHITE)

        paused.blit(font.render("hit p", 1, BLACK), (30, 50))
        paused.blit(font.render("to", 1, BLACK), (30, 70))
        paused.blit(font.render("continue", 1, BLACK), (30, 90))
        paused.blit(font.render("game", 1, BLACK), (30, 110))

        paused.blit(font.render("p   pause", 1, BLACK), (30, 170))
        paused.blit(font.render("q   quit", 1, BLACK), (30, 190))
        paused.blit(font.render("s   sound", 1, BLACK), (30, 210))

        self.surface.blit(paused, (40, 0))

    def draw_bricks(self):
        bricks = pygame.image.load(os.path.join(ASSETS_DIR, "bricks.png"))
        self.surface.blit(bricks, (20, 0))
        self.surface.blit(bricks, (240, 0))
        pygame.draw.line(self.surface, WHITE, (18, 0), (18, 400), 3)
        pygame.draw.line(self.surface, WHITE, (261, 0), (261, 400), 3)
    def draw_sidebar(self, (score, level, lines), next_block=None):
        self.draw_score(score)
        self.draw_level(level)
        self.draw_lines(lines)
        self.draw_queue(next_block)

    def draw_score(self, score):
        # Box under score
        pygame.draw.line(self.surface, WHITE, (263, 38), (400, 38), 3)
        pygame.draw.rect(self.surface, GREY, (263, 40, 137, 17))
        pygame.draw.line(self.surface, WHITE, (263, 58), (400, 58), 3)
        # Box for actual score
        pygame.draw.rect(self.surface, WHITE, (263, 62, 138, 24))
        pygame.draw.line(self.surface, WHITE, (263, 89), (400, 89), 3)
        # Box & title
        self.draw_box(self.surface, (276, 16, 112, 33))
        self.surface.blit(font.render("score", 1, BLACK), (284, 21))
        # Actual score
        self.surface.blit(font.render(str(score), 1, BLACK), (self.align(score), 61))
    def draw_level(self, level):
        # Box & title
        self.draw_box(self.surface, (276, 116, 112, 55))
        self.surface.blit(font.render("level", 1, BLACK), (284, 121))
        # Actual level
        self.surface.blit(font.render(str(level), 1, BLACK), (self.align(level), 141))
    def draw_lines(self, lines):
        # Box & title
        self.draw_box(self.surface, (276, 176, 112, 55))
        self.surface.blit(font.render("lines", 1, BLACK), (284, 181))
        # Actual lines
        self.surface.blit(font.render(str(lines), 1, BLACK), (self.align(lines), 201))
    def draw_queue(self, next_block):
        # Box & title
        self.draw_box(self.surface, (276, 251, 112, 112))
        self.surface.blit(font.render("queue", 1, BLACK), (284, 256))
        # Actual next block
        if next_block:
            for tile in next_block.tiles:
                x, y = tile.x-4, tile.y-2
                location = map(sum, zip((x*CELL_W, y*CELL_H), (310, 316)))
                self.surface.blit(tile.block.image, location)

    # Miscellaneous
    def draw_box(self, window, (wx, wy, ww, wh)):
        t = 3 # 'Thickness' of the box
        bx, by = wx+t, wy+t
        bw, bh = ww-(2*t), wh-(2*t)
        outer_box = [(wx-t, wy+t), (wx, wy+t), (wx, wy),
                     (wx+ww-t, wy), (wx+ww-t, wy+t), (wx+ww, wy+t),
                     (wx+ww, wy+wh-t), (wx+ww-t, wy+wh-t), (wx+ww-t, wy+wh),
                     (wx, wy+wh), (wx, wy+wh-t), (wx-t, wy+wh-t)]
        inner_box = [(bx-t, by+t), (bx, by+t), (bx, by), 
                     (bx+bw-t, by), (bx+bw-t, by+t), (bx+bw, by+t),
                     (bx+bw, by+bh-t), (bx+bw-t, by+bh-t), (bx+bw-t, by+bh), 
                     (bx, by+bh), (bx, by+bh-t), (bx-t, by+bh-t)]
        pygame.draw.polygon(window, WHITE, outer_box, 0)
        pygame.draw.polygon(window, GREY, inner_box, 3)
    def align(self, nb):
        x = 343
        n = len(str(nb))
        if n <= 4:
            return x-(n-1)*20
        else:
            return x-60-(n-5)*10
