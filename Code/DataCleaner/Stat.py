import pandas as pd
import numpy as np
import collections


class Stat:

    def __init__(self, dataSetPath,outputDTPath):

        self.outputDTPath = outputDTPath
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.countStateFrquency(self.dt)

    def countStateFrquency(self, dt):
        states = dt["State"].tolist()
        overallNumberOfStates = len(states)


        statDT = self.buildDataset()
        for index, row in statDT.iterrows():
            statDT.loc[index,'Frequency'] = states.count(row['State'])
            statDT.loc[index, 'Probability'] = statDT.loc[index,'Frequency']/overallNumberOfStates


        statDT.sort_values('stateIndex')
        self.saveOutputAsCSV(statDT)

    def buildDataset(self):
        stateList = self.generateStates(25)
        stateIndex = list(range(len(stateList)))
        dict = {    "stateIndex" : stateIndex,
                    "State": stateList   }

        stat = pd.DataFrame(data=dict)
        stat["Frequency"] = np.nan
        stat["Probability"] =np.nan
        return stat

    def generateStates(self, numberOfStates):

        stateList = []
        for small in range(0, numberOfStates):    # in method1: numberOfStates=7
            for medium in range(0, numberOfStates):
                for large in range(0, numberOfStates):
                    if small + medium + large > (numberOfStates - 1):
                        break
                    else:
                        state = str(small) + "_" + str(medium) + "_" + str(large)
                        stateList.append(state)
        #print(stateList)
        return stateList

    def saveOutputAsCSV(self,dt):
        dt.to_csv(self.outputDTPath, sep=',', encoding='utf-8', index=False)

    def getDistribution(self,columnName):

        dtPath = "./../datasets/Final_Cleaned_Not_Aggregated(6Month)_And_Without_State_6_6_6.csv"
        dt = pd.read_csv(dtPath, error_bad_lines=False, index_col=False, dtype='unicode')
        values = dt[columnName].value_counts()
        sum = np.sum(values)
        pro = (values/sum).to_frame()
        pro.columns = [ 'Probability']
        pro.index.names = ['NumberOfPolyps']
        pro.to_csv("./../datasets/"+columnName+"Distribution.csv", sep=',', encoding='utf-8', index=True)




