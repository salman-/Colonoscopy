import pandas as pd
import numpy as np
import math

class PolypGrowth:

    def __init__(self):
        self.realStatesDT = pd.read_csv("./../datasets/state_seq_simulated.csv")
        self.realStatesDT.fillna("-1", inplace=True)
        print("----------------------- realStatesDT ----------------------------")
        print(self.realStatesDT.iloc[0, :].tolist())
        print("----------------------- observedStatesDT ------------------------")
        self.observedStatesDT = pd.read_csv("./../datasets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv")
        self.observedStatesDT.fillna("-1", inplace=True)
        print(self.observedStatesDT.iloc[0, :].tolist())
        print("-----------------------------------------------------------------")
        self.polypGrowth = pd.DataFrame([], columns=self.observedStatesDT.columns)

        """
        paitentList = self.realStatesDT["Paitent_ID"].unique().tolist()
        # print(paitentList)

        for paitent in paitentList:
            dt1 = realStatesDT[realStatesDT.Paitent_ID == paitent]
            #print("---------------- dt1 ----------------")
            #print(dt1)
            dt2 = observedStatesDT[observedStatesDT.Paitent_ID == paitent]
            #print("----------------- dt2 ---------------")
            #print(dt2)
            polypGrowth = addEmptyRowToDT(polypGrowth)
        """

    def setPaitent_IDToPolypGrowthCurrentRow(self,paitentID):
        nRow = np.shape(self.polypGrowth)[0]
        self.polypGrowth.iloc[nRow, "Paitent_ID"] = paitentID

    def addEmptyRowToPolypGrowth(self):
        nCol = np.shape(self.polypGrowth)[1]
        nRow = np.shape(self.polypGrowth)[0]
        row = np.empty((1, nCol,))[0]
        row[:] = np.nan
        self.polypGrowth.loc[nRow] = row
        return self.polypGrowth

    def createState(self,polypNumberList):
        polypsInString = list(map(str, polypNumberList))
        return polypsInString[0] + "_" + polypsInString[1] + "_" + polypsInString[2]

    def subsidze2States(self,realState, observedState):
        realState = self.breakToPolypsNumber(realState)
        observedState = self.breakToPolypsNumber(observedState)
        res = self.createState([realState[0] - observedState[0],  # Small Polyps diff
                           realState[1] - observedState[1],  # Medium Polyps diff
                           realState[2] - observedState[2]])  # Large Polyps diff
        return res

    def breakToPolypsNumber(self,state):

        polypsInString = state.split("_")
        polypsInInt = list(map(int, polypsInString))
        return polypsInInt