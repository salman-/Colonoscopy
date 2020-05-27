import pandas as pd
import numpy as np
import math

class PolypGrowth:

    def __init__(self,outputDtPath):
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

        paitentList = self.realStatesDT["Paitent_ID"].unique().tolist()
        #print("paitentList: ",paitentList)

        for paitent in paitentList:
            dt1 = self.getAllRowsForAPaitent_ID(self.realStatesDT,paitent)
            #print("---------------- dt1 ----------------",paitent)
            #print(dt1)
            dt2 = self.getAllRowsForAPaitent_ID(self.observedStatesDT,paitent)
            #print("----------------- dt2 ---------------",paitent)
            #print(dt2)
            #print("-------------------------------------")
            for i in range(0,np.shape(dt1)[0]+1):
                realStatesList = self.realStatesDT.loc[i,:].tolist()
                for j in range(0, np.shape(dt2)[0]+1):
                    #print("dt2 rows :    ",np.shape(dt2)[0]," indices: ",list(  range(0, np.shape(dt2)[0])  ))
                    observedStatesList = self.observedStatesDT.loc[j, :].tolist()
                    print("realStatesList",realStatesList)
                    print("observedStatesList", observedStatesList)
                    print("--------------------------------------")
                    self.subtract2Rows(self.observedStatesDT.columns.tolist(),realStatesList,observedStatesList)

        self.writeToFile(outputDtPath)



    def getAllRowsForAPaitent_ID(self,dt,paitent_ID):
        return dt[dt.Paitent_ID == paitent_ID]

    def subtract2Rows(self,columnsList, realStatesList, observedStatesList):
        index = 0
        for i in range(1, len(columnsList) - 1):  # i is the column index which contains state, 0 column is paiten_ID last column is not needed

            remainPolyp = realStatesList[i]  # Get states for a given row (row = 0)
            observedPolyp = observedStatesList[i]

            if not observedPolyp == "-1":
                self.addEmptyRowToPolypGrowth()
                self.polypGrowth.iloc[index, 0] = realStatesList[0]                   # Set Paitent_ID in polypGrowth DT
                self.polypGrowth.iloc[index, 1] = self.subsidze2States(remainPolyp, observedPolyp)
                col = 2
                for state in realStatesList[(i + 1):]:                     # أNavigate throw the list to find next State

                    if state == "-1":
                        self.polypGrowth.iloc[index, col] = math.nan
                        col = col + 1
                    else:
                        self.polypGrowth.iloc[index, col] = state
                        index = index + 1
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