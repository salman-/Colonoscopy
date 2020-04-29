import numpy as np
from   numpy import random

class DataSet:
    
    def __init__(self, stateSize, missPercentage, nRow, nCol):
        
        self.stateSize      = stateSize
        self.missPercentage = missPercentage 
        self.nRow           = nRow
        self.nCol           = nCol
        self.missedIndices  = self.getMissingIndex()
        self.matrix         = self.createDataSetWithNULLs(self.missedIndices)
        
        self.firstPsi       = self.getOriginalPsi()
        
#-----------------------------------------------------------------
        
    def createDataSetWithNULLs(self,missedIndices):
        
        psi     = self.getOriginalPsi()                                        # Original Psi is created by us
        matrix  = self.getDataSetWithoutNuLL(psi)
        matrix  = self.omitEnteries(matrix, self.missedIndices)
        return matrix
    
#------------------------------------------------------------------  
    
    def getDataSetWithoutNuLL(self,psi):
        
        matrix  = self.writeFirstColumn() 
        matrix  = self.writeAllColumns(psi,matrix)                             # Fill all columns from second column 
        return matrix
    
#-------------------------------------------------------------------------
        
    def writeAllColumns(self,psi,matrix):
        
        for row in range(self.nRow):           # row
            for col in range(1,self.nCol):     # column  
                previousState = matrix[row,col-1]
                matrix[row,col] = self.randomlyChooseState(psi[previousState,:]) # randomly obtain a state 
        return matrix
        
#-------------------------------------------------------------------------
    
    def writeFirstColumn(self):
        
        rowDt = np.full((self.nRow,self.nCol), -1)
        rowDt[:,0] =  random.choice(np.arange(self.stateSize),self.nRow)       # Set the first column
        return  rowDt 

#------------------------------------------------------------------
    
    def getOriginalPsi(self):
       
        return np.random.dirichlet(np.arange(self.stateSize)+1, self.stateSize)

#------------------------------------------------------------------    
    
    def getMissingIndex(self):                                           # Generate random indexes which should be missed

        numberOfNULLs = int(self.missPercentage * self.nCol * self.nRow)
        indices       = np.arange((self.nCol * self.nRow)-1).tolist()          
        return np.sort( np.array( random.choice(indices,numberOfNULLs)))
        


    def omitEnteries(self, matrix, indexes):                                     # Set the received indexes as -1
        
        matrix = np.reshape(matrix,(1, self.nRow* self.nCol ))
        matrix[0,indexes] = -1
        matrix = np.reshape(matrix,( self.nRow,self.nCol ))
        return matrix

#------------------------------------------------------------------
    
    def randomlyChooseState(self,probabilityWeight): #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

        items = np.arange( self.stateSize)
        return items[np.argmin((np.cumsum(probabilityWeight) / sum(probabilityWeight)) < np.random.rand())]
        
    