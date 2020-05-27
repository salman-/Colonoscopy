import pandas as pd
import numpy as np
import math
from PolypGrowth import PolypGrowth


outputPath = "./../datasets/polypGrowth/polypGrowth.csv"
pg = PolypGrowth(outputPath)


"""
columnsList        = pg.realStatesDT.columns.tolist()
print("Columns: ",columnsList)
realStatesList     = pg.realStatesDT.loc[4,:].tolist()
print("realStatesList:     ",realStatesList)
observedStatesList = pg.observedStatesDT.loc[1,:].tolist()
print("observedStatesList: ",observedStatesList)

pg.subtract2Rows(pg.observedStatesDT.columns.tolist(),realStatesList,observedStatesList)

print("====================================================================")
print(pg.polypGrowth)"""