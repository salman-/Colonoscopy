import pandas as pd
import scipy.stats
import math

## Emision matirix works based on Binomial Disribution
class EmissionMatrix:

    def __init__(self,numberOfStates):

        self.smallSuccess = 0.75
        self.smallFailure = 0.25

        self.mediumSuccess = 0.85
        self.mediumFailure = 0.15

        self.largeSuccess = 0.95
        self.largeFailure = 0.05

        self.stateList = []
        self.stateList  = self.generateStates(self.stateList,numberOfStates)
        self.matrix = self.createEmissionMatrix(self.stateList)
        self.matrix = self.fillEmissionMatrix()
        self.writeToCSVFile(self.matrix)
#-----------------------------------------------------------
    def generateStates(self, stateList, numberOfStates):

        for small in range(0, numberOfStates):    # in method1: numberOfStates=7
            for medium in range(0, numberOfStates):
                for large in range(0, numberOfStates):
                    if small + medium + large > (numberOfStates - 1):
                        break
                    else:
                        state = str(small) + "_" + str(medium) + "_" + str(large)
                        stateList.append(state)

        self.stateList.append('6_6_6')  # "6_6_6" is only used in the Method1

        return stateList

    def fillEmissionMatrix(self):

        for realState in self.stateList:  # Navigate throw DT

            for observedStates in self.stateList:

                print("realState is: " + str(realState) + " observedStates is: " + str(observedStates))
                realStateNumber = self.getPolypsNumber(realState)
                observedStatesNumber = self.getPolypsNumber(observedStates)
                if ((realStateNumber[0] < observedStatesNumber[0]) or (
                        realStateNumber[1] < observedStatesNumber[1]) or (
                        realStateNumber[2] < observedStatesNumber[2])):
                    pro = 0
                else:
                    pro = self.getProbability(observedStatesNumber, realStateNumber)
                self.matrix[observedStates][realState] = pro

            print("-----------------------")
        return self.matrix

    def getPolypsNumber(self,state):
        res = list(map(int, str(state).split("_")))
        return res

    def getProbability(self,observedStatesNumber, realStateNumber):
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
        emissionMatrix = {state: toState.copy() for state in stateList} # matrix to keep state transitions
        return emissionMatrix

#-------------------------------------------------------- Save EmissionMatrox into a .csv file

    def writeToCSVFile(self,mat):
        mat = pd.DataFrame(mat)
        mat.to_csv("./../datasets/EmissionMatrix/EmissionMatrix.csv", sep=',', encoding='utf-8', index=True)