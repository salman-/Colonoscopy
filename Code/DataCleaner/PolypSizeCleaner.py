import numpy as np
import pandas as pd

class PolypSizeCleaner:

    def __init__(self, dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.setSizeInWords()


    def setSizeInWords(self):

        self.cleanSizeInMM()
        self.setSizeInWordsBasedOnSizeInMM()
        self.writeToFile()

    def cleanSizeInMM(self):

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace(' ', '0')
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace('>10mm', '12')

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].fillna(0)
        self.cleanedDataSet[' Size (in mm)'] = self.cleanedDataSet[' Size (in mm)'].astype(str)

        self.cleanedDataSet[' Size (in mm)'] = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: sum(map(float, x))/len(x))
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].astype(float)


    def setSizeInWordsBasedOnSizeInMM(self):

        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                (self.cleanedDataSet[" Size (in mm)"].between(0,5)), "Size of Sessile in Words"] = "Small"

        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                (self.cleanedDataSet[" Size (in mm)"].between(5,10)), "Size of Sessile in Words"] = "Medium"
        
        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                 (10 < self.cleanedDataSet[" Size (in mm)"]), "Size of Sessile in Words"] = "Large"


    def writeToFile(self):
        self.cleanedDataSet.to_csv("./datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
