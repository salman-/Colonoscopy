import numpy as np
import pandas as pd
import json
import math

class PolypSizeCleaner:

    def __init__(self, dataSetPath):
        """small_medium_large  = [.76,.16,.07]
        small_medium = [.82,.18]
        medium_large  = [.7,.3]    ##
        self.index = 0"""
        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.polypsInSize = pd.DataFrame([], columns=self.cleanedDataSet.columns)  # After polyps No is distributed into size categorize,
                                                                                   # the new record will be saved in this dt
        #self.cleanedDataSet[" Size-Range-Len"] = math.nan
        self.cleanedDataSet.insert(46, ' Size-Range-Len', math.nan)
        self.getSizeRange()
        #self.setSizeInWords()
        self.cleanedDataSet = self.distributePolypsInDifferentSizeCategories()
        self.writeToFile()

    def distributePolypsInDifferentSizeCategories(self):

        for index, row in self.cleanedDataSet.iterrows():
            sizeRange = self.getMinAndMax(index)
            sizeCategory = self.specifyNumberOfSizeCategorizes(sizeRange[0], sizeRange[1])
            self.cleanedDataSet.loc[index,"Size-Range-Len"] = len(sizeCategory)
            polypNo = float(row["Number of sessiles"])

            print("index: ",index ,"polypNo: ",row['Number of sessiles']," sizeCategoryLen: ",sizeCategory, "Len: ",self.cleanedDataSet.loc[index,"Size-Range-Len"])

            """if self.isPolypNrBiggerThanPolypSizes(index):
                print("isPolypNrBiggerThanPolypSizes: ",self.isPolypNrBiggerThanPolypSizes(index))
                for i in range(len(sizeCategory)):
                    copiedRow = row.copy()
                    copiedRow["Number of sessiles"] = 1

                    if sizeCategory[i] == "Small":
                        copiedRow[" Size (in mm)"] = 1
                        copiedRow['Number of sessiles'] = ??
                    if sizeCategory[i] == "Medium":
                        copiedRow[" Size (in mm)"] = 7
                    if sizeCategory[i] == "Large":
                        copiedRow[" Size (in mm)"] = 12
                    self.polypsInSize.append( copiedRow )

            print("Deleted")
            #self.cleanedDataSet = self.cleanedDataSet.drop(index)"""

        return self.cleanedDataSet


    def isPolypNrBiggerThanPolypSizes(self,index):   #Check if the number of polyps are less than categorize of polyp sizes
        sizeCategory = len(self.getMinAndMax(index))
        minMax = self.getMinAndMax(index)
        sizeCategoryLen = len(self.specifyNumberOfSizeCategorizes(minMax[0],minMax[1]))
        polypNo = float(self.cleanedDataSet.loc[index,'Number of sessiles'])
        res = (polypNo >= sizeCategoryLen)
        return res

    def getSizeRange(self):

        if ' Size-Range' in self.cleanedDataSet.columns:
            self.cleanedDataSet.drop([' Size-Range'], axis=1, inplace=True)
        self.cleanedDataSet[' Size (in mm)'].fillna(0,inplace=True)
        col = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: list(map(float, x)))

        self.cleanedDataSet.insert(45, ' Size-Range', col )  #45 is the column next to " Size (in mm)"

    def getMinAndMax(self,index):   # Must return min and max for each range of size.
        #sizeList =json.loads(self.cleanedDataSet.loc[index, " Size-Range"])    #https://stackoverflow.com/questions/62114610/how-can-i-convert-a-string-to-a-list
        sizeList = self.cleanedDataSet.loc[index, " Size-Range"]
        #print("index: ",index," sizeList: ",sizeList)
        return [np.min(sizeList), np.max(sizeList)]

    def specifyNumberOfSizeCategorizes(self,min,max):
        if (min in range(0,6)) and (max in range(6,10)):        # 0<=Small<=5  6<=Medium<=9    10<=Medium
            res = ["Small","Medium"]
        elif (min in range(0,6)) and (max in range(10,1000)):
            res = ["Small", "Medium","Large"]
        elif (min in range(6,10)) and (max in range(10,1000)):
            res = ["Medium","Large"]
        elif (min in range(0,6)) and (max in range(0,6)) :
            res = ["Small"]
        elif (min in range(6,10)) and (max in range(6,10)) :
            res = ["Medium"]
        elif (min in range(10,1000)) and (max in range(10,1000)) :
            res = ["Large"]
        return res

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

    """def addEmptyRowToPolypsInSize(self):
        nCol = np.shape(self.polypsInSize)[1]
        nRow = np.shape(self.polypsInSize)[0]
        row = np.empty((1, nCol,))[0]
        row[:] = np.nan
        self.polypsInSize.loc[nRow] = row
        return self.polypsInSize"""

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
