import pygame
from table import finished
import os
from config import *
from random import randint,choice,shuffle
import sys
from copy import deepcopy
Lbutton = pygame.image.load(os.path.join(RES, 'left.png'))
Rbutton = pygame.image.load(os.path.join(RES, 'right.png'))

class Agent:
    def __init__(self, player_id, algo=None, screen=None, table=None):
        self.INF = 70
        self.quanvalue = QUANVALUE
        self.player_id = player_id
        self.algo = algo
        self.screen = screen
        self.table = table

    def random_algo(self, state_game):
        pos = 0
        if self.player_id:
            while True:
                pos = randint(7, 11)
                if state_game[pos][0] != 0:
                    break
        else:
            while True:
                pos = randint(1, 5)
                if state_game[pos][0] != 0:
                    break
        
        return pos, choice(['Left', 'Right'])

    def human(self, state_game, cur_point):
        move = [None, None]
        old_box = 0
        self.table.redraw(0)
        x, y = 0, 0
        isClicked = False

        available_boxes = []
        for i in range(1,6):
            if state_game[i][0] > 0:
                available_boxes.append(i)

        while True:
            isClicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClicked = True


            if 240 < y < 340:
                if 160 < x < 260:
                    move[0] = 1
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(Lbutton, (165, 315))
                        self.screen.blit(Rbutton, (233, 315))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'Left' if x < 210 else 'Right'

                elif 260 < x < 360:
                    move[0] = 2
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(Lbutton, (265, 315))
                        self.screen.blit(Rbutton, (333, 315))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'Left' if x < 310 else 'Right'
                elif 360 < x < 460:
                    move[0] = 3
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(Lbutton, (360, 315))
                        self.screen.blit(Rbutton, (428, 315))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'Left' if x < 410 else 'Right'
                elif 460 < x < 560:
                    move[0] = 4
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(Lbutton, (460, 315))
                        self.screen.blit(Rbutton, (528, 315))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'Left' if x < 510 else 'Right'
                elif 560 < x < 660:
                    move[0] = 5
                    if move[0] not in available_boxes:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(Lbutton, (560, 315))
                        self.screen.blit(Rbutton, (628, 315))
                        old_box = move[0]

                    if isClicked:
                        move[1] = 'Left' if x < 610 else 'Right'
                else:
                    self.table.redraw(0)
                    old_box = 0

            else:
                self.table.redraw(0)
                old_box = 0

            pygame.display.flip()
            if move[0] is not None and move[1] is not None:
                break
        return move[0], move[1]

    def execute(self, state_game_, cur_point_, depth=3):
        state_game, cur_point = deepcopy(state_game_), deepcopy(cur_point_)

        if self.algo is None:  ## human play
            return self.human(state_game, cur_point)