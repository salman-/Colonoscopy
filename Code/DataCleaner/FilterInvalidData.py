
import pandas as pd
import numpy as np


class FilterInvalidData:

    def __init__(self,dtPath):
        self.dt = pd.read_csv(dtPath , error_bad_lines=False, index_col=False, dtype='unicode')
        self.filter1()
        self.filter2()
        self.fiter3()
        self.filter4()
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

    def fiter3 (self):          # Remove: Number of Polyp == 0, Size != 0, Pathology != 0
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


    def writeToFile(self):
        self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
