from copy import deepcopy
import tkinter as tk
from tkinter import messagebox
from time import sleep

def calculateIndex(index):
    if 0 <= index < 12:
        return index
    if index < 0:
        absIndex = abs(index)
        if absIndex < 12: return 12 - absIndex
        return 12 * (1 + int(absIndex/12)) % absIndex
    if index > 11:
        return index % 12

class Cell:
    def __init__(self, index, score):
        self.index = index
        self.isQuanCell = True if self.index == 5 or self.index == 11 else False
        self.score = score

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
class Table:  
    def __init__(self):
        self.draw = '''
        +--------------------+
        |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--------------------+
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

    # def handleNextIndex(self, index):
    #     if index < 0:
    #         absIndex = abs(index)
    #         if absIndex < 12: return 12 - absIndex
    #         return 12 * (1 + int(absIndex/12)) % absIndex
    #     if index > 11:
    #         return index % 12


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

    def addScore(self, player, cell2):       
        score = self.state[cell2.index][0]
        
        # Nếu ô ăn được là ô quan thì cộng thêm điểm
        if cell2.isQuanCell:
            score += self.state[cell2.index][1] * 5
            self.state[cell2.index][1] = 0
        # Gán điểm cho player
        if player == 'player1': 
            self.player1Score += score
        else: 
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
            print('Change Turn!')
            self.turn += 1    
            return None

        if cell1Next.score == 0:
            return cell1Next, cell2Next

    # Moving function
    def moving(self, player, index, direction):
        text = 'Turn {}: {} chọn ô {}, hướng {}'
        print(text.format(self.turn + 1, player, index, direction))
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
    
        nextCell = Cell(nextIndex, self.state[nextIndex][0])
        nextnextCell = Cell(nextnextIndex, self.state[nextnextIndex][0])
        return nextCell, nextnextCell

    def saveState(self, array):
        for i in range(len(array)):
            o = [array[i], 1] if (i == 5 or i == 11) else [array[i], 0]
            self.state[i] = o

    def movingTurn(self, player, index, direction):
        c1, c2 = self.handleMoving(player, index, direction)
        
        while c1 is not None and c2 is not None:
            c1, c2 = self.handleMoving(player, c1.index, direction)


    def handleMoving(self, player, index, direction):
        cell1, cell2 = self.moving(player, index, direction)

        if self.isChangeTurns(cell1, cell2) is True:
            print('Change Turn!')
            self.turn += 1    
            return None, None  

        # ăn điểm
        if cell1.score == 0:
            keepEating = self.eatCells(player, cell1, cell2, direction)

            i = 0
            while keepEating is not None:
                i+=1
                keepEating = self.eatCells(player, keepEating[0], keepEating[1], direction)
                if i == 10: break
            return None, None  
        
        # đi tiếp
        elif cell1.score != 0:
            return cell1, cell2
                
    def validFinish(self):
        quanPhai = self.state[5][0] + self.state[5][1]
        quanTrai = self.state[11][0] + self.state[11][1]
        if (quanPhai == 0 and quanTrai == 0):
            self.playerScore = [self.player1Score, self.player2Score]
            self.finished()


    def drawTable(self, arr = None):
        if arr is None:
            arr = self.initDrawTable()
        print(self.draw.format(*arr))
        text = """        Player1's score: {}\n        Player2's score: {}\n"""
        print(text.format(self.player1Score, self.player2Score))
        self.validFinish() 


    '''Checking whether if Game is finished'''
    def finished(self):
        if finished(self.state):
            # If point of player 0 > player 1 than you won
            if self.playerScore[0] > self.playerScore[1]:
                result = 'You won'
            # If point of player 0 < player 1 than computer won
            elif self.playerScore[0] < self.playerScore[1]:
                result = 'Computer won'
            # Or draw
            else: result = 'Draw'
            # Show the message box to inform the result
            print(result)
            while True:
                tk.Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('End Game !', 'Result: ' + result)
                sleep(2)
                return True
        else:
            return False
    

def finished(_state):
    return  _state[5] == [0, 0] and _state[11] == [0, 0]