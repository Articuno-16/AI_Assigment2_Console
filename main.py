from table import Table

box = Table()

box.drawTable()
box.movingTurn(player='player1', index=2, direction='Right')
box.movingTurn(player='player2', index=8, direction='Right')

