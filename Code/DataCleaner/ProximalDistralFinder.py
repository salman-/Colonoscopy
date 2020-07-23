import numpy as np
import pandas as pd





class ProximalDistralFinder:

    def __init__(self, dataSethPath):
        self.dt = pd.read_csv(dataSethPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.proximalFinder()
        self.distalFinder()
        self.writeToFile()
        #self.fillNA()

    # Looks at the related location columns and rewrite the proximal and Distal Columns since the Original columns
    # of distal and proximal had problems
    def proximalFinder(self):
        conditions = [(self.dt["Cecum"] == "1") | (self.dt["Ascending Colon"] == "1") | (self.dt["Ileocecal Valve"] == "1")
                      | (self.dt["Hepatic Flexure"] == "1") | (self.dt["Transverse Colon"] == "1")]
        choices = [1]
        self.dt["Proximal/Right"] = np.select(conditions, choices, default=0)

    def distalFinder(self):
        conditions = [(self.dt["Splenic Flexure"] == "1") | (self.dt["Descending Colon"] == "1") |
                      (self.dt["Sigmoid Colon"] == "1") | (self.dt["Rectum"] == 1) | (self.dt["Rectosigmoid"] == "1")]
        choices = [1]
        self.dt["Distal/Left"] = np.select(conditions, choices, default=0)

    #def fillNA(self):
     #   self.dt = self.dt.fillna(0)

    def writeToFile(self):
        self.dt.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)



