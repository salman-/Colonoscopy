import numpy as np
import pandas as pa
from numpy import random
from numpy import nan

"""        
    def __init__(self):

        self.stateSize      = 40

        self.nRow           = 6000
        self.nCol           = 5
        self.matrix  = pa.read_csv('./DataSets/data.csv', header= None).values
        self.matrix = self.matrix.reshape(1, 30000)
        self.missedIndices  = np.where(pa.isnull(self.matrix))[1]
        self.matrix = self.matrix.reshape(6000, 5)
"""

class ColonoscopyDataSet:
    

    def __init__(self):

        self.matrix = pa.read_csv('./DataSets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv')
        self.nRow   = np.shape(self.matrix)[0]
        self.nCol   = np.shape(self.matrix)[1]

        self.stateSize = self.getStateSize(self.matrix)
        self.matrix = self.matrix.to_numpy()
        self.missedIndices = np.where(pa.isnull(self.matrix))[1]

        print("State Size: "+str(self.stateSize)+" nRow: "+str(self.nRow ) + " nCol: "+str(self.nCol))

#-----------------------------------------------------------------
    
    def getStateSize(self,dt):

        states = dt.loc[:,"Time0"]                     # Start by the first column and append the other columns to it
        columnNumber = len(self.matrix.columns.tolist())
        for i in range(2, columnNumber ):
            states.append( dt.iloc[:,i] )
        return len(states.unique())


    
    def randomlyChooseState(self,psi): #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

        res = self.choice(np.arange( self.stateSize),psi)
        return res
    
    
    def choice(self,items, weights):
        return items[np.argmin((np.cumsum(weights) / sum(weights)) < np.random.rand())]

