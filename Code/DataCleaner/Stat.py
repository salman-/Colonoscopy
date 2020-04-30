import pandas as pd
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


