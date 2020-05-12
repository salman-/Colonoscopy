import numpy as np
import numpy.random as random
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

class Psi:
    
    def __init__(self, dataset,stateList ):

        self.matrix = self.obtainPsi(dataset,stateList)

####################################################################################
####################################################################################
####################################################################################
    """def getStates(self,dt):

        states = dt.loc[:,"Time0"]                   # Start by the first column and append the other columns to it
        columnNumber = len(dt.columns.tolist())

        for i in range(2, columnNumber ):
            states = states.append( dt.iloc[:,i] )

        states = states.dropna().unique()
        states = np.sort(states)

        return states"""



    def createMatrixByStates(self,stateList):
        toState = {state: 0 for state in stateList}
        mat = {state: toState.copy() for state in stateList}
        return pd.DataFrame(mat)

    def obtainPsi(self, dataset,stateList):

        psi = self.createMatrixByStates(stateList)
        stateChangeMatrix = self.fillStateChangeMatrix(dataset,stateList)

        for fromState in stateList:
            alphaArray = np.array(stateChangeMatrix.loc[fromState,:].tolist())+1
            row = random.dirichlet( alphaArray,1)               # Use driclet distribution to generate the Psi
            psi[fromState] = row[0]

        self.saveDataFrame(psi)
        return  psi #np.round(res,5)

    def fillStateChangeMatrix(self, dataset,stateList):

        stateChangeMatrix = self.createMatrixByStates(stateList)
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
        dt.to_csv("./DataSets/Psi.csv", sep=',', encoding='utf-8', index=True)