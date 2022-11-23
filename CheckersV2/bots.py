'''
Created on Dec 10, 2021

@author: matth
'''


#error messages control
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#neural network models
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import clone_model, load_model
from tensorflow.keras import regularizers

import numpy as np
import time





def createNN():
    model = keras.Sequential()
    model.add(layers.Dense(units=32,activation='relu',input_shape=(37,),kernel_regularizer=regularizers.l2(0.001)))
    for x in range(3):   
        model.add(layers.Dense(units=16,activation='relu',kernel_regularizer=regularizers.l2(0.001)))
    model.add(layers.Dense(units=1,activation='sigmoid',kernel_regularizer=regularizers.l2(0.001)))
    model.compile(optimizer=tf.keras.optimizers.Adam(0.02),loss=tf.keras.losses.MeanSquaredError())
    return model


def initBots(num):
    bots = []
    for i in range(num):
        bots.append(createNN())
    
    return bots



def cross(models):
    
    
    layers = [models[0].layers, models[1].layers]
    nuModel = createNN()
    nuLayers = nuModel.layers
    
    for k in range(len(nuLayers)): #each layer of model
        which = np.random.randint(2)
        nuW = nuLayers[k].get_weights()
        w = layers[which][k].get_weights()
    
        for i in range(len(w[0])): #kernel matrix
            for j in range(len(w[0][i])):
                
                    nuW[0][i][j] = w[0][i][j]
    
        for i in range(len(w[1])): #bias values
            nuW[1][i] = w[1][i]
    
        nuLayers[k].set_weights(nuW)
    
    
    return nuModel

def randMutate(model):
    
    nuModel = clone_model(model)
    layers = model.layers
    nuLayers = nuModel.layers
    
    for k in range(len(nuLayers)): #each layer of model
        if np.random.uniform() < 0.05:
            nuW = nuLayers[k].get_weights()
            w = layers[k].get_weights()
        
            for i in range(len(w[0])): #kernel matrix
                for j in range(len(w[0][i])):
                    
                        nuW[0][i][j] = w[0][i][j] + np.random.normal()
        
            for i in range(len(w[1])): #bias values
                nuW[1][i] = w[1][i] + np.random.normal()
        
            nuLayers[k].set_weights(nuW)
        
    return nuModel

def saveBoss(bot,epoch,folder):
    bot.save(folder + '/boss/bot(' + str(epoch) + ').h5')
    
def getSavedBoss(folder):
    
    folder = folder + '/boss'
    bots = []
    for filename in os.listdir(folder):
        bots.append(load_model(folder + '/' + filename))
    
    return bots


def saveBots(bots,epoch,folder):
    
    for count,bot in enumerate(bots):
        bot.save(folder + '/' + 'bot(' + str(count) + ').h5')
        
    file = open(folder + '/epoch.txt','w')
    file.write(str(epoch))
    file.close()
    print('the bots have all been saved under the folder: ' + folder + ' after a total of (' + str(epoch) + ') epochs')
    
    
def getSavedBots(folder):
    bots = []
    epoch = 0
    for filename in os.listdir(folder):
        if filename == 'epoch.txt':
            file = open(folder + '/' + filename)
            epoch = int(file.readline())
            file.close()
        elif filename == 'boss':
            continue
        else:
            bots.append(load_model(folder+'/'+filename))
        
    return bots,epoch