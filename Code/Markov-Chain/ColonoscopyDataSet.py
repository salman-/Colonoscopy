import numpy as np
import pandas as pd
from numpy import random
from numpy import nan
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 350)


class ColonoscopyDataSet:
    

    def __init__(self,dtPath):

        self.matrix = pd.read_csv(dtPath)
        #self.printValue("matrix", self.matrix)

        self.stateList     = self.getStates(self.matrix)    # List of states
        #self.printValue("stateList",self.stateList)
        self.stateSize     = len(self.stateList)
        #self.printValue("stateSize", self.stateSize)

        self.missedIndices = self.getMissedIndices(self.matrix)
        #self.printValue("missedIndices",self.missedIndices)


#-----------------------------------------------------------------
    def getMissedIndices(self, dt):

        missed = np.where(np.asanyarray(pd.isna(dt)))
        dict = {"rowIndex": missed[0],
                "colIndex": missed[1]}
        return pd.DataFrame(dict)

#----------------------------------------------------------------
    def getStates(self,dt):

        states = dt.loc[:,"Time0"]                   # Start by the first column and append the other columns to it
        columnNumber = len(self.matrix.columns.tolist())

        for i in range(2, columnNumber ):
            states = states.append( dt.iloc[:,i] )

        states = states.dropna().unique()
        states = np.sort(states)

        return states

    def randomlyChooseState(self,proWeights):    #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        return self.stateList[np.argmin((np.cumsum(proWeights) / sum(proWeights)) < np.random.rand())]

    def printValue(self,valueName,value):
        print("*********************************"+ valueName +"***************************************")
        print(value)