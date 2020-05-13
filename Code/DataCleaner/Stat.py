import pandas as pd
import numpy as np
import collections


class Stat:

    def __init__(self, dataSetPath,outputDTPath):

        self.outputDTPath = outputDTPath
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.countStateFrquency(self.dt)

    def countStateFrquency(self, dt):

        dt = dt.loc[:,"State"].tolist()
        counter = collections.Counter(dt)
        stat = pd.DataFrame(data=counter, index=["Frquency"])
        stat = stat.transpose()
        stat.loc[:, "Probability"] = stat.loc[:, "Frquency"] / len(dt)
        stat.index.names = ['State']
        self.saveOutputAsCSV(stat)

    def saveOutputAsCSV(self,dt):
        dt.to_csv(self.outputDTPath, sep=',', encoding='utf-8', index=True)

    def getDistribution(self,columnName):

        dtPath = "./../datasets/Final_Cleaned_Not_Aggregated(6Month)_And_Without_State_6_6_6.csv"
        dt = pd.read_csv(dtPath, error_bad_lines=False, index_col=False, dtype='unicode')
        values = dt[columnName].value_counts()
        sum = np.sum(values)
        pro = (values/sum).to_frame()
        pro.columns = [ 'Probability']
        print(type(pro))
        print(pro.columns)
        #print(np.sum(pro.tolist()))
        pro.index.names = ['NumberOfPolyps']
        pro.to_csv("./../datasets/"+columnName+"Distribution.csv", sep=',', encoding='utf-8', index=True)




