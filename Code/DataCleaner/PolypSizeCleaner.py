import numpy as np
import pandas as pd
import pandasql as ps

class PolypSizeCleaner:

    def __init__(self, dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.validateSizeColumns()   # A valid polyp must have either Size in mm or Size in cm in a specific format


    def validateSizeColumns(self):

        #if  self.checkValidityOfSize():

        self.cleanSizeInMM()
        self.setSizeInWordsBasedOnSizeInMM()
        self.convertSizeInNumberToSizeInWords()
        self.writeToFile()

        #else:
        #    self.printMessage("Your dataset has inconsistent records in Size please find 'Invalid-record' folder for more information ")


    def checkValidityOfSize(self):
        return  self.checkMMSizeFormat()

    def checkMMSizeFormat(self):                    #The only valid size is int-int mm, int mmm, or NA

        invalidSizeFormat = self.cleanedDataSet.loc[~self.cleanedDataSet.loc[:," Size (in mm)"].str.contains('^(?:\d+-\d+mm|\d+mm)$', na=True), ['PolypID','facility','patient_ID','year','month',' Size (in mm)']]
        query= """
                select *
                from invalidSizeFormat
                where ` Size (in mm)` !=0
        """
        invalidSizeFormat = ps.sqldf(query)
        invalidSizeFormat.to_csv("./datasets/invalid-records/invalidSizeFormatMM.csv", sep=',', encoding='utf-8', index=False)
        return (np.shape(invalidSizeFormat)[0]== 0)

    def cleanSizeInMM(self):

        self.cleanedDataSet[" Size (in mm)"] = self.cleanedDataSet[" Size (in mm)"].str.replace(' ', '0')

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

    def printMessage(self,message):
        print("..............................................................")
        print(message)
        print("..............................................................")

    def convertSizeInNumberToSizeInWords(self):

        self.cleanedDataSet["Size of Sessile in Words"].replace("1", "Small", inplace=True)
        self.cleanedDataSet["Size of Sessile in Words"].replace("2", "Small", inplace=True)  # in real world 2 = Diminiutive

        self.cleanedDataSet["Size of Sessile in Words"].replace("3", "Medium",inplace=True)  # in real world 3 = Semi
        self.cleanedDataSet["Size of Sessile in Words"].replace("4", "Medium",inplace=True)  # in real world 4 = Medium

        self.cleanedDataSet["Size of Sessile in Words"].replace("5", "Large", inplace=True)  # in real world 5 = Large

