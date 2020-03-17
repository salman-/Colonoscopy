import numpy as np
import pandas as pa
import numpy.random as random
import random as rand
from numpy import nan

class Psi:
    
    def __init__(self, dataset, stateSize):
        
        self.matrix = self.obtainPsi(dataset, stateSize)
        
        
####################################################################################
####################################################################################
####################################################################################
   
    
    def obtainPsi(self, dataset, stateSize):                                    
    
        changeMatrix = self.createStateChangeMatrix(dataset, stateSize) 
        
        res=np.zeros((stateSize,stateSize))
        
        for fromState in np.arange(stateSize):
            row = random.dirichlet( (changeMatrix[fromState,:]+1),1)            # Use driclet distribution to generate the Psi
            res[fromState] = row
        
        return res #np.round(res,5)   
    
    def createStateChangeMatrix(self, dataset, stateSize):
        
        stateChangeMatrix=np.zeros((stateSize, stateSize))
        for fromState in np.arange(stateSize):
            for toState in np.arange(stateSize):
                stateChangeMatrix[fromState,toState] = self.stateChangeCounter(dataset, fromState, toState)
        return stateChangeMatrix
        

    def stateChangeCounter(self, dataset, firstState,secondState):
        
        nrow=np.shape(dataset)[0]    ###inorder to make this function testable using unittest we skipped the self.nRow, and self.nCol
        ncol=np.shape(dataset)[1]

        sum = 0               
        for row in range(nrow): 
            for col in range(ncol-1):
                if dataset[row][col+1]==secondState and not (dataset[row][col+1]== -1) and dataset[row][col]==firstState and not (dataset[row][col]==-1) :
                    sum = sum+1
        return sum    
    