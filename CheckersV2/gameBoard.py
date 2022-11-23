'''
Created on Dec 9, 2021

@author: matth
'''

import numpy as np


class gameBoard:
    
    def __init__(self,position=None,turn=0,age=0):
        self.position = position
        if position is None:
            self.position = self.initPosition()
        
        
        self.turn = turn
        self.age = age
        
    
    def initPosition(self):
        position = np.array([[ 0, 1, 0, 1, 0, 1],#[ 0, 1, 0, 1, 0, 1, 0, 1],
                             [ 1, 0, 1, 0, 1, 0],#[ 1, 0, 1, 0, 1, 0, 1, 0],
                             [ 0, 0, 0, 0, 0, 0],
                             [ 0, 0, 0, 0, 0, 0],
                             [ 0,-1, 0,-1, 0,-1],#[ 0,-1, 0,-1, 0,-1, 0,-1],
                             [-1, 0,-1, 0,-1, 0]])#[-1, 0,-1, 0,-1, 0,-1, 0]])
        return position
    
    def getVal(self):
        
        
        if len(self.getPieces()) == 0:
            if self.turn == 0:
                return [0,1]
            elif self.turn == 1:
                return [1,0]
        elif self.age >= 60 or len(self.getMoves()) == 0:
            return [1/2, 1/2]
        else:
            return None
        
    
    def getPieces(self):

        pieces = []
        
        for i in range(0,6,2):
            for j in range(1,6,2):
                if np.sign(self.position[i][j]) > 0:
                    pieces.append([i,j])
        
        for i in range(1,6,2):
            for j in range(0,6,2):
                if np.sign(self.position[i][j]) > 0:
                    pieces.append([i,j])
                    
        return pieces
    
    def flip(self):
        return gameBoard(flipBoard(self.position),self.turn,self.age,lastOnTop=not self.lastOnTop)
    
    def doAction(self):
        return self.flip()
    
    def getActions(self):
        
        
        actions = []
        
        for move in self.getMoves():
            b = self.position.copy()
        
            p = move[0]
            d = move[1]
            val = b[p[0]][p[1]]
            
            if p[0]+d[0] == 6-1:
                val = 2
            
            b[p[0]][p[1]] = 0
            b[p[0]+d[0]][p[1]+d[1]] = val
            
            if abs(d[0]) == 2:
                b[int(p[0]+d[0]/2)][int(p[1]+d[1]/2)] = 0
                
            actions.append(gameBoard(flipBoard(b),turn=1-self.turn,age=self.age+1))
        return actions
        
    
    
    def getMoves(self):
        position = self.position
        pieces = self.getPieces()
        moves = []
        
        for p in pieces:
            #collect all slides
            forw = p[0] + 1
            right = p[1] - 1
            left = p[1] + 1
            back = p[0] - 1
            if forw < 6:
                if right > -1 and position[forw][right] == 0:
                    moves.append([p,[1,-1]])
                if left < 6 and position[forw][left] == 0:
                    moves.append([p,[1,1]])
            
            if position[p[0]][p[1]] == 2 and back > -1:
                
                if right > -1 and position[back][right] == 0:
                    moves.append([p,[-1,-1]])
                if left < 6 and position[back][left] == 0:
                    moves.append([p,[-1,1]])
            
            #collect all jumps
            forw = p[0] + 2
            right = p[1] - 2
            left = p[1] + 2
            semiforw = p[0] + 1
            semiright = p[1] - 1
            semileft = p[1] + 1
            back = p[0] - 2
            semiback = p[0] - 1
            
            if forw < 6:
                if right > -1 and position[forw][right] == 0 and np.sign(position[semiforw][semiright]) == -1:
                    moves.append([p,[2,-2]])
                if left < 6 and position[forw][left] == 0 and np.sign(position[semiforw][semileft]) == -1:
                    moves.append([p,[2,2]])
            
            if position[p[0]][p[1]] == 2 and back > -1:
                if right > -1 and position[back][right] == 0 and position[semiback][semiright] == -1:
                    moves.append([p,[-2,-2]])
                if left < 6 and position[back][left] == 0 and position[semiback][semileft] == -1:
                    moves.append([p,[-2,2]])
        return moves
    
    



def flipBoard(position):
    b = np.flip(position.copy(),0)
    b = -np.flip(b,1)
    return b


# def doMove(gameBoard,move):
#     b = position.copy()
#     p = move[0]
#     d = move[1]
#     val = b[p[0]][p[1]]
#
#     if p[0]+d[0] == 7:
#         val = 2
#
#     b[p[0]][p[1]] = 0
#     b[p[0]+d[0]][p[1]+d[1]] = val
#
#     if abs(d[0]) == 2:
#         b[int(p[0]+d[0]/2)][int(p[1]+d[1]/2)] = 0
#
#     return flipBoard(b)


def board2NN(gameBoard):
    tiles = np.zeros([1,37])
    tiles[0] = gameBoard.age / 40
    count = 1
    for i in range(4):
        for j in range(4):
            if (i+j)%2 == 1:
                tile = gameBoard.position[i][j]
                if abs(tile) == 1:
                    tiles[0][count] = tile
                elif abs(tile) == 2:
                    tiles[0][count+1] = tile / 2
                count = count + 2
    
    return np.array(tiles)