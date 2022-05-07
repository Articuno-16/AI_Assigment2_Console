from time import sleep
import pygame,sys
import os
from agent import Agent

from GUI import TableGUI
from config import *

def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e

class Game:
    def __init__(self, algo_0=None, algo_1=None):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.players = [Agent(0, algo_0, self.screen, self.table), Agent(1, algo_1, self.screen, self.table)]
        self.move = None

    def redraw(self, turn):
        self.table.redraw(turn)
    
    def finished(self):
        return self.table.finished()

    def update(self,turn, move):
        # Chỉnh lại khúc này
        self.table.movingTurn('player{}'.format(turn),move[0],move[1])

    def run(self):
        # User go first or agent go first
        turn = 0 if USER_GO_FIRST else 1
        running = True

        # Game loop
        self.redraw(turn)
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit();sys.exit()					
            move = self.players[turn].execute(self.table.state, self.table.playerScore)
            print(move)
            self.update(turn,move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")
            sleep(1)
            turn ^= 1
            self.redraw(turn)
            print(self.table)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()