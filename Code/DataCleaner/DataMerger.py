import pandas as pd
import numpy as np

class DataMerger:     # After spliting the main dataset to small capsules then we can rebuild data based on our needs

    def __init__(self, advanceFlag):

        self.dt = pd.read_csv("./../datasets/Capsules/cleanedDataSet.csv")
        if advanceFlag == 1:
            print("sub set advanced data")
            self.getAdvancedDT()
            self.dtPath = "./../datasets/Final DT/NonAdvancedMergedDT.csv"
        elif advanceFlag == 2:
            print("sub set non-advanced data")
            self.getNonAdvancedDT()
            self.dtPath = "./../datasets/Final DT/AdvancedMergedDT.csv"
        else:
            self.dtPath = "./../datasets/Final DT/MergedDT.csv"
            print("No preferance on Advance non-advance")

        self.getPolypsBasedOnSize("Small")
        self.mergeRowsForEachPaitent("Small")

        self.getPolypsBasedOnSize("Medium")
        self.mergeRowsForEachPaitent("Medium")

        self.getPolypsBasedOnSize("Large")
        self.mergeRowsForEachPaitent("Large")

        self.mergAllPolypsOfPaitents()

    def getAdvancedDT(self):
        self.dt = #???

    def getNonAdvancedDT(self):
        self.dt = #???

    def getPolypsBasedOnSize(self, size):

        dt = self.dt[self.dt["Size of Sessile in Words"].str.contains(size)]  # Select columns by Size
        #dt = dt.drop(["Number of Capsules","PolypID"], axis=1)
        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)

    def mergeRowsForEachPaitent(self,size):  # By applying a Group by and then a SUM it categorize the polyps of a patient on 1 row

        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt = pd.read_csv(pathToSaveCSV)
        dt = dt.groupby(by=['facility','patient_ID','year','month'], as_index=False).sum()

        #dt.apply(print)
        dt = dt[['facility','patient_ID','year','month','Number of sessiles','Adenocarcinoma','High Grade Dysplasia','Tubular Villous','Villous','Adenoma']]
        dt.rename(columns={'Number of sessiles': 'Nr_{0}'.format(size)},inplace=True)
        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)

    def mergAllPolypsOfPaitents(self):      # Each user might have different size of polyps. Aggregate these polyps in 1 row

        smallPolyps = pd.read_csv("./../datasets/Polyps/Small.csv")
        print("======================== smallPolyps =============================")
        print(smallPolyps)
        mediumPolyps = pd.read_csv("./../datasets/Polyps/Medium.csv")
        print("======================== mediumPolyps ===========================")
        print(mediumPolyps)
        largPolyps   = pd.read_csv("./../datasets/Polyps/Large.csv")
        print("========================= largPolyps =============================")
        print(largPolyps)

        MergedDT = smallPolyps.merge(mediumPolyps, how="outer",on=['facility','patient_ID','year','month']).merge(largPolyps, how="outer",on=['facility','patient_ID','year','month'])

        MergedDT.to_csv(self.dtPath, sep=',', encoding='utf-8', index=False)



