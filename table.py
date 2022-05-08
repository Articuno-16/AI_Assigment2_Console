from copy import deepcopy
import tkinter as tk
from tkinter import messagebox
from time import sleep
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

        self.playerScore = [0, 0]
        self.state = [
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]
        ]
        self.i = 0

    def initTable(self, table):
        arr = []
        for i in range(11,5,-1):
            arr.append(table[i][0])
        arr.append(table[5][0])
        arr.append(table[11][1])
        arr.append(table[5][1])
        for i in range(0,5):
            arr.append(table[i][0])
            
        return arr

    def fakeTable(self):
        arr = []
        for ele in self.state:
            arr.append(ele[0])
        return arr

    def handleNextIndex(self, index):
        if index < 0:
            absIndex = abs(index)
            if absIndex < 12: return 12 - absIndex
            return 12 * (1 + int(absIndex/12)) % absIndex
        if index > 11:
            return index % 12

    def isChangeTurns(self, cell1, cell2):
        if cell1.isQuanCell and cell1.score != 0:
            return True
        if cell1.score == 0 and cell2.score == 0:
            return True
        return False 

    def isEatPoints(self, cell1, cell2):
        return True if cell1.score == 0 and cell2.score != 0 else False


    # return None, None nếu dừng, return 2 cell tiếp theo nếu ăn tiếp
    def eatCells(self, cell1, cell2, direction):
        print('Ăn điểm!')
        self.playerScore[0] += cell2.score
        self.state[cell2.index][0] = 0
        print (self.state[cell2.index][0])
        self.consoleTable(None)
        if direction == 'Right':
            nextIndex = cell2.index + 1
            nextnextIndex = nextIndex + 1  
        else:
            nextIndex = cell2.index - 1
            nextnextIndex = nextIndex - 1

        if nextIndex > 11 or nextIndex < 0:
            nextIndex = self.handleNextIndex(nextIndex)
        if nextnextIndex > 11 or nextnextIndex < 0:
            nextnextIndex = self.handleNextIndex(nextnextIndex)

        if (0 < nextIndex < 12 and 0 < nextnextIndex < 12):
            cell1Next = Cell(nextIndex, self.state[nextIndex][0])
            cell2Next = Cell(nextnextIndex, self.state[nextnextIndex][0])
            if (self.isEatPoints(cell1Next, cell2Next)):
                return cell1Next, cell2Next
        return None, None

    # Moving function
    def moving(self, player, index, direction):
        text = 'Turn {}: {} chọn ô {}, hướng {}'
        print(text.format(self.i + 1,player, index, direction))
        self.i+=1
        array = self.fakeTable()
        currScore = array[index]
        array[index] = 0
        if (direction=='Right'):
            for i in range(currScore):
                array[index+i+1]+=1
            nextIndex = index+currScore+1
            nextnextIndex = nextIndex+1
        elif direction == 'Left':
            for i in range(currScore):
                array[index-i-1]+=1
            nextIndex = index-currScore-1
            nextnextIndex = nextIndex-1

        self.saveState(array)
        arr = self.initTable(self.state)
        print(self.draw.format(*arr))
        
        if nextIndex > 11 or nextIndex < 0:
            nextIndex = self.handleNextIndex(nextIndex)
        if nextnextIndex > 11 or nextnextIndex < 0:
            nextnextIndex = self.handleNextIndex(nextnextIndex)

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
            # if c1 is not None and c2 is not None: print(c1.index, c2.index)


    def handleMoving(self, player, index, direction):
        cell1, cell2 = self.moving(player, index, direction)

        if self.isChangeTurns(cell1, cell2) is True:
            print('Change Turn!')    
            return None, None  

        # ăn điểm
        if self.isEatPoints(cell1, cell2):
            keepEating = self.eatCells(cell1, cell2, direction)
            if keepEating is None: 
                print(keepEating[0].index, keepEating[1].index)
                return keepEating[0], keepEating[1]
            return None, None
        
        # đi tiếp
        elif cell1.score != 0:
            return cell1, cell2
                

    def consoleTable(self, arr):
        if arr is None:
            arr = self.initTable(self.state)
        print(self.draw.format(*arr)) 

    def finished(self):
        '''Checking whether if Game is finished'''
        if finished(self.state):
            # If point of player 0 > player 1 than you won
            if self.playerScore[0] > self.playerScore[1]:
                result = 'You won'
            # If point of player 0 < player 1 than computer won
            elif self.playerScore[0] < self.playerScore[1]:
                result = 'Computer won'
            # If equal than draw
            else: 
                result = 'Draw'
            # Show the message box to inform the result
            while True:
                tk.Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('End Game !', 'Result: ' + result)
                sleep(2)
                break
            return True
        else:
            return False
    

def finished(_state):
    return  _state[5] == [0, 0] and _state[11] == [0, 0]