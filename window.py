import pygame, time, os, sys
import pyglet
from pygame.locals import *
from config import *
# from game import *
import game

class Window(object):
    def __init__(self):
        # Create the window
        self.surface = pygame.display.set_mode(W_SIZE)
        pygame.display.set_caption("nitris")

        # ...
        self.board = pygame.Surface(G_SIZE)
        self.clock = pygame.time.Clock()

        # Create the game
        self.game = game.Game()

        # Start music (refactor this)
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, "music/tetris-gb.wav"))
        pygame.mixer.music.play(-1)
        self.state = PLAY
        self.music = PLAY


        # Draw elements
        self.draw()


    # Keyboard stuff (https://github.com/acchao/tetromino_andrew/)
    def process_quit(self):
        def quit():
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Mouse
                quit()
            elif event.type == pygame.KEYUP:  # Keyboard
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_q):
                    quit()
            # Return the event if not quitting
            else:
                pygame.event.post(event)
    # Rewrite this!
    def process_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Keyboard
                if (event.key == pygame.K_p):
                    if self.state == PLAY:
                        self.state = PAUSE
                        if self.music == PLAY:
                            self.music = PAUSE
                            pygame.mixer.music.pause()
                    elif self.state == PAUSE:
                        self.state = PLAY
                        if self.music == PAUSE:
                            self.music = PLAY
                            pygame.mixer.music.unpause()
                else:
                    pygame.event.post(event)

    # Rewrite this, move can_rotate into game
    # Check why you can hard_drop while paused
    def process_input(self):
        # Discrete key presses
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    self.game.block.drop_hard(self.game)
                elif event.key == pygame.K_UP:
                    if self.game.block.can_rotate(self.game):
                        self.game.block.rotate()
                elif (event.key == pygame.K_LEFT):
                    if self.game.block.can_move(self.game, LEFT):
                        self.game.block.move(LEFT)
                elif event.key == pygame.K_RIGHT:
                    if self.game.block.can_move(self.game, RIGHT):
                        self.game.block.move(RIGHT)
                elif event.key == pygame.K_DOWN:
                    if self.game.block.can_move(self.game, DOWN):
                        self.game.block.move(DOWN)
                self.game.last_event = time.time()
                break
        # Continuous key presses
        keystate = pygame.key.get_pressed()
        if keystate[K_DOWN]:
            if time.time() - self.game.last_event >= SOFT_DROP_SPEED:
                if self.game.block.can_move(self.game, DOWN):
                    self.game.block.move(DOWN)
                self.game.block.soft_drop += 1
                self.game.last_event = time.time()

    # Drawing stuff
    def draw(self):
        self.draw_bricks()
        self.draw_board()
        self.draw_sidebar()
    def redraw(self):
        if self.state == PLAY:
            self.draw_board()
        elif self.state == PAUSE:
            self.draw_paused()
        elif self.state == OVER:
            self.draw_over()

        self.draw_sidebar()

    def draw_board(self):
        self.surface.blit(self.board, (40, 0))
    def draw_paused(self):
        paused = pygame.Surface(G_SIZE)
        paused.fill(WHITE)

        paused.blit(font.render("hit p", 1, BLACK), (30, 50))
        paused.blit(font.render("to", 1, BLACK), (30, 70))
        paused.blit(font.render("continue", 1, BLACK), (30, 90))
        paused.blit(font.render("game", 1, BLACK), (30, 110))

        paused.blit(font.render("p   pause", 1, BLACK), (30, 170))
        paused.blit(font.render("q   quit", 1, BLACK), (30, 190))
        # paused.blit(font.render("s   sound", 1, BLACK), (30, 210))

        self.surface.blit(paused, (40, 0))
    def draw_over(self):
        paused = pygame.Surface(G_SIZE)
        paused.fill(WHITE)

        paused.blit(font.render("game", 1, BLACK), (30, 50))
        paused.blit(font.render("over", 1, BLACK), (30, 70))

        self.surface.blit(paused, (40, 0))

    def draw_bricks(self):
        bricks = pygame.image.load(os.path.join(ASSETS_DIR, "bricks.png"))
        self.surface.blit(bricks, (20, 0))
        self.surface.blit(bricks, (240, 0))
        pygame.draw.line(self.surface, WHITE, (18, 0), (18, 400), 3)
        pygame.draw.line(self.surface, WHITE, (261, 0), (261, 400), 3)
    def draw_sidebar(self):
        self.draw_score(self.game.score)
        self.draw_level(self.game.level.n)
        self.draw_lines(self.game.lines)
        self.draw_queue(self.game.next_block)

    # Functions for sidebar
    def draw_score(self, score):
        # Box under score
        pygame.draw.line(self.surface, WHITE, (263, 38), (400, 38), 3)
        pygame.draw.rect(self.surface, GREY, (263, 40, 137, 17))
        pygame.draw.line(self.surface, WHITE, (263, 58), (400, 58), 3)
        # Box for actual score
        pygame.draw.rect(self.surface, WHITE, (263, 62, 138, 24))
        pygame.draw.line(self.surface, WHITE, (263, 89), (400, 89), 3)
        # Box & title
        self.box(self.surface, (276, 16, 112, 33))
        self.surface.blit(font.render("score", 1, BLACK), (284, 21))
        # Actual score
        self.surface.blit(font.render(str(score), 1, BLACK), (self.align(score), 61))
    def draw_level(self, level):
        # Box & title
        self.box(self.surface, (276, 116, 112, 55))
        self.surface.blit(font.render("level", 1, BLACK), (284, 121))
        # Actual level
        self.surface.blit(font.render(str(level), 1, BLACK), (self.align(level), 141))
    def draw_lines(self, lines):
        # Box & title
        self.box(self.surface, (276, 176, 112, 55))
        self.surface.blit(font.render("lines", 1, BLACK), (284, 181))
        # Actual lines
        self.surface.blit(font.render(str(lines), 1, BLACK), (self.align(lines), 201))
    def draw_queue(self, next_block):
        # Box & title
        self.box(self.surface, (276, 251, 112, 112))
        self.surface.blit(font.render("queue", 1, BLACK), (284, 256))
        # Actual next block
        if next_block:
            for tile in next_block.tiles:
                x, y = tile.x-4, tile.y-2
                location = map(sum, zip((x*CELL_W, y*CELL_H), (310, 316)))
                self.surface.blit(tile.block.image, location)

    # Helper functions
    def box(self, window, (wx, wy, ww, wh)):
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


    # THE WHILE LOOP
    def while_loop(self):
        self.clock.tick(FPS)
        self.board.fill(WHITE)

        self.process_quit()
        self.process_pause()

        if self.state == PLAY:
            self.play()

        self.redraw()
        pygame.display.update()

    def play(self):
        self.process_input()

        self.game.block.ghost(self.game, self.board)

        self.game.advance()

        # Remove completed lines & Update global info
        self.game.draw(self.board)
        
        # Check that the game is not over
        self.game.check_over(self.game.block)


