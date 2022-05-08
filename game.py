from time import sleep
import pygame,sys
import os
from agent import Agent, Human, RandomAgent

from GUI import TableGUI,SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_CAPTION,USER_GO_FIRST,RES
PLAYER1 = 'player1'
PLAYER2 = 'player2'



def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e
def getMenu(screen,font,fontbig):
    background = pygame.image.load(os.path.join(RES, 'background.png')) 
    screen.blit(background, (0, 0))
    pygame.display.set_caption("Madarin Capture Square")
    color=(255,255,255)
    label = fontbig.render(' MADARIN CAPTURE SQUARE ', True, (255,255,23))
    noti = font.render(' Press To Play: ', True, color)
    text1 = font.render(' A - Easy', True, color)
    text2 = font.render(' B - Medium', True, color)
    text3 = font.render(' C - Hard', True, color)

    screen.blit(label, (100,100))
    screen.blit(noti, (200,50+150))
    screen.blit(text1, (200,80+150))
    screen.blit(text2, (200,110+150))
    screen.blit(text3, (200,140+150))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # dfs
                    return "Easy"
                if event.key == pygame.K_b:
                    return "Medium"
                if event.key == pygame.K_c:
                    return "hard"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()	
            pygame.display.flip()

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.fontbig = pygame.font.Font('freesansbold.ttf', 40)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.players = []

    def redraw(self, turn):
        self.table.redraw(turn)
    
    def finished(self):
        return self.table.finished()

    def update(self,turn, move):
        # Chỉnh lại khúc này
        self.table.movingTurn(turn, move[0], move[1])

    def run(self):
        # User go first or agent go first
        turn = 0 if USER_GO_FIRST else 1

        # Display Menu
        level = getMenu(self.screen,self.font,self.fontbig)
        self.players.append(self.AgentFactory(level,PLAYER1))
        self.players.append(self.AgentFactory(level,PLAYER2))
        
        print("*** Level : {} ***".format(level))
        running = True

        # Game loop
        self.redraw(turn)
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()		
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()

                        
            move = self.players[turn].execute(self.table.state)
            print(move)
            self.update(self.players[turn].player_id,move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")
            turn ^= 1
            self.redraw(turn)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def reset(self): 
        self.table = TableGUI(self.screen)
        self.players.clear()
        self.move = None
        level = getMenu(self.screen,self.font,self.fontbig)
        self.players.append(self.AgentFactory('human'))
        self.players.append(self.AgentFactory(level))


    def AgentFactory(self,str,playerID):
        if str == "easy":
            return RandomAgent(playerID,self.screen,self.table)
        elif str == 'medium':
            return RandomAgent(playerID,self.screen,self.table)
        elif str == 'hard':
            return RandomAgent(playerID,self.screen,self.table)
        elif str == 'human':
            return Human(playerID,self.screen,self.table)
        else :
            return RandomAgent(playerID,self.screen,self.table)