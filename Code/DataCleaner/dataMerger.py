import pandas as pd
import pandasql as ps
import numpy as np

class DataMerger:         # After spliting the main dataset to small capsules then we can rebuild data based on our needs

    def __init__(self):

        self.getPolypsBasedOnSize("Small")
        self.omitUnusedColumns("Small")
        self.mergeRowsForEachPaitent("Small")

        self.getPolypsBasedOnSize("Medium")
        self.omitUnusedColumns("Medium")
        self.mergeRowsForEachPaitent("Medium")

        self.getPolypsBasedOnSize("Large")
        self.omitUnusedColumns("Large")
        self.mergeRowsForEachPaitent("Large")

        self.mergAllPolypsOfPaitents()


    def getPolypsBasedOnSize(self, size):

        polyp        = pd.read_csv("./../datasets/Capsules/polyp.csv")
        patientPolyp = pd.read_csv("./../datasets/Capsules/patientPolyp.csv")
        patient      = pd.read_csv("./../datasets/Capsules/patient.csv")
        location     = pd.read_csv("./../datasets/Capsules/location.csv")
        cancerStatus = pd.read_csv("./../datasets/Capsules/cancerStatus.csv")

        polypQuery = """ 
                       select patient.ID, 
                              polyp.`Number of sessiles` as Nr_{0} , location.*, cancerStatus.*

                       from   patient join patientPolyp on patient.ID           = patientPolyp.`PatientID-Date`
                                      join polyp        on patientPolyp.PolypID = polyp.PolypID
                                      join location     on polyp.PolypID        = location.PolypID
                                      join cancerStatus on polyp.PolypID        = cancerStatus.PolypID
                       where    `Size of Sessile in Words` ="{1}"               
                                       """.format(size, size)

        polyps = ps.sqldf(polypQuery)

        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        polyps.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)

    def mergAllPolypsOfPaitents(self):      # Each user might have different size of polyps. Aggregate these polyps in 1 row

        samallPolyps = pd.read_csv("./../datasets/Polyps/Small.csv")

        mediumPolyps = pd.read_csv("./../datasets/Polyps/Medium.csv")

        largPolyps   = pd.read_csv("./../datasets/Polyps/Large.csv")

        patient      = pd.read_csv("./../datasets/Capsules/patient.csv")

        MergedDT = samallPolyps.merge(mediumPolyps, how="outer",on="ID").merge(largPolyps, how="outer",on="ID")
        MergedDT = patient.merge(MergedDT, how="inner",on="ID")
        MergedDT = MergedDT.drop(["ID"], axis=1)

        MergedDT.to_csv("./../datasets/Final DT/MergedDT.csv", sep=',', encoding='utf-8', index=False)

    def mergeRowsForEachPaitent(self,size):  # By applying a Group by and then a SUM it categorize the polyps of a patient on 1 row

        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt = pd.read_csv(pathToSaveCSV).astype(float)

        columns = list(dt.columns[1:])

        print("Size is:   "+size)
        dt = dt.groupby(by=['ID'], as_index=False)[columns].sum()
        print("======================================================")
        print(dt)

        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)

    def omitUnusedColumns(self,size):

        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt = pd.read_csv(pathToSaveCSV)
        dt = dt.fillna(0)

        dt = dt.drop(["PolypID","PolypID.1"],axis=1)
        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)
