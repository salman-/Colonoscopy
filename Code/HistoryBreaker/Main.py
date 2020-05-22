import pandas as pd
import numpy as np
import math

realStatesDT = pd.read_csv("./../datasets/state_seq_simulated.csv")
#print(realStatesDT)
#print("------------------------------------------------")
observedStatesDT = pd.read_csv("./../datasets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv")
print(observedStatesDT)

polypGrowth = pd.DataFrame([], columns=observedStatesDT.columns)

#print("------------------------- polypGrowth -----------------------")
#print(polypGrowth)

def addEmptyRowToDT(dt):
    nCol = np.shape(dt)[1]
    nRow = np.shape(dt)[0]
    row = np.empty((1, nCol ,))[0]
    row[:] = np.nan
    dt.loc[nRow] =row
    return dt

addEmptyRowToDT(polypGrowth)

paitentList = realStatesDT["Paitent_ID"].unique().tolist()
print(paitentList)

for paitent in paitentList:
    dt1 = realStatesDT[realStatesDT.Paitent_ID == paitent]
    print("---------------- dt1 ----------------")
    print(dt1)
    dt2 = observedStatesDT[observedStatesDT.Paitent_ID == paitent]
    print("----------------- dt2 ---------------")
    print(dt2)
    polypGrowth = addEmptyRowToDT(polypGrowth)

print("=================================")
print(polypGrowth)

def breakToPolypsNumber(state):

    polypsInString = state.split("_")
    polypsInInt= list(map(int, polypsInString))
    return polypsInInt

res = breakToPolypsNumber("1_3_4")
#print(res)

def createState(polypNumberList):
     polypsInString= list(map(str,polypNumberList))
     return polypsInString[0]+"_"+polypsInString[1]+"_"+polypsInString[2]

#res = createState([1,2,4])
#print(res)

def subsidze2States(realState, observedState):

    realState = breakToPolypsNumber(realState)
    observedState = breakToPolypsNumber(observedState)
    res =createState([realState[0] - observedState[0],    # Small Polyps diff
                 realState[1] - observedState[1],    # Medium Polyps diff
                 realState[2] - observedState[2]])   # Large Polyps diff
    return res

res = subsidze2States("1_3_4","0_2_1")
#print(res)