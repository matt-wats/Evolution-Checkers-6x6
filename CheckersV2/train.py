'''
Created on Dec 10, 2021

@author: matth
'''

import tensorflow as tf

import time
import keyboard
from CheckersV2.gameBoard import gameBoard, flipBoard, board2NN
from CheckersV2.search import doSearch
import numpy as np
from CheckersV2.bots import saveBoss

contTraining = True

def stopTraining():
    global contTraining
    contTraining = False
    print('Hotkey triggered to stop training at current epoch\n')
    
    return True

keyboard.add_hotkey('left ctrl + right shift + s', stopTraining)

class gamePlay:
    def __init__(self):
        self.start = np.random.randint(0,2)
        self.gameBoards = [gameBoard(turn=self.start)]
        self.termVal = []
        
        
    def setVal(self,val):
        if self.start == 0:
            self.termVal = val
        else:
            self.termVal = [val[1],val[0]]
        
    def addGameBoard(self,gameBoard):
        self.gameBoards.append(gameBoard)
        
    def getCurr(self):
        return self.gameBoards[-1]
        
        

def play(bots,show=False):
    
    game = gamePlay()
    
    while game.getCurr().getVal() is None:
        
        gameBoard = doSearch(game.getCurr(),bots[game.getCurr().turn])
        game.addGameBoard(gameBoard)
        
        if show:
            if gameBoard.turn == 0:
                print(gameBoard.position)
            else:
                print(flipBoard(gameBoard.position))
        
    
    game.setVal(game.getCurr().getVal())
    
    # if game.getCurr().getVal()[0] == 1:
    #     print('THE UP AND COMER WON')
    # elif game.getCurr().getVal()[0] == 0:
    #     print('our guy LOST??')
    
    return game


def tournament(bots,bot):
    
    amount = len(bots)
    
    games = []
    for i in range(amount):
        games.append([])
        
    numGames = 6
    
    for count,b in enumerate(bots):
        for i in range(numGames):
            game = play([b,bot])
            games[count].append(game)
        
    
        
    sums = []
    for agentGames in games:
        s = 0
        for game in agentGames:
            s = s + game.termVal[0]
        sums.append(s)
        
        
    order = np.flip(np.argsort(sums))
    
    best = order#[0]#:int(len(order)/2)]
    
    #print(best)
    
    print('score: ',sums[order[0]])
    
    changed = False
    if sums[order[0]] >= numGames*0.65:
        bot = bots[order[0]]
        changed = True
        print('change of best bot')
    
    return [bots[i] for i in best], [games[i] for i in best], bot, changed     #bots[best],games[best],bot



def trainBots(bots,bot,startEpoch=0,numEpochs=-1,folder='temp'):
            
    currEpoch = startEpoch
    global contTraining
    
    while contTraining and (currEpoch < startEpoch + numEpochs or numEpochs == -1):
        print('epoch #' + str(currEpoch) + '/' + str(startEpoch+numEpochs) + ' began at minute: ' + str(time.perf_counter()/60))
        bestBots,games,bot,changed = tournament(bots, bot)
        
        if changed:
            saveBoss(bot,currEpoch,folder)
        
        bots = reproduce(bestBots,games)
        currEpoch += 1
        
    print('ending training afters (' + str(currEpoch) + ') epochs, at minute ' + str(time.perf_counter()/60))
    
    return bots,bot,currEpoch

def randomGames(val=0):
    
    ins = []
    outs = []
    
    for i in range(6):
        
        for k in range(6-i):
            
            board = np.zeros([1,37])
            for j in range(i+1):
                board[0][np.random.randint(1,37)] = (-1)**val
            
            ins.append(board)
            outs.append([val])
        
    return ins,outs


def reinfLearn(model,games):
    
    inDat = []
    outDat = []
    
    for game in games:
        for gameBoard in game.gameBoards:
            inDat.append(board2NN(gameBoard))
            outDat.append([game.termVal[1-gameBoard.turn]])
            
    p0 = randomGames(0)
    p1 = randomGames(1)
    
    inDat = inDat + p0[0] + p1[0]
    outDat = outDat + p0[1] + p1[1]       
            
    
    train = tf.data.Dataset.from_tensor_slices((inDat, outDat))
    
    train = train.shuffle(225)
    
    model.fit(train)
    
    return model


def reproduce(models,games):
    
    return [reinfLearn(models[0], games[0])]
    
    nuModels = []#models.copy()
    
    for count,model in enumerate(models):
        nuModels.append(reinfLearn(model, games[count]))
    
    return nuModels