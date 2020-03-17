import pandas as pd
import numpy  as np

class InformationMatrix:
    
    def __init__(self):
        self.informationMatrix = pd.read_csv("./DataSets/information_matrix.csv",header=None)
        self.states = np.shape( self.informationMatrix )[0]
        
        
#------------------------------------------------------------------
        
        
    def getRandomStateFromInformationMatrix(self, rowId):
        
        weightedPro = self.informationMatrix.loc[rowId,:] 
        return self.randomlyChooseState( weightedPro )
        
        
#------------------------------------------------------------------
    
    def randomlyChooseState(self,probabilityWeight): #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

        items = np.arange( self.states)
        return items[np.argmin((np.cumsum(probabilityWeight) / sum(probabilityWeight)) < np.random.rand())]