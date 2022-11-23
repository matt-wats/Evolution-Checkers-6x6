'''
Created on Dec 12, 2021

@author: matth
'''
from CheckersV2.bots import getSavedBoss
from CheckersV2.train import play

folder = 'fixed'

bots = getSavedBoss(folder)

bot0 = bots[0]
bot1 = bots[-1]

play([bot0,bot1],show=True)