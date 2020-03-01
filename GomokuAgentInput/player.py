import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        while True:
            row = int(input("Enter a row: "))
            column = int(input("Enter a column: "))
            moveLoc = tuple([row-1, column-1])
            if legalMove(board, moveLoc):
                return moveLoc
            else:
                print("Invalid location")
