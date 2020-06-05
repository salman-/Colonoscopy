import numpy as np
import pandas as pd
import json
import math

class PolypSizeCleaner:

    def __init__(self, dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')

        self.cleanSizeInMM()
        self.setSizeInWordsBasedOnSizeInMM()
        self.writeToFile()

    def cleanSizeInMM(self):

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace(' ', "0")
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].fillna(0).astype(str)
        self.cleanedDataSet[' Size (in mm)'] = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: sum(map(float, x))/len(x))   # Get the average of values such as "3-5mm"
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].astype(float)

    def setSizeInWordsBasedOnSizeInMM(self):

        self.cleanedDataSet.loc[(self.cleanedDataSet[" Size (in mm)"].between(0,5.99)), "Size of Sessile in Words"] = "Small"
        self.cleanedDataSet.loc[(self.cleanedDataSet[" Size (in mm)"].between(6,9.99)), "Size of Sessile in Words"] = "Medium"
        self.cleanedDataSet.loc[ (10 <= self.cleanedDataSet[" Size (in mm)"]), "Size of Sessile in Words"] = "Large"

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
