'''
Created on Dec 10, 2021

@author: matth
'''
from CheckersV2.gameBoard import flipBoard, board2NN
import numpy as np
import time


class Node:
    def __init__(self,gameBoard,parent=None,name='maco'):
        self.parent = parent
        self.children = []
        self.gameBoard = gameBoard
        
        self.name = name
        
        self.visited = 0
        self.vals = [0,0]
        
    def visit(self,scores):
        self.visited = self.visited + 1
        self.vals[0] = self.vals[0] + scores[0]
        self.vals[1] = self.vals[1] + scores[1]
        #print(self.name)
        
    
    def getUCB(self):
        vals = [None,None]
        if self.visited == 0:
            return [np.inf,np.inf]
        
        c = np.sqrt(2)
        vals[0] = (self.vals[0] / self.visited) + c * np.sqrt(np.log(self.parent.visited)/self.visited)
        vals[1] = (self.vals[1] / self.visited) + c * np.sqrt(np.log(self.parent.visited)/self.visited)
        
        return vals
    
    
    def getRate(self):
        vals = [None,None]
        
        if self.visited == 0:
            return [0,0]
        
        vals[0] = self.vals[0] / self.visited
        vals[1] = self.vals[1] / self.visited
        
        return vals
        
    def hasChildren(self):
        if len(self.children) == 0:
            return False
        else:
            return True
        
    # def addChild(self,node):
    #     self.children.append(node)


def evaluate(model,gameBoard):
    pos = board2NN(gameBoard)
    est = model(pos)
    
    vals = [None,None]
    
    if gameBoard.getVal() is None:
        vals[gameBoard.turn] = 1-est
        vals[1-gameBoard.turn] = est
    else:
        vals = gameBoard.getVal()
    
    return vals
    
    

def doSearch(gameBoard,model):
    
    node = Node(gameBoard,name='taco')
    
    start = time.perf_counter()
    
    count = 0
    while time.perf_counter()-start < 2**-3:
        mcts(node,model)
        count = count + 1
        #print(count)
    
    bestNode = getBest(node)
    return bestNode.gameBoard

def getBest(node):
    
    bestNode = None
    bestVal = -np.inf
    
    for n in node.children:
        val = n.getRate()[node.gameBoard.turn]# + np.random.normal(0.01)
        #print(n.gameBoard.position,val)
        if val >= bestVal:
            bestNode = n
            bestVal = val
    
    
    return bestNode

def chooseChild(node):
    
    bestNode = None
    bestVal = -np.inf
    
    for n in node.children:
        val = n.getUCB()[node.gameBoard.turn]
        if val >= bestVal:
            bestNode = n
            bestVal = val
    
    
    return bestNode

def mcts(node,model):
    
    currNode = node
    
    #print(currNode.gameBoard.position,currNode.gameBoard.age,len(currNode.children))
    
    while currNode.visited > 0:
        
        if len(currNode.children) > 0:
            currNode = chooseChild(currNode)
        else:
            break
        
    #print(currNode.gameBoard.position,currNode.gameBoard.age,len(currNode.children))

    expandNode(currNode, model)    
    
    
    
    
def expandNode(node,model):
    
    vals = evaluate(model, node.gameBoard)
    
    actions = node.gameBoard.getActions()
    for a in actions:
        childNode = Node(gameBoard=a,parent=node)
        node.children.append(childNode)
        
        #print(childNode.gameBoard.position)
    
    # print(node.gameBoard.position,node.gameBoard.age,len(node.children))
    
    currNode = node
    while currNode is not None:
        #print(vals,currNode.name)
        currNode.visit(vals)
        #print(currNode.vals,currNode.visited,currNode.name)
        currNode = currNode.parent
        
    #return node    
    
    
    