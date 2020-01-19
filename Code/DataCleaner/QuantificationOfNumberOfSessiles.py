import numpy as np
import pandas as pd


class QuantificationOfNumberOfSessiles:

    def __init__(self,dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.convertQualtivativeValuesToNumbers()   # Sometimes Number of sessels are expressed with words such as Few, or Multiple.
                                                    # This func convert them to numbers

        self.distributeTheNumberOfSessileIntoLocations()
        self.writeToFile()

    def convertQualtivativeValuesToNumbers(self):   # "Number of sessiles" is some times explained in words which must be converted to numbers

        self.cleanedDataSet["Number of sessiles"].replace("few",2,inplace=True)
        self.cleanedDataSet["Number of sessiles"].replace("multiple", 3, inplace=True)
        self.cleanedDataSet["Number of sessiles"].replace("Multiple", 3, inplace=True)

        self.cleanedDataSet["Number of sessiles"].replace("probable",1,inplace=True)
        self.cleanedDataSet["Number of sessiles"].replace("several", 3, inplace=True)
        self.cleanedDataSet["Number of sessiles"].replace("many", 4, inplace=True)
        self.writeToFile()

    def distributeTheNumberOfSessileIntoLocations(self):

        self.cleanedDataSet.fillna(0, inplace=True)
        self.cleanedDataSet['Right '] = self.cleanedDataSet['Right '].astype(float)
        self.cleanedDataSet['Left'] = self.cleanedDataSet['Left'].astype(float)
        self.cleanedDataSet['Number of sessiles'] = self.cleanedDataSet['Number of sessiles'].astype(float)

        self.cleanedDataSet["Right "] = np.random.binomial(self.cleanedDataSet["Number of sessiles"],
                                                           self.cleanedDataSet["Right "] / (self.cleanedDataSet["Right "] + self.cleanedDataSet["Left"]))

        self.cleanedDataSet["Left"] = self.cleanedDataSet["Number of sessiles"] - self.cleanedDataSet["Right "]

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)


