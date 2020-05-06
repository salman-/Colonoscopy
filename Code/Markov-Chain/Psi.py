import numpy as np
import pandas as pa
import numpy.random as random
import random as rand
import pandas as pd
from numpy import nan
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

class Psi:
    
    def __init__(self, dataset, stateSize,stateList):
        
        self.matrix = self.obtainPsi(dataset, stateSize,stateList)
        #print(self.matrix)
        
        
####################################################################################
####################################################################################
####################################################################################
   
    
    def obtainPsi(self, dataset, stateSize,stateList):
    
        changeMatrix = self.createStateChangeMatrix(dataset, stateSize,stateList)

        toState = {state: 0 for state in stateList}
        psi = {state: toState.copy() for state in stateList}
        psi = pd.DataFrame(psi)
        
        for fromState in stateList:
            alphaArray = np.array(changeMatrix.loc[fromState,:].tolist())+1
            row = random.dirichlet( alphaArray,1)               # Use driclet distribution to generate the Psi
            psi[fromState] = row[0]

        self.saveDataFrame(psi)
        return psi #np.round(res,5)"""
    
    def createStateChangeMatrix(self, dataset, stateSize, stateList):

        toState = {state: 0 for state in stateList}
        stateChangeMatrix = {state: toState.copy() for state in stateList}
        stateChangeMatrix = pd.DataFrame(stateChangeMatrix)

        for fromState in stateList:
            for toState in stateList:
                stateChangeMatrix.loc[fromState, toState] = self.stateChangeCounter(dataset, fromState, toState)
                #print("From State: " + fromState +
                #      " To State: " + toState    +
                #      " stateChange: " + str(stateChangeMatrix.loc[fromState, toState]))

        return stateChangeMatrix
        

    def stateChangeCounter(self, dataset, firstState,secondState):
        
        nrow=np.shape(dataset)[0]    ###inorder to make this function testable using unittest we skipped the self.nRow, and self.nCol
        ncol=np.shape(dataset)[1]
        sum = 0               
        for row in range(nrow): 
            for col in range(ncol-1):
                if dataset.iloc[row,col + 1]==secondState and not (pd.isna(dataset.iloc[row,col + 1])) and dataset.iloc[row,col]==firstState and not (pd.isna(dataset.iloc[row,col])) :
                    sum = sum+1
        return sum    

    def saveDataFrame(self,dt):
        dt.to_csv("Psi.csv", sep=',', encoding='utf-8', index=True)