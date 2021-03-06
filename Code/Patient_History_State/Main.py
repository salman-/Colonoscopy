import pandas as pd
import numpy as np
import math
dtPath = "./../datasets/Final_CleanedDT.csv"

#----------------------------------------- Create History Matrix
dt = pd.read_csv(dtPath)
minYear = np.min(dt.year)
maxYear = np.max(dt.year)

historyMatrix = pd.DataFrame()
print("=======================================> Generate History Matrix")
for ind in dt.index:
     facility = dt['facility'][ind]
     paitent_ID = dt['patient_ID'][ind]
     year = dt['year'][ind]
     state = dt['State'][ind]
     historyMatrix.loc[paitent_ID,year] = state
     historyMatrix.loc[paitent_ID, "0Facility"] = facility
     #print(ind)
     print("-------------------------")

historyMatrix.columns = historyMatrix.columns.astype(str)
historyMatrix = historyMatrix.reindex(sorted( historyMatrix.columns  ), axis=1)

"""
  Shift all the states to the very first column. So, the first column always have an state
"""
print("=======================================> SHIFTING")
for rowNumber in range(len(historyMatrix)):

    firstNonNaColName = historyMatrix.iloc[rowNumber, 1:].first_valid_index()   # finds the name of the first column with non NA value (exclude the patient_ID)
    firstNonNaIndex = historyMatrix.columns.get_loc(firstNonNaColName)  # finds the index of the first column with non NA value
    #print("rowNumber: "+str(rowNumber))

    for colNumber in range(firstNonNaIndex, len(historyMatrix.columns)):

        historyMatrix.iloc[rowNumber,colNumber-firstNonNaIndex+1] = historyMatrix.iloc[rowNumber,colNumber]
        if colNumber > 1:
             historyMatrix.iloc[rowNumber, colNumber] = math.nan

"""
Rename the columns
"""
historyMatrix.index.name = 'patient_ID'
lst = ["facility"]

for i in range(0 , len(historyMatrix.columns)-1):
    lst.append("Time{num}".format(num=i))

historyMatrix.columns = lst

historyMatrix.to_csv("./../datasets/historyMatrix.csv", sep=',', encoding='utf-8',index=True)

"""
Remove the paitents which has only 1 colonoscopy result
"""

selectedRows = historyMatrix.iloc[:,2:].notna().any(axis=1).tolist()               # rows With More Than 1 Colonscopy
historyMatrixOfPaitentsWithMoreThan1Colnoscopy = historyMatrix.iloc[selectedRows,:]
historyMatrixOfPaitentsWithMoreThan1Colnoscopy.to_csv("./../datasets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv", sep=',', encoding='utf-8')