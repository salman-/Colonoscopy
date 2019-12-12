import pandas as pd
import numpy as np

"""
Method2 categorizes the states into 4 main groups (0,1,2,3,4) as below:
1. Call categorizeStates to classify the current states
2. Update the state based on new categories using buildStateForEachPaitent

"""

class ReduceStatesMethod2:

    def __init__(self):

        self.dtPath = "./../Dataset/cleanedData.csv"
        self.mainDt = pd.read_csv(self.dtPath)
        self.mainDt = self.mainDt[["facility", "patient_ID", "year", "month", "Nr_Small", "Nr_Medium", "Nr_Large"]]
        self.mainDt.fillna(0, inplace=True)

        self.buildStateForEachPaitent("Nr_Small")
        self.buildStateForEachPaitent("Nr_Medium")
        self.buildStateForEachPaitent("Nr_Large")
        self.mainDt = self.mainDt.iloc[:, 1:11].astype(int).astype(str)
        self.mainDt["New_State"] = self.mainDt["New_Nr_Small"] + "_" + self.mainDt["New_Nr_Medium"] + "_" + self.mainDt["New_Nr_Large"]  # Add State column

    def categorizeStates(self):

        dict = {"0": [0],
                "1": list(range(1, 3)),
                "2": list(range(3, 5)),
                "3": list(range(5, 100))}
        return dict

    def findStatusOfPolypNumber(self,PolypNumber):

        dict = self.categorizeStates()
        foundKey = -1
        for key in list(dict.keys()):
            if PolypNumber in dict[key]:
                foundKey = key
                break
        return foundKey

    def buildStateForEachPaitent(self,polypSize):  # polypSize can be  "Nr_Small","Nr_Medium" and "Nr_Large"
        polyps = self.mainDt[polypSize]
        newState = []
        for i in range(0, np.shape(polyps)[0]):

            newState.append( self.findStatusOfPolypNumber(polyps.iloc[i] ))

        updateState = "New_"+polypSize
        self.mainDt[updateState] = newState

    def output(self):
        self.mainDt.to_csv("./../Dataset/paitent_State_Reduced_State_By_Method2.csv", sep=',', encoding='utf-8', index=False)





