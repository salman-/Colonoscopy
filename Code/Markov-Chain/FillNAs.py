import numpy as np
from   InformationMatrix import InformationMatrix
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 400)


class FillNAs:

    def __init__(self,dataSet,dtPath, stateList):
        
        self.dataSet  = dataSet
        self.im       = InformationMatrix(dtPath, stateList)

#--------------------------------------------------------------

    def fillNA_First_Iteration(self,dataSet, currentPsi):

        for index,missedInex in dataSet.missedIndices.iterrows():
            row = missedInex["rowIndex"]
            col = missedInex["colIndex"]
            previousState = dataSet.matrix.iloc[row,col-1]

            rowId = dataSet.randomlyChooseState(currentPsi.loc[:, previousState ].tolist())
            dataSet.matrix.iloc[row,col] = self.im.getRandomStateFromInformationMatrix(rowId)

        return dataSet.matrix

    
    def fillNA_After_First_Iteration(self, dataSet,currentPsi):

        lastColumnIndex = str(np.shape(dataSet.matrix)[1] - 1)

        for index, missedInex in dataSet.missedIndices.iterrows():                         # For all missed enteries
            rowIndex = missedInex["rowIndex"]
            colIndex = missedInex["colIndex"]

            isInLastColumn = (str(colIndex) == lastColumnIndex)
            if isInLastColumn:                                                             # missed index in LAST column
                previousState = dataSet.matrix.iloc[rowIndex,colIndex-1]
                nextState = 1
            else:
                previousState = dataSet.matrix.iloc[rowIndex,colIndex-1]                  # previous state in current data matrix
                nextState = dataSet.matrix.iloc[rowIndex,colIndex+1]                      # next PREDICTED state

            chanceMatrix = self.getChanceMatrix(dataSet,previousState,nextState,currentPsi)

            rowId  = dataSet.randomlyChooseState(chanceMatrix)
            dataSet.matrix[rowIndex,colIndex] = self.im.getRandomStateFromInformationMatrix(rowId)

        return dataSet.matrix

    
    def getChanceMatrix(self,dataSet,previousState,nextState,psi):

        if nextState == 1:                                # if missed index is in the last column then nextState is 1
            mul = psi.loc[previousState,:].tolist()
        else:                                             # minssed index is NoT in Last  Column

            a = np.array(psi.loc[previousState, :].tolist())
            b = np.array(psi.loc[:,nextState].tolist())
            mul = a * b

        weightedProb =  mul /  np.sum(mul)
        return weightedProb


    def isPSIsConverged(self,psiNew,psiLast,threshold):
        res = np.array((abs(psiNew-psiLast)<=threshold).values.tolist()).all()
                                          # return true if all the difference between all the enteries is less than 0.02

        return res