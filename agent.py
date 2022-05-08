import pygame
from table import finished
import os
from GUI import RES,QUANVALUE
from random import randint,choice,shuffle
import sys
from copy import deepcopy
Lbutton = pygame.image.load(os.path.join(RES, 'left.png'))
Rbutton = pygame.image.load(os.path.join(RES, 'right.png'))
NUM_SQUARE = 12
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

class MinimaxAgent(Agent):
    def __init__(self, player_id, screen, table):
        super().__init__(player_id, screen, table)
    # Check Nợ quân: (new_state, new_point)
    def refill(self,_state, _player_point):
        state, player_point = deepcopy(_state), deepcopy(_player_point)

        if not any([i[0] for i in state[1:NUM_SQUARE//2]]):
            player_point[0] -= 5

            for i in range(1,NUM_SQUARE//2):
                state[i][0] = 1
        
        if not any([i[0] for i in state[7:NUM_SQUARE]]):
            player_point[1] -= 5

            for i in range(7,NUM_SQUARE):
                state[i][0] = 1
        return state, player_point
    
    # Get Final Result and Winner: (Bool,point)
    def getResult(self, state_, cur_point_): # (Finished?, Who won?)
        state, player_point = deepcopy(state_), deepcopy(cur_point_)
        if finished(state):
            # get all remaining prawns in the 
            player_point[0] += sum([i[0] for i in state[1:NUM_SQUARE//2]])
            player_point[1] += sum([i[0] for i in state[NUM_SQUARE//2 + 1:NUM_SQUARE]])

            if player_point[0] > player_point[1]: # Player 0 wins
                return (True, -self.INF if self.player_id else self.INF)
            elif player_point[0] < player_point[1]: # Player 1 wins
                return (True ,self.INF if self.player_id else -self.INF)
            else: # It's a Tie
                return(True,0)
        # Game has not finished yet
        return (False, player_point[1] if self.player_id else player_point[0])

    # Get moves that are Available: [(index,'l'),(index,'r')],[],[],..
    def getPossibleMoves(self, state , player_id): #list of actions: [(index,'l'),(index,'r')]
        list_of_action = []
        if not player_id:
            for i in range(1, NUM_SQUARE//2):
                if state[i][0]: # prawns in that square
                    list_of_action.extend([(i,'l'), (i,'r')])
        else:
            for i in range(NUM_SQUARE//2 + 1, NUM_SQUARE):
                if state[i][0]:
                    list_of_action.extend([(i,'l'), (i,'r')])

        shuffle(list_of_action)
        return list_of_action
    
    # Evaluation after each turn: Int
    def evaluation(self, cur_point , is_end):
        if is_end[0]:
            return is_end[1] + cur_point[1] - cur_point[0] if self.player_id else is_end[1] + cur_point[0] - cur_point[1]
        return cur_point[1] - cur_point[0] if self.player_id else cur_point[0] - cur_point[1]

    # Generate next possible move foreach player: (new_state, new_point)
    def performNextMove(self , state__, move , cur_point_ , id): # Khởi tạo bước đi trong bàn cờ
        state , cur_point = deepcopy(state__), deepcopy(cur_point_)
        
        # direction: 1 for RIGHT and 2 for LEFT
        direction = 1 if move[1] == 'r' else 2
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
            if state[next_pos][1] != 0 or (state[next_pos][0] == 0 and state[(next_pos + direction) % NUM_SQUARE][0] == 0 and
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
                    state[(next_pos + direction) % NUM_SQUARE][1] = 2
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
                
    def alpha_beta_agent(self , state_game , cur_point , depth = 3): # Alpha_Beta Algorithms
        inf = float('inf')
        def alpha_beta(cur_depth, index, curstate, cur_point, alpha, beta):
            #print(curstate)
            index = index%2
            cur_depth += 1
            # return if max depth or gameover
            is_end = self.getResult(curstate, cur_point)
            if is_end[0] or cur_depth == depth:
                return None, self.evaluation(cur_point, is_end)
            # init
            best_score, best_action = None, None
            curstate , cur_point = self.refill(curstate, cur_point)
            ## minimax and AB pruning by each turn
            # Player: Maximize
            if index==0:
                best_score = -inf
                for move in self.getPossibleMoves(curstate, self.player_id):
                    next_state, next_point = self.performNextMove(curstate, move , cur_point ,self.player_id)
                    _, score = alpha_beta(cur_depth, index+1, next_state, next_point, alpha, beta)
                    best_score = max(score,best_score)
                    if score > alpha:
                        alpha = score
                        best_action = move
                    if best_score >= beta: # beta cutoff
                        break
            # Opponent: Minimize
            else:
                best_score = inf
                for move in self.getPossibleMoves(curstate, self.player_id^1):
                    next_state, next_point = self.performNextMove(curstate, move , cur_point ,self.player_id^1)
                    _, score = alpha_beta(cur_depth, index+1, next_state, next_point, alpha, beta)
                    best_score = min(best_score,score)
                    if score < beta:
                        beta = score
                        best_action = move
                    if best_score <= alpha: # alpha cutoff
                        break
            # leaf state
            if best_score == inf or best_score == -inf or best_score is None:
                is_end = self.getResult(curstate, cur_point)
                return None, self.evaluation(cur_point, is_end)
            return best_action, best_score
        action, _ = alpha_beta(0,0,state_game,cur_point,-inf,inf)
        return self.getPossibleMoves(state_game , self.player_id)[0] if action == None else action
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
        for i in range(6,11):
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
                    move[0] = 6
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
                    move[0] = 7
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
                    move[0] = 8
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
                    move[0] = 9
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
                    move[0] = 10
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
    
