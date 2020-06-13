
import pandas as pd
import numpy as np

class FilterUnusefullData:

    def __init__(self,dataSetPath):
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.filterRecordsWithNoPathology()
        self.writeToFile()



    def filterRecordsWithNoPathology(self): # if a paitent does not have pathology in any of his 6 capsules it will be removed
        capsulePathology1 = self.dt.iloc[:, [73, 74, 75, 76, 78, 79, 80]].notna().all(axis=1)
        capsulePathology2 = self.dt.iloc[:, [114, 115, 116, 117, 119, 120, 121]].notna().all(axis=1)
        capsulePathology3 = self.dt.iloc[:, [156, 157, 158, 159, 162, 163, 164]].notna().all(axis=1)
        capsulePathology4 = self.dt.iloc[:, [198, 199, 200, 201, 203, 204, 205]].notna().all(axis=1)
        capsulePathology5 = self.dt.iloc[:, [239, 240, 241, 242, 244, 245, 246]].notna().all(axis=1)
        capsulePathology6 = self.dt.iloc[:, [280, 281, 282, 283, 285, 286, 287]].notna().all(axis=1)

        dictionary = {"capsulePathology1": capsulePathology1,
                      "capsulePathology2": capsulePathology2,
                      "capsulePathology3": capsulePathology3,
                      "capsulePathology4": capsulePathology4,
                      "capsulePathology5": capsulePathology5,
                      "capsulePathology6": capsulePathology6}

        filteredDT = pd.DataFrame(dictionary)  #Each column in this dataframe shows, if the pathology of respected capsule existed or not

        self.dt = self.dt[
            (filteredDT["capsulePathology1"] == True) | (filteredDT["capsulePathology2"] == True) | (filteredDT["capsulePathology3"] == True) |
            (filteredDT["capsulePathology4"] == True) | (filteredDT["capsulePathology5"] == True) | (filteredDT["capsulePathology6"] == True)]


    def writeToFile(self):
        self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)