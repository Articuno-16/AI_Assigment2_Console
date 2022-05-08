PLAYER1 = 'player1'
PLAYER2 = 'player2'
LEFT = 'Left'
RIGHT = 'Right'

def calculateIndex(index):
    if 0 <= index < 12:
        return index
    if index < 0:
        absIndex = abs(index)
        if absIndex < 12: return 12 - absIndex
        return 12 * (1 + int(absIndex/12)) % absIndex
    if index > 11:
        return index % 12

def getUser(user):
    if user is PLAYER1:
        return PLAYER2
    return PLAYER1

def getInput(player=None):
    while True:
        user = getUser(player)
        index = int(input('Index: '))
        direction = input('Direction: ')
        direction = RIGHT if direction == 'r' or direction == 'R' else LEFT
        if validInput(user, index): break
    return user, index, direction

def validInput(user, index):
    if user is PLAYER1:
        if 0 <= index < 5: 
            return True
        else: 
            print('You must input from 0 to 4')
            return False
    elif user is PLAYER2:
        if 6 <= index < 11: 
            return True
        else: 
            print('You must input from 6 to 11')
            return False

class Cell:
    def __init__(self, index, score):
        self.index = index
        self.isQuanCell = True if self.index == 5 or self.index == 11 else False
        self.score = score