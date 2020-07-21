import numpy as np
import pandas as pd
import json
import math
import collections

class PolypSizeFixMultipleCategory:

    def __init__(self, dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')

        self.getAllSizes()                  #  if size is 2,3,5,10mm then save it as [2,3,5,10] in the Size-Range column
        self.setSizeRange()                 # Specify the minimum and Maximum range of size of polyp

        self.dt = pd.DataFrame([], columns=self.cleanedDataSet.columns.tolist())

        self.itterate_Over_The_Rows_To_Find_Polyps_With_Multiple_Category()
        self.cleanedDataSet.drop([" Size-Range"], axis=1,inplace=True)  # Remove the helper column from main DT
        self.dt.drop([" Size-Range"], axis=1,inplace=True)  # Remove the helper column from main DT

        print("Is 2 dt has the same column?  ",collections.Counter(self.cleanedDataSet.columns.tolist()) == collections.Counter(self.dt.columns.tolist()))
        #print(self.dt.columns)
        #print(self.cleanedDataSet.columns)

        self.cleanedDataSet = pd.concat([self.cleanedDataSet,self.dt])
        self.writeToFile()


    def setSizeRange(self):
        self.cleanedDataSet.loc[:, " Size-Range"].apply(lambda x: [min(x), max(x)])


    def itterate_Over_The_Rows_To_Find_Polyps_With_Multiple_Category(self):

        for index, row in self.cleanedDataSet.iterrows():

            sizeCategory = self.specifyNumberOfSizeCategorizes(min(row[" Size-Range"]),max(row[" Size-Range"]))  # return something like [Small,Medium]
            polypNo = float(row["Number of sessiles"])

            if self.isPolypNrBiggerThanPolypSizes(len(sizeCategory),polypNo):
                selectedSizeCategory = ""

                minimumPolyp = polypNo % len(sizeCategory)
                if (polypNo % len(sizeCategory)) > 0 :
                    selectedSizeCategory = self.which_Size_Category_Must_Receive_1_Extra_Polyp(sizeCategory)
                    print("Selected Category for "+str( minimumPolyp) +" remaining polyp is: ",selectedSizeCategory)

                self.distributePolypsInDifferentSizeCategories(sizeCategory,row,minimumPolyp,selectedSizeCategory)
                print("Paitent_ID: ",row["patient_ID"] ," polypNo: ", row['Number of sessiles']," sizeCategoryLen: ", sizeCategory, "Len: ", len(sizeCategory))

                self.cleanedDataSet = self.cleanedDataSet.drop(index)

    def which_Size_Category_Must_Receive_1_Extra_Polyp(self,sizeCategory):

        pro = self.getRespectedProbability(sizeCategory)
        selectedcategorySize = self.specifyTheCategorySize(sizeCategory,pro)
        return selectedcategorySize

    def getRespectedProbability(self,sizeCategory):
        if sizeCategory == ["Small", "Medium","Large"] :
            return [.76,.17,.07]
        if sizeCategory == ["Small", "Medium"]:
            return [.82,.18]
        if sizeCategory == ["Medium", "Large"]:
            return [.7,.3]
        if len(sizeCategory) == 1:                        # if the list contains only Small or only Medium or only Large
            return [1]


    def specifyTheCategorySize(self,sizeCategory,pro):
        selectedCategory = np.random.choice(sizeCategory, p=pro)
        return selectedCategory

    def distributePolypsInDifferentSizeCategories(self,sizeCategory,row,minimumPolyp,selectedSizeCategory):

        for i in range(len(sizeCategory)):
            copiedRow = row.copy()
            print("i is:", i ,"Category is: ", sizeCategory[i])
            if selectedSizeCategory == sizeCategory[i]:
                copiedRow["Number of sessiles"] = minimumPolyp+1
            else:
                copiedRow["Number of sessiles"] = 1
            copiedRow = self.fillPolypSize(copiedRow, sizeCategory[i])
            print("i is:", i, "Category is: ", sizeCategory[i]+ "Polyp No: "+str(copiedRow["Number of sessiles"]))
            self.addEmptyRowToDT(copiedRow.values)
            print("------------------------------------------------------")


    def fillPolypSize(self,row,sizeCategory):
        if sizeCategory == "Small":
            row[" Size (in mm)"] = 1
        if sizeCategory == "Medium":
            row[" Size (in mm)"] = 7
        if sizeCategory == "Large":
            row[" Size (in mm)"] = 12
        return row


    def isPolypNrBiggerThanPolypSizes(self,categoryLength,polypNo):   #Check if the number of polyps are less than categorize of polyp sizes

        if polypNo > categoryLength and polypNo > 0 and categoryLength > 1 :
            return True
        else:
            return False

    def getAllSizes(self):

        if ' Size-Range' in self.cleanedDataSet.columns:
            self.cleanedDataSet.drop([' Size-Range'], axis=1, inplace=True)
        self.cleanedDataSet[' Size (in mm)'].fillna(0,inplace=True)
        col = self.cleanedDataSet[' Size (in mm)'].str.findall("(\d+)").apply(lambda x: list(map(float, x)))#.values

        self.cleanedDataSet.insert(45, ' Size-Range', col )  #45 is the column next to " Size (in mm)"

    def specifyNumberOfSizeCategorizes(self,min,max):
        if (min in range(0,6)) and (max in range(6,10)):        # 0<=Small<=5  6<=Medium<=9    10<=Medium
            res = ["Small","Medium"]
        elif (min in range(0,6)) and (max in range(10,100000)):
            res = ["Small", "Medium","Large"]
        elif (min in range(6,10)) and (max in range(10,100000)):
            res = ["Medium","Large"]
        elif (min in range(0,6)) and (max in range(0,6)) :
            res = ["Small"]
        elif (min in range(6,10)) and (max in range(6,10)) :
            res = ["Medium"]
        elif (min in range(10,100000)) and (max in range(10,100000)) :
            res = ["Large"]
        return res

    def addEmptyRowToDT(self, row):

        nRow = np.shape(self.dt)[0]
        self.dt.loc[nRow] = row

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
