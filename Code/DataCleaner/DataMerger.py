import pandas as pd
import pandasql as ps
import numpy as np

class DataMerger:         # After spliting the main dataset to small capsules then we can rebuild data based on our needs

    def __init__(self):

        self.getPolypsBasedOnSize("Small")
        self.mergeRowsForEachPaitent("Small")

        self.getPolypsBasedOnSize("Medium")
        self.mergeRowsForEachPaitent("Medium")

        self.getPolypsBasedOnSize("Large")
        self.mergeRowsForEachPaitent("Large")

        self.mergAllPolypsOfPaitents()


    def getPolypsBasedOnSize(self, size):

        polyp        = pd.read_csv("./../datasets/Capsules/polyp.csv")
        patientPolyp = pd.read_csv("./../datasets/Capsules/patientPolyp.csv")
        patient      = pd.read_csv("./../datasets/Capsules/patient.csv")
        location     = pd.read_csv("./../datasets/Capsules/location.csv")
        cancerStatus = pd.read_csv("./../datasets/Capsules/cancerStatus.csv")

        dt = patient.merge(patientPolyp, on='patient_ID')\
             .merge(polyp       , on='PolypID') \
             .merge(location, on='PolypID') \
             .merge(cancerStatus, on='PolypID')

        dt = dt[ dt["Size of Sessile in Words"]== size]

        dt = dt.drop(["PolypID","Number of Capsules","Shape","Size of Sessile in Words"], axis=1)
        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)

    def mergAllPolypsOfPaitents(self):      # Each user might have different size of polyps. Aggregate these polyps in 1 row

        smallPolyps = pd.read_csv("./../datasets/Polyps/Small.csv")
        mediumPolyps = pd.read_csv("./../datasets/Polyps/Medium.csv")
        largPolyps   = pd.read_csv("./../datasets/Polyps/Large.csv")

        MergedDT = smallPolyps.merge(mediumPolyps, how="outer",on=['facility','patient_ID','year','month']).merge(largPolyps, how="outer",on=['facility','patient_ID','year','month'])

        MergedDT.to_csv("./../datasets/Final DT/MergedDT.csv", sep=',', encoding='utf-8', index=False)

    def considerPolypsWithPathology(self, polypDT):   # if a polyp has no pathology then, the number its sesels must be 0 as well
                                                      # Biopsy is not counted
        sumOfPathologies = polypDT.loc[:, "Adenocarcinoma"] + polypDT.loc[:, "Villous"] + polypDT.loc[:, "adenoma"] + \
                           polypDT.loc[:, "high grade dysplasia"] + polypDT.loc[:, "Adenomatous-capital"] + \
                           polypDT.loc[:, "Tubular"]

        selectedRows = np.arange(len(polypDT))[sumOfPathologies == 0]
        polypDT.iloc[selectedRows, 1] = 0

        return polypDT

    def mergeRowsForEachPaitent(self,size):  # By applying a Group by and then a SUM it categorize the polyps of a patient on 1 row

        pathToSaveCSV = "./../datasets/Polyps/{0}.csv".format(size)
        dt = pd.read_csv(pathToSaveCSV)

        print("Size is:   "+size)
        dt = dt.groupby(by=['facility','patient_ID','year','month'], as_index=False).sum()
        dt["Size of Sessile in Words"] = size                                             #After sum, this col is concated, so it must be overwritten by correct value
        dt.rename(columns={'Number of sessiles': 'Nr_{0}'.format(size)},inplace=True)

        dt = self.considerPolypsWithPathology(dt)
        print("======================================================")
        print(dt)

        dt.to_csv(pathToSaveCSV, sep=',', encoding='utf-8', index=False)
