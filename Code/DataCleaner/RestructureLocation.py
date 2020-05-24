import numpy as np
import pandas as pd

class RestructureLocation:

    def __init__(self,dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.setRight()
        self.setLeft()
        #self.removeAllLocationsButRightAndLeft()
        self.writeToFile(dataSetPath)

    def setRight(self):

        dt = self.cleanedDataSet.iloc[:, np.r_[81, 47:60]]  # 70 = PolyID
        dt = dt.fillna(0)
        dt = dt.astype(float)
        self.cleanedDataSet["Right "] = dt["cecum"] + dt["ascending colon"] +\
                                        dt["ileocecal valve"] + dt["hepatic flexure"] + \
                                        dt["transverse colon"] + dt["splenic flexure"] +\
                                        dt["appendix"] + dt["Right "]

    def setLeft(self):

        dt = self.cleanedDataSet.iloc[:, np.r_[81, 47:60]]  # 70 = PolyID
        dt = dt.fillna(0)
        dt = dt.astype(float)
        self.cleanedDataSet["Left"] = dt["descending colon"] + dt["sigmoid colon"] +\
                                      dt["rectum"] + dt["rectosigmoid"] + dt["Left"]

    def removeAllLocationsButRightAndLeft(self):

        self.cleanedDataSet.drop(
            ["cecum", "ascending colon", "ileocecal valve", "hepatic flexure",
             "transverse colon","splenic flexure", "appendix", "descending colon",
             "sigmoid colon", "rectum", "rectosigmoid"], axis=1,inplace=True)

    def writeToFile(self,dataSetPath):
        self.cleanedDataSet.to_csv(dataSetPath, sep=',', encoding='utf-8', index=False)
