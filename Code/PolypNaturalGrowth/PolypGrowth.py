import pandas as pd
import numpy as np
import math

class PolypGrowth:

    def __init__(self,outputDtPath):

        self.realStatesDT = pd.read_csv("./../datasets/state_seq_simulated.csv").fillna("-1")
        self.observedStatesDT = pd.read_csv("./../datasets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv").fillna("-1")
        self.polypGrowth = pd.DataFrame([], columns=self.observedStatesDT.columns)
        self.index = 0
        paitentList = self.realStatesDT["Paitent_ID"].unique().tolist()

        for paitent in paitentList:
            dt1 = self.getAllRowsForAPaitent_ID(self.realStatesDT,paitent)
            dt2 = self.getAllRowsForAPaitent_ID(self.observedStatesDT,paitent)
            self.getPolypGrowth(dt1, dt2)
        self.removeRowsWith1Entery()
        self.writeToFile(outputDtPath)


    def getPolypGrowth(self,dt1,dt2):

        for index1, row1 in dt1.iterrows():
            realStatesList = row1.tolist()
            for index2, row2 in dt2.iterrows():
                observedStatesList = row2.tolist()
                print("realStatesList    ", realStatesList)
                print("observedStatesList", observedStatesList)
                print("--------------------------------------")
                self.subtract2Rows(self.observedStatesDT.columns.tolist(), realStatesList, observedStatesList)

    def removeRowsWith1Entery(self):
        dt = self.polypGrowth.iloc[:, 2:].notna()
        indices = np.where(dt.apply(np.sum, axis=1).tolist())[0].tolist()
        self.polypGrowth = self.polypGrowth.iloc[indices, :]

    def getAllRowsForAPaitent_ID(self,dt,paitent_ID):
        return dt[dt.Paitent_ID == paitent_ID]

    def subtract2Rows(self,columnsList, realStatesList, observedStatesList):

        for i in range(1, len(columnsList) - 1):  # i is the column index which contains state, 0 column is paiten_ID last column is not needed

            remainPolyp = realStatesList[i]  # Get states for a given row (row = 0)
            observedPolyp = observedStatesList[i]

            if not observedPolyp == "-1":
                self.addEmptyRowToPolypGrowth()
                self.polypGrowth.iloc[self.index, 0] = realStatesList[0]                   # Set Paitent_ID in polypGrowth DT
                self.polypGrowth.iloc[self.index, 1] = self.subsidze2States(remainPolyp, observedPolyp)
                col = 2
                for state in realStatesList[(i + 1):]:                     # أNavigate throw the list to find next State

                    if state == "-1":
                        self.polypGrowth.iloc[self.index, col] = math.nan
                        col = col + 1
                    else:
                        self.polypGrowth.iloc[self.index, col] = state
                        self.index = self.index + 1
                        break
        return self.polypGrowth

    def getValidMinimumSequence(self,statusList,index):
        return statusList[index:].tolist()

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
        #print("realState:------", realState)
        realState = self.breakToPolypsNumber(realState)
        observedState = self.breakToPolypsNumber(observedState)
        small =  realState[0] - observedState[0]
        medium = realState[1] - observedState[1]
        large =  realState[2] - observedState[2]
        res = self.createState([small,  medium, large])  # Large Polyps diff
        return res

    def breakToPolypsNumber(self,state):

        polypsInString = state.split("_")
        polypsInInt = list(map(int, polypsInString))
        return polypsInInt

    def writeToFile(self,dataSetPath):
        self.polypGrowth.to_csv(dataSetPath, sep=',', encoding='utf-8', index=False)