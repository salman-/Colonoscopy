import numpy as np
import pandas as pd

class proximalAndDistalFinder:
    def __init__(self):
        self.dt = pd.read_csv('../datasets/Capsules/cleanedDataSet.csv')
        self.proximalFinder()
        self.distalFinder()


    def proximalFinder(self):
        conditions = [(self.dt["Cecum"] == 1) | (self.dt["Ascending Colon"] == 1) | (self.dt["Hepatic Flexure"] == 1) |
                      (self.dt["Transverse Colon"] == 1)]
        choices = [1]
        self.dt["Proximal/Right"] = np.select(conditions, choices, default=0)

    def distalFinder(self):
        conditions = [(self.dt["Splenic Flexure"] == 1) | (self.dt["Descending Colon"] == 1) |
                      (self.dt["Sigmoid Colon"] == 1) | (self.dt["Rectum"] == 1) | (self.dt["Rectosigmoid"] == 1)]
        choices = [1]
        self.dt["Distal/Left"] = np.select(conditions, choices, default=0)

    def writeToFile(self):
        self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)



