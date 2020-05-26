import pandas as pd
import numpy as np
import math
from PolypGrowth import PolypGrowth


pg = PolypGrowth()

"""
index = 0
col = 2
listRealStatesDT = realStatesDT.iloc[0,1:]
listObservedStatesDT = observedStatesDT.iloc[0,1:]
for i in range(0,len(listRealStatesDT)):

    print(i, " : ", listRealStatesDT[i], " | ", listObservedStatesDT[i])

    if listRealStatesDT[i] =="-1":
        polypGrowth.iloc[index, col ] = ""
        col = col + 1
    else:
        polypGrowth.loc[index, "Time0"] = subsidze2States(listRealStatesDT[i], listObservedStatesDT[i])
        polypGrowth.iloc[index, col ] = listRealStatesDT[i]
        index = index + 1
        col = 2
        polypGrowth = addEmptyRowToDT(polypGrowth)
        polypGrowth.iloc[index, col] = listRealStatesDT[i]
"""


print("====================================================================")
print(pg.polypGrowth)