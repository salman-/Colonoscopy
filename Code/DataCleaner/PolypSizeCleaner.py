import numpy as np
import pandas as pd

class PolypSizeCleaner:

    def __init__(self, dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.getSizeRange()
        #self.setSizeInWords()
        self.writeToFile()

    def getSizeRange(self):
        #self.cleanedDataSet[' Size-Range'] = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)")
        self.cleanedDataSet.drop([' Size-Range'], axis=1,inplace=True)
        if ' Size (in mm)' in self.cleanedDataSet.columns:
            self.cleanedDataSet[' Size (in mm)'].fillna(0,inplace=True)
        col = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: list(map(float, x)))

        self.cleanedDataSet.insert(45, ' Size-Range', col )
        self.getMinAndMax(0)
        self.getMinAndMax(13)

    def getMinAndMax(self,index):   # Must return min and max for each range
        sizeList = ???
        print("index: ",index," min:  ",np.min(sizeList)," max:  ", np.max(sizeList))
        return ???

    def setSizeInWords(self):

        self.cleanSizeInMM()
        self.setSizeInWordsBasedOnSizeInMM()
        self.writeToFile()

    def cleanSizeInMM(self):

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace(' ', '0')
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace('>10mm', '12')

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].fillna(0)
        self.cleanedDataSet[' Size (in mm)'] = self.cleanedDataSet[' Size (in mm)'].astype(str)

        self.cleanedDataSet[' Size (in mm)'] = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: sum(map(float, x))/len(x))   # Get the average of values such as "3-5mm"
        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].astype(float)


    def setSizeInWordsBasedOnSizeInMM(self):

        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                (self.cleanedDataSet[" Size (in mm)"].between(0,5)), "Size of Sessile in Words"] = "Small"

        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                (self.cleanedDataSet[" Size (in mm)"].between(6,9)), "Size of Sessile in Words"] = "Medium"
        
        self.cleanedDataSet.loc[ self.cleanedDataSet["Size of Sessile in Words"].isna() &
                                 (10 <= self.cleanedDataSet[" Size (in mm)"]), "Size of Sessile in Words"] = "Large"


    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
