from copy import deepcopy
import tkinter as tk

def calculateIndex(index):
    if 0 < index < 12:
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

        self.player1Score = 0
        self.player2Score = 0
        self.state = [
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]
        ]
        self.turn = 0

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

    def isEatPoints(self, cell1, cell2):
        return True if cell1.score == 0 and cell2.score != 0 else False

    def addScore(self, player, cell2):
        if player == 'player1': 
            self.player1Score += cell2.score 
        else: 
            self.player2Score += cell2.score

        # Nếu ô ăn được là ô quan thì bỏ điểm ở trong
        if cell2.isQuanCell:
            self.state[cell2.index][1] = 0

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
        
        array = self.fakeTable()
        currScore = array[index]
        array[index] = 0
        if (direction=='Right'):
            for i in range(currScore):
                array[calculateIndex(index+i+1)]+=1
            nextIndex = calculateIndex(index + currScore +1) 
            nextnextIndex = calculateIndex(nextIndex + 1)
        elif direction == 'Left':
            for i in range(currScore):
                array[index-i-1]+=1
            nextIndex = calculateIndex(index - currScore -1) 
            nextnextIndex = calculateIndex(nextIndex - 1)

        self.saveState(array)
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
                print('Ồ, tiếp tục ăn này')
                print(keepEating[0].index, keepEating[1].index)
                keepEating = self.eatCells(player, keepEating[0], keepEating[1], direction)
                if i == 10: break
            self.turn += 1
            return None, None  
        
        # đi tiếp
        elif cell1.score != 0:
            return cell1, cell2
                

    def drawTable(self, arr = None):
        if arr is None:
            arr = self.initTable(self.state)
        print(self.draw.format(*arr))
        text = """        Player1's score: {}\n        Player2's score: {}\n"""
        print(text.format(self.player1Score, self.player2Score)) 

    def finished(self):
        '''Checking whether if Game is finished'''
        if finished(self.state):
            # If point of player 0 > player 1 than you won
            if self.player_points[0] > self.player_points[1]:
                result = 'You won'
            # If point of player 0 < player 1 than computer won
            elif self.player_points[0] < self.player_points[1]:
                result = 'Computer won'
            # If equal than draw
            else: 
                result = 'Draw'
            # Show the message box to inform the result
            while True:
                tk.Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('End Game !', 'Result: ' + result)
                time.sleep(2)
                break
            return True
        else:
            return False
    

def finished(_state):
    return  _state[0] == [0, 0] and _state[6] == [0, 0]