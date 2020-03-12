import numpy as np
import pandas as pa
from numpy import random
from numpy import nan


class ColonoscopyDataSet:
    
        
    def __init__(self):
        
        self.stateSize      = 40
        
        self.nRow           = 6000
        self.nCol           = 5
        self.matrix  = pa.read_csv('./DataSets/data.csv', header= None).values
        self.matrix = self.matrix.reshape(1, 30000)
        self.missedIndices  = np.where(pa.isnull(self.matrix))[1]
        self.matrix = self.matrix.reshape(6000, 5)
        
       
#-----------------------------------------------------------------
    

    
    def randomlyChooseState(self,psi): #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

        res = self.choice(np.arange( self.stateSize),psi)
        return res
    
    
    def choice(self,items, weights):
        return items[np.argmin((np.cumsum(weights) / sum(weights)) < np.random.rand())]

