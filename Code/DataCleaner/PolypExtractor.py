import numpy as np
import pandas as pd

'''dt.columns[40:81]   # Capsul 1
dt.columns[122:163]    # Capsul 3
dt.columns[163:204]    # Capsul 4
dt.columns[204:245]    # Capsul 5
dt.columns[245:286]    # Capsul 6'''


class PolypExtractor:

    def __init__(self, dataSetPath):
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')

        capsulData = {
            "Capsul": [1, 2, 3, 4, 5, 6],
            "Begin": [40, 81, 122, 163, 204, 245],
            "End" : [81, 122, 163, 204, 245, 286]
        }
        self.capsules = pd.DataFrame(capsulData)

        self.cleanedDataSet = pd.DataFrame([], columns=self.dt.columns[0:81])
        self.cleanDataSet()

    # ------------------------------------------------------------------------------

    def cleanDataSet(self):

        self.getPolyps()
        self.removeWhiteSpaces()
        self.writeToFile()

    def getPolyps(self):

        for rowId in list(range(1, self.dt.shape[0])):  # For each paitent
            for capsuleID in list(range(0, 6)):         # There are 6 Capsul

                if self.isAllCellsNULL(rowId, capsuleID):
                    row = self.getPolypeAndCapsul(rowId, capsuleID)
                    self.addEmptyRowToCleanedDataSet(row)

                print("---------------------------")


    def isAllCellsNULL(self, rowId, capsuleID):

        capsul = self.getCapsulRange( capsuleID)  # Capsul[0] is the begining of Capsul and Capsul[1] is the end of Capsul
        capsulBegin = capsul[0]
        capsulEnd = capsul[1]
        target = not all(pd.isnull(self.dt.iloc[rowId, capsulBegin:capsulEnd]))

        return target

    def getCapsulRange(self, capsulID):

        capsulBegin = self.capsules.iloc[capsulID, 1]
        capsulEnd = self.capsules.iloc[capsulID, 2]
        return (capsulBegin, capsulEnd)

    def getCapsul(self, rowId, capsulBegin, capsulEnd):
        print(self.dt.iloc[rowId, capsulBegin:capsulEnd])

    # ------------------------------------------------------------------------------

    def getPolypeAndCapsul(self, rowId, capsuleID):

        capsul = self.getCapsulRange(capsuleID)  # Capsul[0] is the begining of Capsul and Capsul[1] is the end of Capsul
        capsulBegin = capsul[0]
        capsulEnd = capsul[1]

        print("RowID: " + str(rowId) + " CapsuleID: " + str(capsuleID) + " capsulBegin: " + str(capsulBegin) + " capsulEnd: " + str(capsulEnd))
        print("-----")

        paitentHist = pd.concat([self.dt.iloc[rowId, 0:40], self.dt.iloc[rowId, capsulBegin:capsulEnd]])
        return pd.DataFrame([paitentHist.tolist()], columns=self.dt.columns[1:82]).values[0]

    # ------------------------------------------------------------------------------

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)

    def removeWhiteSpaces(self):
        self.cleanedDataSet.replace(" ", "", inplace=True)
        self.cleanedDataSet.replace("  ", "", inplace=True)
        self.cleanedDataSet.replace("   ", "", inplace=True)

    def addEmptyRowToCleanedDataSet(self, rowData):
        nRow = np.shape(self.cleanedDataSet)[0]
        self.cleanedDataSet.loc[nRow] = rowData
