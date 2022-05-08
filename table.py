from copy import deepcopy
import tkinter as tk
from support import *
### Deadline : 16h - 17h họp lại

## Hiện thực trên console
# Mượn quân: Nếu như bên mình không có quân thì thực hiện bằng cách trả điểm rãi vào mỗi ô 1 quân
# Điều kiện dừng (finished())
# Tính điểm trò chơi lúc nó kết thúc 
# Test lại tính đúng đắn 
# Hàm di chuyển (movingTurn())

## GUI
# Điều chỉnh lại tọa độ của mấy cái state

## Game 
# Hiện thực lại cái frame để chạy
# Hiện lên cửa sổ chọn mức độ trò chơi

PLAYER1 = 'player1'
PLAYER2 = 'player2'

myState = [
    [1, 0], [7, 0], [0, 0], [7, 0], [7, 0], [2, 1],
    [1, 0], [1, 0], [8, 0], [7, 0], [7, 0], [1, 0]
]


class Table:  
    def __init__(self):
        self.draw = '''
	    10  9  8  7	 6
        +--------------------+
    11  |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}| 5
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--------------------+
            0  1  2  3  4
        '''

        '''
		        10	9  8  7	 6
            +--------------------+
        11	| x| x| x| x| x| x| x| 5
            | Q|--------------| Q|
            |  | x| x| x| x| x|  |
            +--------------------+
                0  1  2  3  4
        '''
        self.turn = 0
        self.player1Score = 0
        self.player2Score = 0
        self.playerScore = [0, 0]
        # self.state = myState
        self.state = [
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]
        ]
        
    def initDrawTable(self):
        arr = []
        for i in range(11,5,-1):
            arr.append(self.state[i][0])
        arr.append(self.state[5][0])
        arr.append(self.state[11][1])
        arr.append(self.state[5][1])
        for i in range(0,5):
            arr.append(self.state[i][0])
            
        return arr

    def borrow(self, player):
        if player is PLAYER1:
            self.player1Score -= 5
            for i in range(5):
                self.state[i][0] += 1
        elif player is PLAYER2:
            self.player2Score -= 5
            for i in range(6, 11):
                self.state[i][0] += 1
        
        self.drawTable()

    def isSpread(self, player):
        sum = self.spread(player)
        return True if sum == 0 else False

    def spread(self, player):
        sum = 0
        if player is PLAYER1:
            for i in range(0, 5):
                sum += self.state[i][0]
        else:
            for i in range(6, 11):
                sum += self.state[i][0]
        return sum

    def handleBorrow(self, player):
        if self.isSpread(player):
            print('Caution! Your cells are empty, so you must borrow troops.')
            self.borrow(player)

    # valid is change turn
    def isChangeTurns(self, cell1, cell2):
        if cell1.isQuanCell and cell1.score != 0:
            return True
        if cell1.score == 0 and cell2.score == 0:
            if cell2.isQuanCell is False:
                return True
            else:
                cell2.score += 5 if self.state[cell2.index][1] == 1 else 0
                return True if cell2.score == 0 else False
        return False 

    # add score if user eat points
    def addScore(self, player, cell2):       
        score = self.state[cell2.index][0]
        
        # Nếu ô ăn được là ô quan thì cộng thêm điểm
        if cell2.isQuanCell:
            score += self.state[cell2.index][1] * 5
            self.state[cell2.index][1] = 0
        # Gán điểm cho player
        if player is PLAYER1: 
            self.player1Score += score
        elif player is PLAYER2:
            self.player2Score += score
        
        self.state[cell2.index][0] = 0
        cell2.score = 0
        self.drawTable()

    # return None, None nếu dừng, return 2 cell tiếp theo nếu ăn tiếp
    def eatCells(self, player, cell1, cell2, direction):
        print('Ăn điểm!')
        
        self.addScore(player, cell2)

        if direction == 'Right':
            nextIndex = calculateIndex(cell2.index + 1)
            nextnextIndex = calculateIndex(nextIndex + 1) 
        else:
            nextIndex = calculateIndex(cell2.index - 1)
            nextnextIndex = calculateIndex(nextIndex - 1)

        cell1Next = Cell(nextIndex, self.state[nextIndex][0])
        cell2Next = Cell(nextnextIndex, self.state[nextnextIndex][0])

        if self.isChangeTurns(cell1Next, cell2Next) is True:
            return None

        if cell1Next.score == 0:
            return cell1Next, cell2Next

    # Moving function
    def move(self, player, index, direction):
        tmp = self.state[index][0]
        if (direction == 'Right'):
            for i in range(tmp):
                self.state[calculateIndex(index + i + 1)][0] +=1
            nextIndex = calculateIndex(index + tmp +1) 
            nextnextIndex = calculateIndex(nextIndex + 1)
        else:
            for i in range(tmp):
                self.state[calculateIndex(index - i - 1)][0] +=1
            nextIndex = calculateIndex(index - tmp - 1) 
            nextnextIndex = calculateIndex(nextIndex - 1)

        self.state[index][0] = 0
        self.drawTable()
    
        cell1 = Cell(nextIndex, self.state[nextIndex][0])
        cell2 = Cell(nextnextIndex, self.state[nextnextIndex][0])
        return cell1, cell2       

    def handleMoving(self, player, index, direction):
        cell1, cell2 = self.move(player, index, direction)

        if self.isChangeTurns(cell1, cell2) is True:
            return None, True 

        # ăn điểm
        if cell1.score == 0:
            keepEating = self.eatCells(player, cell1, cell2, direction)
            while keepEating is not None:
                keepEating = self.eatCells(player, keepEating[0], keepEating[1], direction)
            return None, True 
        
        # đi tiếp
        elif cell1.score != 0:
            return cell1, False

    def start(self):
        self.drawTable()
        user = None

        while True:
            if user is None:
                user = input('player: ')
                if user == '1': user = PLAYER1
                elif user == '2': user = PLAYER2
            else:
                if user is PLAYER1:
                    user = PLAYER2
                else: user = PLAYER1
            index = int(input('index: '))

            direction = input('direction: ')
            if direction == 'r': direction = 'Right'
            else: direction = 'Left'

            result = self.movingTurn(user, index, direction)
            if result is True:
                break
        
    def movingTurn(self, player, index, direction):
        # self.drawTable()
        self.handleBorrow(player)

        text = 'Turn {}: {} chọn ô {}, hướng {}'
        print(text.format(self.turn + 1, player, index, direction))
        c1, swap = None, False

        while True:
            if swap is True:
                print('Change Turn!')
                self.turn += 1
                return self.validFinish()

            if c1 is None:
                c1, swap = self.handleMoving(player, index, direction)
            else: 
                c1, swap = self.handleMoving(player, c1.index, direction)

        return False
           
    def validFinish(self):
        quanPhai = self.state[5][0] + self.state[5][1]
        quanTrai = self.state[11][0] + self.state[11][1]
        if (quanPhai == 0 and quanTrai == 0):
            self.playerScore = [self.player1Score, self.player2Score]
        return self.finished()

    def drawTable(self, arr = None):
        if arr is None:
            arr = self.initDrawTable()
        print(self.draw.format(*arr))
        text = """        Player1's score: {}   Player2's score: {}\n"""
        print(text.format(self.player1Score, self.player2Score))
        # self.validFinish() 

    '''Checking whether if Game is finished'''
    def finished(self):
        if finished(self.state):
            # You won
            if self.playerScore[0] > self.playerScore[1]:
                result = 'You won!'
            # Computer won
            elif self.playerScore[0] < self.playerScore[1]:
                result = 'Computer won!'
            # Or draw
            else: result = 'Draw'
            # Show the message box to inform the result
            print(result)
            while True:
                tk.Tk().wm_withdraw()  # to hide the main window
                # messagebox.showinfo('End Game !', 'Result: ' + result)
                # time.sleep(2)
                break
            return True
        else:
            return False
    

def finished(_state):
    return  _state[5] == [0, 0] and _state[11] == [0, 0]