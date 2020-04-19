import pandas as pd
import numpy as np
import math
dtPath = "./../datasets/Final_CleanedDT.csv"

#----------------------------------------- Create History Matrix
dt = pd.read_csv(dtPath)
minYear = np.min(dt.year)
maxYear = np.max(dt.year)

historyMatrix = pd.DataFrame()

for ind in dt.index:
     facility = dt['facility'][ind]
     paitent_ID = dt['patient_ID'][ind]
     year = dt['year'][ind]
     state = dt['State'][ind]
     historyMatrix.loc[paitent_ID,year] = state
     historyMatrix.loc[paitent_ID, "0Facility"] = facility

historyMatrix.columns = historyMatrix.columns.astype(str)

historyMatrix = historyMatrix.reindex(sorted( historyMatrix.columns  ), axis=1)
print(historyMatrix.columns)

for rowNumber in range(len(historyMatrix)):

    firstNonNaColName = historyMatrix.iloc[rowNumber, 1:].first_valid_index()   # finds the name of the first column with non NA value (exclude the patient_ID)
    firstNonNaIndex = historyMatrix.columns.get_loc(firstNonNaColName)  # finds the index of the first column with non NA value
    print(firstNonNaIndex)
    for colNumber in range(firstNonNaIndex, len(historyMatrix.columns)):

        historyMatrix.iloc[rowNumber,colNumber-firstNonNaIndex+1] = historyMatrix.iloc[rowNumber,colNumber]
        if colNumber > 1:
             historyMatrix.iloc[rowNumber, colNumber] = math.nan
        print("--------------------------------------")

print(historyMatrix)

historyMatrix.to_csv("./../datasets/historyMatrix.csv", sep=',', encoding='utf-8')