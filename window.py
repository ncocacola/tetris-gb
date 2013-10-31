import os, pygame, sys, time
from pygame.locals import *

import block, game
from config import *

class Window(object):
    def __init__(self):
        # Create the window/Initialise
        pygame.display.set_caption("tetris")
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.board = pygame.Surface(BOARD_SIZE)
        self.clock = pygame.time.Clock()

        # self.state = SPLASH

        self.init()

    def init(self):
        # Create the game
        self.game = game.Game()
        self.state = PLAY
        self.ghost = True

        # Music (refactor this)
        pygame.mixer.music.play(-1)
        self.music = PLAY

        # Draw
        self.draw()

    # THE WHILE LOOP
    def main(self):
        self.clock.tick(FPS)
        self.board.fill(WHITE)

        self.listen_for_quit()

        # if self.state == SPLASH:
        #     self.draw_splashscreen()
        #     self.listen_for_start()
        # else:
        self.listen_for_pause()
        self.listen_for_ghost()
        self.listen_for_sound()
        self.listen_for_reset()

        self.listen_for_input()

        # Play
        if self.state == PLAY:
            if self.ghost:
                self.draw_ghost_block()
            self.game.advance()
            self.game.draw(self.board)

        # Check if the game is over
        if self.game.over():
            self.state = OVER

        self.redraw()

    # Drawing
    def draw(self):
        self.window.fill(BLACK)
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


    def draw_splashscreen(self):
        image = pygame.image.load(os.path.join(ASSETS_DIR, "splash.png"))
        self.window.blit(image, (0, 0))


    def draw_board(self):
        self.window.blit(self.board, (40, -40))
    def draw_paused(self):
        paused = pygame.Surface(BOARD_SIZE)
        paused.fill(WHITE)

        paused.blit(font.render("hit p", 1, BLACK), (30, 50))
        paused.blit(font.render("to", 1, BLACK), (30, 70))
        paused.blit(font.render("continue", 1, BLACK), (30, 90))
        paused.blit(font.render("game", 1, BLACK), (30, 110))

        paused.blit(font.render("p   pause", 1, BLACK), (30, 170))
        paused.blit(font.render("q   quit", 1, BLACK), (30, 190))
        paused.blit(font.render("r   reset", 1, BLACK), (30, 210))

        paused.blit(font.render("s   sound", 1, BLACK), (30, 250))
        paused.blit(font.render("g   ghost", 1, BLACK), (30, 270))

        self.window.blit(paused, (40, 0))
    def draw_over(self):
        over = pygame.Surface(BOARD_SIZE)
        over.fill(WHITE)

        self.box(over, (30, 50, 140, 100), True)

        over.blit(font.render("game", 1, BLACK), (60, 70))
        over.blit(font.render("over", 1, BLACK), (60, 100))

        over.blit(font.render("thanks", 1, BLACK), (40, 180))
        over.blit(font.render("for", 1, BLACK), (70, 210))
        over.blit(font.render("playing", 1, BLACK), (30, 240))

        over.blit(font.render("r to reset", 1, BLACK), (15, 300))

        self.window.blit(over, (40, 0))

    def draw_bricks(self):
        self.window.blit(BRICKS, (20, 0))
        self.window.blit(BRICKS, (240, 0))
        pygame.draw.line(self.window, WHITE, (18, 0), (18, 400), 3)
        pygame.draw.line(self.window, WHITE, (261, 0), (261, 400), 3)
    def draw_sidebar(self):
        self.draw_score(self.game.score)
        self.draw_level(self.game.level.n)
        self.draw_lines(self.game.lines)
        self.draw_queue(self.game.next_block)
    
    def draw_ghost_block(self):
        # Copy the block (deep copy won't work)
        ghost_block = type(self.game.block)()
        ghost_block.tiles=[]
        for tile in self.game.block.tiles:
            ghost_block.tiles.append(block.Tile(tile.type, tile.x, tile.y))
        ghost_block.hard_drop(self.game)
        ghost_block.draw(self.board, True)

    # Functions for sidebar
    def draw_score(self, score):
        # Box under score
        pygame.draw.line(self.window, WHITE, (263, 38), (400, 38), 3)
        pygame.draw.rect(self.window, GREY, (263, 40, 137, 17))
        pygame.draw.line(self.window, WHITE, (263, 58), (400, 58), 3)
        # Box for actual score
        pygame.draw.rect(self.window, WHITE, (263, 62, 138, 24))
        pygame.draw.line(self.window, WHITE, (263, 89), (400, 89), 3)
        # Box & title
        self.box(self.window, (276, 16, 112, 33))
        self.window.blit(font.render("score", 1, BLACK), (284, 21))
        # Actual score
        self.window.blit(font.render(str(score), 1, BLACK), (self.align(score), 61))
    def draw_level(self, level):
        # Box & title
        self.box(self.window, (276, 116, 112, 55))
        self.window.blit(font.render("level", 1, BLACK), (284, 121))
        # Actual level
        self.window.blit(font.render(str(level), 1, BLACK), (self.align(level), 141))
    def draw_lines(self, lines):
        # Box & title
        self.box(self.window, (276, 176, 112, 55))
        self.window.blit(font.render("lines", 1, BLACK), (284, 181))
        # Actual lines
        self.window.blit(font.render(str(lines), 1, BLACK), (self.align(lines), 201))
    def draw_queue(self, next_block):
        # Box & title
        self.box(self.window, (276, 251, 112, 112))
        self.window.blit(font.render("queue", 1, BLACK), (284, 256))
        # Actual next block
        if self.state == PLAY:
            for tile in next_block.tiles:
                x, y = tile.x-4, tile.y-2
                location = map(sum, zip((x*CELL_W, y*CELL_H), (310, 316)))
                self.window.blit(tile.type.image, location)

    # Keyboard: TODO Refactor all of these
    # listen_for_input() doesn't have post(event) because it runs after 
    # all the others in the loop
    def listen_for_quit(self):
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
    def listen_for_start(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                print "YESBOS"
                self.init()
            # Return the event if not quitting
            else:
                pygame.event.post(event)

    def listen_for_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Keyboard
                if (event.key == pygame.K_p):
                    if self.state == PLAY:
                        self.state = PAUSE
                        if self.music == PLAY:
                            self.music = PAUSE
                            pygame.mixer.music.pause()
                    elif self.state == PAUSE:
                        pygame.event.clear()
                        self.state = PLAY
                        if self.music == PAUSE:
                            self.music = PLAY
                            pygame.mixer.music.unpause()
                else:
                    pygame.event.post(event)
    def listen_for_ghost(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_g):
                    self.ghost = not (self.ghost)
            pygame.event.post(event)
    def listen_for_sound(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_s):
                    if self.music == PLAY:
                        self.music = OVER
                        pygame.mixer.music.stop()
                    elif self.music == OVER:
                        self.music = PLAY
                        pygame.mixer.music.play()
            pygame.event.post(event)
    def listen_for_reset(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_r):
                    if not (self.state == PAUSE):
                        # rewind() doesn't work
                        pygame.mixer.music.stop()
                        pygame.mixer.music.play()
                        self.game = game.Game()
                        self.state = PLAY
            pygame.event.post(event)

    # Can you generalise this?
    def listen_for_input(self):
        # Discrete key presses
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    self.game.block.hard_drop(self.game)
                elif (event.key == pygame.K_UP):
                    if self.game.block.can_rotate(self.game):
                        self.game.block.rotate()
                elif (event.key == pygame.K_LEFT):
                    if self.game.block.can_move(self.game, LEFT):
                        self.game.block.move(LEFT)
                elif (event.key == pygame.K_RIGHT):
                    if self.game.block.can_move(self.game, RIGHT):
                        self.game.block.move(RIGHT)
                elif (event.key == pygame.K_DOWN):
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
                self.game.block.soft_points += 1
                self.game.last_event = time.time()


    # Helper functions
    def box(self, surface, (ox, oy, ow, oh), black=False):
        t = 3 # 'Thickness' of the box
        ix, iy = ox+t, oy+t
        iw, ih = ow-(2*t), oh-(2*t)

        outer_box = [(ox-t, oy+t), (ox, oy+t), (ox, oy),
                     (ox+ow-t, oy), (ox+ow-t, oy+t), (ox+ow, oy+t),
                     (ox+ow, oy+oh-t), (ox+ow-t, oy+oh-t), (ox+ow-t, oy+oh),
                     (ox, oy+oh), (ox, oy+oh-t), (ox-t, oy+oh-t)]
        inner_box = [(ix-t, iy+t), (ix, iy+t), (ix, iy),
                     (ix+iw-t, iy), (ix+iw-t, iy+t), (ix+iw, iy+t),
                     (ix+iw, iy+ih-t), (ix+iw-t, iy+ih-t), (ix+iw-t, iy+ih),
                     (ix, iy+ih), (ix, iy+ih-t), (ix-t, iy+ih-t)]

        if black:
            bx, by = ox-t, oy-t
            bw, bh = ow+(2*t), oh+(2*t)

            black_box = [(bx-t, by+t), (bx, by+t), (bx, by),
                         (bx+bw-t, by), (bx+bw-t, by+t), (bx+bw, by+t),
                         (bx+bw, by+bh-t), (bx+bw-t, by+bh-t), (bx+bw-t, by+bh),
                         (bx, by+bh), (bx, by+bh-t), (bx-t, by+bh-t)]

            pygame.draw.polygon(surface, BLACK, black_box, 3)

        pygame.draw.polygon(surface, WHITE, outer_box, 0)
        pygame.draw.polygon(surface, GREY, inner_box, 3)
    def align(self, nb):
        x = 343
        n = len(str(nb))
        if n <= 4:
            return x-(n-1)*20
        else:
            return x-60-(n-5)*10
