import numpy as np
import pandas as pd
import json
import math

class SelectValidData:

    def __init__(self, dataSetPath):

        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.dt = self.dt.loc[self.dt["Number of sessiles"] != "3+"]    # Remove No with 3+
        self.dt = self.dt.loc[self.dt["Number of sessiles"] != "0" ]    # Remove No 0s
        self.dt = self.dt[self.dt["Number of sessiles"].notna()]        # Remove Nan in No
        self.dt = self.dt[self.dt[" Size (in mm)"].notna()]             # Remove Nan in Size
        self.dt = self.dt.loc[self.dt[" Size (in mm)"] != "0"]          # Remove Size with 0s
        print(self.dt)

        self.getAllSizes()                  #  if size is 2,3,5,10mm then save it as [2,3,5,10] in the Size-Range column
        self.setSizeRange()                 # Specify the minimum and Maximum range of size of polyp
        self.dt = self.dt.loc[
                        self.dt[" Size-Category-No"].astype(float) ==1]  # Polyp No must be bigger than Size-Range
        capsulePathology1 = self.dt.iloc[:, [73, 74, 75, 76, 78, 79, 80]].notna().all(axis=1)   # Get capsules with valid pathology
        self.dt = self.dt[capsulePathology1]

        self.writeToFile()

    def getAllSizes(self):

        col = self.dt[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: list(map(float, x)))
        self.dt.insert(45, ' Size-Range', col)  #45 is the column next to " Size (in mm)"

    def setSizeRange(self):
        sizeCategoryLength = self.dt.loc[:, " Size-Range"].apply(lambda x: self.specifyLengthOfSizeCategorizes(min(x), max(x))).values
        self.dt.insert(45, ' Size-Category-No', sizeCategoryLength)

    def specifyLengthOfSizeCategorizes(self, min, max):
        if (min in range(0,6)) and (max in range(6,10)):        # 0<=Small<=5  6<=Medium<=9    10<=Medium
            res = 2  #["Small","Medium"]
        elif (min in range(0,6)) and (max in range(10,1000)):
            res = 3  #["Small", "Medium","Large"]
        elif (min in range(6,10)) and (max in range(10,1000)):
            res = 2  #["Medium","Large"]
        elif (min in range(0,6)) and (max in range(0,6)) :
            res = 1  #["Small"]
        elif (min in range(6,10)) and (max in range(6,10)) :
            res = 1  #["Medium"]
        elif (min in range(10,1000)) and (max in range(10,1000)) :
            res = 1  #["Large"]
        return res

    def writeToFile(self):
        self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)