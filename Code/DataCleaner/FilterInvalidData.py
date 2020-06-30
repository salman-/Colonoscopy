
import pandas as pd
import numpy as np


class FilterInvalidData:

    def __init__(self,dtPath):

        self.dt = pd.read_csv(dtPath , error_bad_lines=False, index_col=False, dtype='unicode')
        self.filter1()
        self.filter2()
        self.filter3()
        self.filter4()
        self.filter5()
        self.writeToFile()


    def filter1 (self):         # Remove: Number of Polyp == 0, Size == 0, Pathology == 0

        condition = ~((self.dt.loc[:, "Number of sessiles"] == "0") & (self.dt.loc[:, " Size (in mm)"] == "0") &
                     (self.dt.loc[:, "Adenocarcinoma"] == "0") & (self.dt.loc[:, "Villous"] == "0") &
                     (self.dt.loc[:, "Tubular Villous"] == "0") & (self.dt.loc[:, "High Grade Dysplasia"] == "0") &
                     (self.dt.loc[:, "Adenoma"] == "0"))

        self.dt = self.dt.loc[condition, :]


    def filter2 (self):         # Remove: Number of Polyp == 0, Size == 0, Pathology != 0

        condition = ~((self.dt.loc[:,"Number of sessiles"] == "0") & (self.dt.loc[:," Size (in mm)"]== "0") &
                          ((self.dt.loc[:,"Adenocarcinoma"]!= "0")  |  (self.dt.loc[:,"Villous"]!= "0") |
                          (self.dt.loc[:,"Tubular Villous"]!= "0") | (self.dt.loc[:,"High Grade Dysplasia"]!= "0") |
                          (self.dt.loc[:,"Adenoma"]!= "0")))

        self.dt = self.dt.loc[condition, :]

    def filter3 (self):          # Remove: Number of Polyp == 0, Size != 0, Pathology != 0

        condition = ~((self.dt.loc[:,"Number of sessiles"] == "0") & (self.dt.loc[:," Size (in mm)"]!= "0") &
                          ((self.dt.loc[:,"Adenocarcinoma"]!= "0")  |  (self.dt.loc[:,"Villous"]!= "0") |
                          (self.dt.loc[:,"Tubular Villous"]!= "0") | (self.dt.loc[:,"High Grade Dysplasia"]!= "0") |
                          (self.dt.loc[:,"Adenoma"]!= "0")))
        self.dt = self.dt.loc[condition, :]

    def filter4 (self):         # Remove: Number of Polyp != 0, Size == 0, Pathology != 0

        condition = ~((self.dt.loc[:,"Number of sessiles"] != "0") & (self.dt.loc[:," Size (in mm)"]== "0") &
                          ((self.dt.loc[:,"Adenocarcinoma"]!= "0")  |  (self.dt.loc[:,"Villous"]!= "0") |
                          (self.dt.loc[:,"Tubular Villous"]!= "0") | (self.dt.loc[:,"High Grade Dysplasia"]!= "0") |
                          (self.dt.loc[:,"Adenoma"]!= "0")))
        self.dt = self.dt.loc[condition, :]

    def filter5(self):         # Remove the rows which its polypNo is less than size categorizes

        self.getAllSizes()                  #  if size is 2,3,5,10mm then save it as [2,3,5,10] in the Size-Range column
        self.setSizeRange()                 # Specify the minimum and Maximum range of size of polyp
        self.dt = self.dt.loc[self.dt[" Size-Category-No"].astype(float) >= self.dt.loc[:,"Number of sessiles"].astype(float)]  # Polyp No must be bigger than Size-Range
#---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
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
