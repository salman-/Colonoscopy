import  pandas as pd
import numpy as np

# How many percentage of the whole patients have Pathology records?

originalDTPath = "./datasets/Original DT/complete-non-cleaned-DT.csv"

dt = pd.read_csv(originalDTPath, error_bad_lines=False, index_col=False, dtype='unicode')

overallPaitentRecords = np.shape(dt)[0]

noPathology = dt[(dt["manual?"] == ("missing pathology report")) | (dt["manual?"]==("missing pathology"))]

recordsWithoutPathology = np.shape(noPathology)[0]
print(recordsWithoutPathology/overallPaitentRecords)

#---------------------------------------------------------------------------------------
# There are 2 columns with the same spell (Adenomatous, and adenomatous) in Pathology records. Do they have the same value?\

dTPath = "./datasets/Capsules/cleanedDataSet.csv"

dt = pd.read_csv(dTPath, error_bad_lines=False, index_col=False, dtype='unicode')

print(all(dt["adenomatous"]==dt["Adenomatous"]))

#--------------------------------------------------------------------------------------------

# Given that we only consider the size of polyps (Small, Medium, Large) How many different group of patients do we have?

dTPath = "./datasets/Final DT/MergedDT.csv"

dt = pd.read_csv(dTPath, error_bad_lines=False, index_col=False, dtype='unicode')
dtSize = dt[["Nr_Small","Nr_Medium","Nr_Large"]].astype(float)
dtSize.fillna(0,inplace=True)
print(dtSize.dtypes)
countBySize = dtSize.groupby(by=["Nr_Small","Nr_Medium","Nr_Large"], as_index=False).size().reset_index(name='Size')
print("Groupby Size")
print("Mean: "+str(np.mean(countBySize["Size"]))+"  Median: "+str(np.median(countBySize["Size"])))
countBySize.to_csv("./datasets/Final DT/countBySize.csv", sep=',', encoding='utf-8', index=False)
print(np.shape(countBySize)[0])

#-------------------------------------------------------------------------------

selectedColumns = ["Nr_Small","Left_x","Right _x","Nr_Medium","Left_y","Right _y","Nr_Large","Left","Right "]
dtSizeAndLocation = dt[selectedColumns].astype(float).fillna(0)

countBySizeAndLocation = dtSizeAndLocation.groupby(by=selectedColumns, as_index=False).size().reset_index(name='Size')
countBySizeAndLocation.to_csv("./datasets/Final DT/countBySizeAndLocation.csv", sep=',', encoding='utf-8', index=False)

print("Groupby Size and Location")
print("Mean: "+str(np.mean(countBySizeAndLocation["Size"]))+"  Median: "+str(np.median(countBySizeAndLocation["Size"])))
print(np.shape(countBySizeAndLocation)[0])
