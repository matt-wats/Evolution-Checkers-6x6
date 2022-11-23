'''
Created on Dec 10, 2021

@author: matth
'''

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#neural network models
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import clone_model, load_model

import numpy as np

model = keras.Sequential()

for x in range(3):   #range(0,random.randrange(0,15)):
    model.add(layers.Dense(units=32,activation='relu'))
    
model.add(layers.Dense(units=1,activation='sigmoid',input_shape=(33,)))

model.compile(optimizer=tf.keras.optimizers.Adam(0.002),loss=tf.keras.losses.MeanSquaredError())

v = np.random.rand(1,33)
w = np.random.rand(1,33)
v2 = np.random.rand(1,33)
w2 = np.random.rand(1,33)

t = np.random.rand(1,33)

outV = [1]#np.array([1])
outW = np.array([0])

inData = [v,w,v2,w2]
outData = [outV,outW,outV,outW]

print(model(t))

train = tf.data.Dataset.from_tensor_slices((inData, outData))

model.fit(train,epochs=8)
    #print(model(v),model(w))
    
print(model(v),model(w),model(v2),model(w2))
print(model(t))