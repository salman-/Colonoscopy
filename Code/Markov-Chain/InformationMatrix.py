import pandas as pd
import numpy  as np
import scipy.stats
import math

class InformationMatrix:

    def __init__(self,   stateList):

        self.smallSuccess = 0.75
        self.smallFailure = 0.25

        self.mediumSuccess = 0.85
        self.mediumFailure = 0.15

        self.largeSuccess = 0.95
        self.largeFailure = 0.05

        #print("---------------------------")
        #print(self.stateList)
        self.stateList = stateList
        self.matrix = self.createEmissionMatrix(self.stateList)
        self.informationMatrix = self.fillEmissionMatrix()
        self.fixTheLastCell(self.informationMatrix)    # The last cell 9_9_9 to 9_9_9 must be almost 1
        self.writeToCSVFile(self.informationMatrix)

#-----------------------------------------------------------------------------------


    def fillEmissionMatrix(self):

        for realState in self.stateList:  # Navigate throw DT

            for observedStates in self.stateList:

                #print("realState is: " + str(realState) + " observedStates is: " + str(observedStates))
                realStateNumber = self.getPolypsNumber(realState)
                observedStatesNumber = self.getPolypsNumber(observedStates)
                if ((realStateNumber[0] < observedStatesNumber[0]) or (
                        realStateNumber[1] < observedStatesNumber[1]) or (
                        realStateNumber[2] < observedStatesNumber[2])):
                    pro = 0
                else:
                    pro = self.getProbability(observedStatesNumber, realStateNumber)
                self.matrix[observedStates][realState] = pro

            #print("-----------------------")
        return pd.DataFrame(self.matrix)

    def getPolypsNumber(self, state):
        res = list(map(int, str(state).split("_")))
        return res

    def getProbability(self, observedStatesNumber, realStateNumber):
        foundSmalls = observedStatesNumber[0]
        # missedSmall = realStateNumber[0] - foundSmalls

        foundMedium = observedStatesNumber[1]
        # missedMedium = realStateNumber[1] - foundMedium

        foundLarge = observedStatesNumber[2]
        # missedLarge = realStateNumber[2] - foundLarge

        proSmall = scipy.stats.binom.pmf(foundSmalls, realStateNumber[0], self.smallSuccess)
        proMedium = scipy.stats.binom.pmf(foundMedium, realStateNumber[1], self.mediumSuccess)
        proLarge = scipy.stats.binom.pmf(foundLarge, realStateNumber[2], self.largeSuccess)

        pro = proSmall * proMedium * proLarge
        return pro

    def createEmissionMatrix(self, stateList):

        toState = {state: 0 for state in stateList}
        emissionMatrix = {state: toState.copy() for state in stateList}  # matrix to keep state transitions
        return emissionMatrix

#----------------------------------------------------
    def fixTheLastCell(self, dt):

        nRow = np.shape(dt)[0]
        nCol = np.shape(dt)[1]
        dt.iloc[nRow-1,nCol-1] = 1 - np.sum(dt.iloc[nRow-1,:(nCol-2)])               # fix the last cell

#------------------------------------------------------------------- Save EmissionMatrox into a .csv file

    def writeToCSVFile(self, mat):
        mat.to_csv("./DataSets/EmissionMatrix.csv", sep=',', encoding='utf-8', index=True)

#------------------------------------------------------------------
    def getRandomStateFromInformationMatrix(self, rowId):

        weightedPro = self.informationMatrix.loc[rowId,:].tolist()
        randomState = self.randomlyChooseState(weightedPro)

        return randomState

#------------------------------------------------------------------
    
    def randomlyChooseState(self,probabilityWeight): #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice

        return self.stateList[np.argmin((np.cumsum(probabilityWeight)) < np.random.rand())]