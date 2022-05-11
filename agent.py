import pygame
import time
from table import *
import os
from GUI import RES,QUANVALUE
from random import randint,choice,shuffle
import sys
from copy import deepcopy
Lbutton = pygame.image.load(os.path.join(RES, 'left.png'))
Rbutton = pygame.image.load(os.path.join(RES, 'right.png'))
NUM_SQUARE = 12
QUAN_1 = 5
QUAN_2 = 11
class Agent:
    def __init__(self, player_id, screen=None, table=None):
        self.INF = 70
        self.quanvalue = QUANVALUE
        self.player_id = player_id
        self.screen = screen
        self.table = table
        
class RandomAgent(Agent):
    def __init__(self, player_id, screen, table):
        super().__init__(player_id, screen, table)
    def execute(self,state_game):
        pos = 0
        available_boxes = []
        if self.player_id == "player2":
            for i in range(6,10):
                if state_game[i][0] > 0:
                    available_boxes.append(i)
            if(len(available_boxes) == 0):
                self.table.borrow("player2")
                available_boxes = range(6,11)
            pos = choice(available_boxes)
             
        else:
            for i in range(0,5):
                if state_game[i][0] > 0:
                    available_boxes.append(i)
            if(len(available_boxes) == 0):
                self.table.borrow("player1")
                available_boxes = range(0,5)
            pos = choice(available_boxes)
        print(pos, choice(['Left', 'Right']))
        return pos, choice(['Left', 'Right'])

class Minimax(Agent):
    def __init__(self, player_id, screen, table, depth):
        super().__init__(player_id, screen, table)
        self.pid = 0 if player_id == "player1" else 1
        self.depth = depth
        
    # Check if two kings are not eaten: 
    # Input: state
    # Output: bool value decides gameover
    #def finished(self,_state):
    #    return _state[QUAN_2] == [0, 0] and _state[QUAN_1] == [0, 0]
    
    # Check Nợ quân: (new_state, new_point)
    def handleBorrowStack(self,_state_game,_player_score):
        state, player_score = deepcopy(_state_game), deepcopy(_player_score)

        if not any([i[0] for i in state[0:QUAN_1]]):
            player_score[0] -= 5

            for i in range(0,QUAN_1):
                state[i][0] = 1
        
        if not any([i[0] for i in state[QUAN_1+1:QUAN_2]]):
            player_score[1] -= 5

            for i in range(QUAN_1+1,QUAN_2):
                state[i][0] = 1
        return state, player_score
    
    # Get Final Result and Winner: (Bool,point)
    def getResult(self, state_, cur_point_): # (Finished?, Who won?)
        state, player_point = deepcopy(state_), deepcopy(cur_point_)
        if finished(state):
            # get all remaining prawns in the 
            player_point[0] += sum([i[0] for i in state[0:QUAN_1]])
            player_point[1] += sum([i[0] for i in state[QUAN_1+1:QUAN_2]])

            if player_point[0] > player_point[1]: # Player 0 wins
                return (True, -self.INF if self.player_id else self.INF)
            elif player_point[0] < player_point[1]: # Player 1 wins
                return (True ,self.INF if self.player_id else -self.INF)
            else: # It's a Tie
                return(True,0)
        # Game has not finished yet
        return (False, player_point[1] if self.player_id else player_point[0])

    # Get moves that are Available: [(index,'l'),(index,'r')],[],[],..
    def getPossibleMoves(self, state, player_id): #list of actions: [(index,'l'),(index,'r')]
        list_of_action = []
        if not player_id:
            for i in range(0, QUAN_1):
                if state[i][0]: # prawns in that square
                    list_of_action.extend([(i,'Left'), (i,'Right')])
        else:
            for i in range(QUAN_1+1, QUAN_2):
                if state[i][0]:
                    list_of_action.extend([(i,'Left'), (i,'Right')])

        shuffle(list_of_action)
        return list_of_action
    
    # Evaluate after each turn: Int
    # Input: score: [Int,Int], winner: [Bool,Bool]
    # Output: Evaluated Score
    def evaluate(self, score, winner):
        if winner[0]:
            return winner[1] + score[1] - score[0] if self.player_id else winner[1] + score[0] - score[1]
        return score[1] - score[0] if self.player_id else score[0] - score[1]

    # Generate next possible move foreach player
    # Input: state, move, cur_point_, player_id
    # Output: (new_state, new_point)
    def performNextMove(self , state__, move , cur_point_ , id): # Khởi tạo bước đi trong bàn cờ
        state , cur_point = deepcopy(state__), deepcopy(cur_point_)
        '''table = Table()
        table.state = state
        table.playerScore = cur_point
        if id:
            table.move("player2",move[0],move[1],False)
        else:
            table.move("player1",move[0],move[1],False)
        return table.state, table.playerScore'''
        # direction: 1 for RIGHT and 2 for LEFT
        direction = 1 if move[1] == 'Right' else -1
        cur_pos = move[0]
        next_pos = (cur_pos + direction) % NUM_SQUARE

        # Each of next positions get +1 prawn
        for _ in range(state[cur_pos][0]):
            state[next_pos][0] += 1
            next_pos = (next_pos + direction) % NUM_SQUARE
        state[cur_pos][0] //= NUM_SQUARE

        while True:
            # if next_pos is a King's spot or (next_pos and next of next_pos are empty)
            # -> No more consecutive pick-up and point not increased
            if next_pos == QUAN_1 or next_pos == QUAN_2 or (state[next_pos][0] == 0 and state[(next_pos + direction) % NUM_SQUARE][0] == 0 and
                                    state[(next_pos + direction) % NUM_SQUARE][1] != 1):
                                    return state , cur_point
                                
            # else if next_pos is empty and (next of next_pos is not empty)
            # -> point increased
            elif state[next_pos][0] == 0 and (
                state[(next_pos + direction) % NUM_SQUARE][0] or state[(next_pos + direction) % NUM_SQUARE][1] == 1
            ):
                # reset the current point and state for (next of next_pos)
                cur_point[id] += state[(next_pos + direction) % NUM_SQUARE][0]
                state[(next_pos + direction) % NUM_SQUARE][0] = 0
                # check if we ate the King
                if state[(next_pos + direction) % NUM_SQUARE][1] == 1:
                    cur_point[id] += self.quanvalue
                    state[(next_pos + direction) % NUM_SQUARE][1] = 0
                # double tap
                if state[(next_pos + direction*2) % NUM_SQUARE][0] == 0 and state[(next_pos + direction * 2) % NUM_SQUARE][1] != 1:
                    next_pos = (next_pos + direction * 2) % NUM_SQUARE
                    
            # else: next pos is not empty and not a King's spot
            # -> continue running
            else:
                cur_pos = next_pos
                for _ in range(state[cur_pos][0]):
                    state[next_pos][0] += 1 
                    next_pos = (next_pos + direction) % NUM_SQUARE
                state[cur_pos][0] //= NUM_SQUARE
                
    def execute(self, state_game): # Alpha_Beta Algorithms
        start = time.time()
        cur_score = [self.table.player1Score, self.table.player2Score]
        inf = float('inf')
        def alpha_beta(cur_depth, index, curstate, cur_point, alpha, beta):
            index = index%2
            # return if max depth or gameover
            is_end = self.getResult(curstate, cur_point)
            if is_end[0] or cur_depth == self.depth:
                return None, self.evaluate(cur_point, is_end)

            # init
            best_score, best_action = None, None
            curstate , cur_point = self.handleBorrowStack(curstate, cur_point)
            ## minimax and AB pruning by each turn
            # Player: Maximize
            if index==0:
                best_score = -inf
                for move in self.getPossibleMoves(curstate, self.pid):
                    next_state, next_point = self.performNextMove(curstate, move , cur_point ,self.pid)
                    _, score = alpha_beta(cur_depth, index+1, next_state, next_point, alpha, beta)
                    if best_score < score:
                        best_score = score
                        best_action = move
                    if beta<=best_score:
                        return best_action, best_score
                    alpha = max(alpha, best_score)
                    
            # Opponent: Minimize
            else:
                best_score = inf
                for move in self.getPossibleMoves(curstate, self.pid^1):
                    next_state, next_point = self.performNextMove(curstate, move , cur_point ,self.pid^1)
                    #print(next_point)
                    
                    _, score = alpha_beta(cur_depth+1, index+1, next_state, next_point, alpha, beta)
                    if best_score > score:
                        best_score = score
                        best_action = move
                    if best_score<=alpha:
                        return best_action, best_score
                    beta = min(beta, best_score)
            return best_action, best_score
        
        final_score,final_action = -inf,None
        curstate , cur_point = self.handleBorrowStack(state_game, cur_score)
        alpha = -inf
        for move in self.getPossibleMoves(curstate, self.pid):
            next_state, next_point = self.performNextMove(curstate, move , cur_point ,self.pid)
            #print(next_state, next_point)
            _, score = alpha_beta(0,1,next_state, next_point,alpha,inf)
            if score>final_score:
                final_score = score
                final_action = move
            alpha = max(alpha,final_score)
            #print(move, score)
        run_time = time.time() - start
        print("Runtime: ",run_time)
        return self.getPossibleMoves(state_game , self.pid)[0] if final_action == None else final_action
class Human(Agent):
    def __init__(self, player_id, screen, table):
        super().__init__(player_id, screen, table)

    def execute(self,state_game):
        move = [None, None]
        old_box = 0
        self.table.redraw(0)
        x, y = 0, 0
        isClicked = False

        available_boxes = []
        for i in range(0,5):
            if state_game[i][0] > 0:
                available_boxes.append(i)

        if(len(available_boxes) == 0):
            self.table.borrow(self.player_id)

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
                    move[0] = 0
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
                    move[0] = 1
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
                    move[0] = 2
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
                    move[0] = 3
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
                    move[0] = 4
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
    
