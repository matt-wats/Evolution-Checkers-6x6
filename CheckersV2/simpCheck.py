'''
Created on Dec 12, 2021

@author: matth
'''

import numpy as np
from CheckersV2.gameBoard import gameBoard
from CheckersV2.bots import getSavedBots
from CheckersV2.search import doSearch

position = np.array([[ 0, 0, 0,-2],
                     [ 0, 0, 0, 0],
                     [ 0, 0, 0, 0],
                     [ 0, 0, 2, 0]])

board = gameBoard(position,turn=0)

bots,epoch = getSavedBots('twoHiddenSmallerRate')

s = doSearch(board,bots[0])

#acts = board.getMoves()

# for a in acts:
#     print(a)

#print(s.position)