'''
Created on Dec 11, 2021

@author: matth
'''

from CheckersV2.bots import initBots, saveBots, getSavedBots
from CheckersV2.train import trainBots, play

nu = True 
numEpochs = -1
foldername = 'fixed'

num = 1

if nu:
    bots = initBots(2)#2*num + 1)
    epoch = 0
else:
    bots,epoch = getSavedBots(foldername)


bots,bot,epoch = trainBots(bots[0:-1],bots[-1],startEpoch=epoch,numEpochs=numEpochs,folder=foldername)
bots.append(bot)

play([bots[0],bot],show=True)

saveBots(bots,epoch,foldername)