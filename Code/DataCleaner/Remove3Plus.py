import numpy as np
import pandas as pd



class Remove3Plus:
    def __init__(self, dataSetPath):
            self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
            self.dt = self.dt[~(self.dt["Number of sessiles"] == "3+")]
            self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)

