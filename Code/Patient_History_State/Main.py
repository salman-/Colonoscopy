import pandas as pd
import numpy as np

dtPath = "./../datasets/Final_CleanedDT.csv"

#----------------------------------------- Create History Matrix
dt = pd.read_csv(dtPath)
minYear = np.min(dt.year)
maxYear = np.max(dt.year)

historyMatrix = pd.DataFrame()

for ind in dt.index:
     paitent_ID = dt['patient_ID'][ind]
     year = dt['year'][ind]
     state = dt['State'][ind]
     historyMatrix.loc[paitent_ID,year] = state

historyMatrix = historyMatrix.reindex(sorted(historyMatrix.columns), axis=1)
historyMatrix.to_csv("./../datasets/historyMatrix.csv", sep=',', encoding='utf-8')