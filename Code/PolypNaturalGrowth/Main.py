import pandas as pd
import numpy as np
import math
from PolypGrowth import PolypGrowth


pg = PolypGrowth()




"""

for i in range(1,len(pg.observedStatesDT.columns)-1):                       # i is the column index which contains state

    remainPolyp   = pg.realStatesDT.iloc[0, i]     # Get states for a given row (row = 0)
    observedPolyp = pg.observedStatesDT.iloc[0, i]
    #print("-- i",i,"list",list(range(1,len(pg.observedStatesDT.columns)-1)))
    #print(i, " remainPolyp: ", remainPolyp, " | observedPolyp: ", observedPolyp)

    if not observedPolyp =="-1":
        pg.addEmptyRowToPolypGrowth()
        pg.polypGrowth.iloc[index, 0] = pg.realStatesDT.iloc[0, 0]                    # Set Paitent_ID in polypGrowth DT
        pg.polypGrowth.iloc[index, 1] = pg.subsidze2States(remainPolyp, observedPolyp)
        col = 2
        for x in pg.realStatesDT.iloc[0, (i+1):].tolist():                      #أNavigate throw the list to find next State

            if x=="-1":
                pg.polypGrowth.iloc[index, col ] = math.nan
                col = col + 1
            else:
                pg.polypGrowth.iloc[index, col] = x
                index = index + 1
                break

print("====================================================================")
print(pg.polypGrowth)
"""



def subtract2Rows(columnsList,realStatesList,observedStatesList):
    index = 0
    for i in range(1, len(columnsList) - 1):  # i is the column index which contains state, 0 column is paiten_ID last column is not needed

        remainPolyp = realStatesList[i]  # Get states for a given row (row = 0)
        observedPolyp = observedStatesList[i]

        if not observedPolyp == "-1":
            pg.addEmptyRowToPolypGrowth()
            pg.polypGrowth.iloc[index, 0] = realStatesList[0]  # Set Paitent_ID in polypGrowth DT
            pg.polypGrowth.iloc[index, 1] = pg.subsidze2States(remainPolyp, observedPolyp)
            col = 2
            for x in realStatesList[(i + 1):]:  # أNavigate throw the list to find next State

                if x == "-1":
                    pg.polypGrowth.iloc[index, col] = math.nan
                    col = col + 1
                else:
                    pg.polypGrowth.iloc[index, col] = x
                    index = index + 1
                    break
    return pg.polypGrowth

columnsList        = pg.realStatesDT.columns.tolist()
print("Columns: ",columnsList)
realStatesList     = pg.realStatesDT.loc[4,:].tolist()
print("realStatesList:     ",realStatesList)
observedStatesList = pg.observedStatesDT.loc[1,:].tolist()
print("observedStatesList: ",observedStatesList)
subtract2Rows(columnsList,realStatesList,observedStatesList)

print("====================================================================")
print(pg.polypGrowth)