import pandas as pd
import numpy as np
import math

class FillNAs:

    def __init__(self,cleanedDTPath):
        self.dt = pd.read_csv(cleanedDTPath, error_bad_lines=False, index_col=False, dtype='unicode')
        trueDataSet = pd.read_csv("./../datasets/Capsules/TrueData.csv", error_bad_lines=False, index_col=False, dtype='unicode')
        trueDataSet = trueDataSet[["Number of sessiles", "Size of Sessile in Words"]]
        trueDataSet = trueDataSet.groupby(["Number of sessiles", "Size of Sessile in Words"]).size().reset_index(name='Count')

        self.fillNAsInSize(trueDataSet)
        self.fillNAsInPolypNo(trueDataSet)
        self.writeToFile()
        # print(dt)

    def fillNAsInPolypNo(self):
        self.dt["Number of sessiles"].fillna(self.getRandomPolypNo(self.dt["Size of Sessile in Words"]), inplace=True)

    def fillNAsInSize(self):
        self.dt["Size of Sessile in Words"].fillna(self.getRandomPolypNo(self.dt["Number of sessiles"]), inplace=True)

    def getRandomPolypNo(self, trueDataSet, size):   #Given that we know the size, it generates Number of polyps
        trueDataSet = trueDataSet[trueDataSet["Size of Sessile in Words"] == size]
        sumCounts = np.sum(trueDataSet["Count"])
        trueDataSet["Count"] = trueDataSet["Count"] / sumCounts
        noList = trueDataSet["Number of sessiles"].tolist()
        pro = trueDataSet["Count"].tolist()
        randomPolypNo = np.random.choice(noList, 1, p=pro)
        return randomPolypNo[0]

    def getRandomPolypSize(self, trueDataSet, polypNo): #Given that we know the polypNo, it generates Size of polyps
        trueDataSet = trueDataSet[trueDataSet["Number of sessiles"] == polypNo]
        sumCounts = np.sum(trueDataSet["Count"])
        trueDataSet["Count"] = trueDataSet["Count"] / sumCounts
        noList = trueDataSet["Size of Sessile in Words"].tolist()
        pro = trueDataSet["Count"].tolist()
        randomPolypNo = np.random.choice(noList, 1, p=pro)
        return randomPolypNo[0]

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
