import pandas as pd
import numpy as np

dtPath = "./../datasets/Final_CleanedDT.csv"

#----------------------------------------- Create History Matrix
dt = pd.read_csv(dtPath)
minYear = np.min(dt.year)
maxYear = np.max(dt.year)

historyMatrix = pd.DataFrame({
    "patient_ID":dt.patient_ID.unique()
})

for year in range(minYear,maxYear+1):
    historyMatrix[str(year)] = -1

print(historyMatrix)