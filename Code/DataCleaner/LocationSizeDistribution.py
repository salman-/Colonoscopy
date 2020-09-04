import pandas as pd
import numpy as np


class LocationSizeDistribution:

    def __init__(self, dataSetPath):
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.changingToFloat()
        self.filterOutCapsulesWithValidLocation()
        x = self.multipleNumberOfPolypsByUniqueLocations()
        y = self.findCasesWithEqualNumberOfPolypsAndSumOfLocations()
        data = self.concat2dt(x,y)
        nonAdv =self.findNonAdv(data)
        adv = self.findAdvanced(data)
        self.wrriteToFile(nonAdv,adv)



    def wrriteToFile(self,nonadv,adv):
        nonadv.to_csv("./../datasets/nonAdvanced111.csv")
        adv.to_csv("./../datasets/Advanced111.csv")


    def changingToFloat(self):                             # Checked: Worked Correctly
        lst = ['Number of sessiles', 'Adenocarcinoma', 'Villous', 'Tubular Villous','High Grade Dysplasia', 'Adenoma',
               'Cecum', 'Ascending Colon', 'Ileocecal Valve', 'Hepatic Flexure', 'Transverse Colon', 'Splenic Flexure',
               'Descending Colon', 'Sigmoid Colon', 'Rectum', 'Rectosigmoid']
        self.dt[lst] = self.dt[lst].astype(float)


    def filterOutCapsulesWithValidLocation(self):          # Checked: Worked Correctly
        lst = ['Cecum', 'Ascending Colon', 'Ileocecal Valve', 'Hepatic Flexure', 'Transverse Colon', 'Splenic Flexure',
               'Descending Colon', 'Sigmoid Colon', 'Rectum', 'Rectosigmoid']

        # 1- filter out cases: "Polyp Num" > "Sum of Locations" & "Sum of Locations" >= 2
        self.dt = self.dt[~((self.dt.loc[:, 'Number of sessiles'] > (self.dt.loc[:,lst].sum(axis= 1))) &
                                                                    (self.dt.loc[:,lst].sum(axis= 1) >= 2))]
        # 2- filter out cases: "Polyp Num" < "Sum of Locations"
        self.dt = self.dt[~((self.dt.loc[:, 'Number of sessiles']) < (self.dt.loc[:, lst].sum(axis=1)))]

        # 3- filter out cases: "Sum of Locations"
        self.dt = self.dt[~(self.dt.loc[:, lst].sum(axis = 1) == 0)]


    def multipleNumberOfPolypsByUniqueLocations(self):  # Multiplies the "Num of Polyps" by locations when there is only one location
        # Checked: Worked Properly
        lst = ['Cecum', 'Ascending Colon', 'Ileocecal Valve', 'Hepatic Flexure', 'Transverse Colon', 'Splenic Flexure',
               'Descending Colon', 'Sigmoid Colon', 'Rectum', 'Rectosigmoid']
        data1 = self.dt[self.dt.loc[:, lst].sum(axis=1) == 1]
        lc = data1.columns.get_loc("Number of sessiles")

        for i in range(len(data1)):
            data1.iloc[i, [37,38,39,40,41,42,43,44,47,48]] = data1.iloc[i, lc] * data1.iloc[i, [37,38,39,40,41,42,43,44,47,48]]

        return data1

    def findCasesWithEqualNumberOfPolypsAndSumOfLocations(self):   # Find capsules when "Sum of Locations" >= 2 and it
                                                                   # is euqual to "Num of Polyps"
        # Checked: Worked Properly
        lst = ['Cecum', 'Ascending Colon', 'Ileocecal Valve', 'Hepatic Flexure', 'Transverse Colon', 'Splenic Flexure',
               'Descending Colon', 'Sigmoid Colon', 'Rectum', 'Rectosigmoid']
        data1 = self.dt[((self.dt.loc[:, 'Number of sessiles']) ==  (self.dt.loc[:, lst].sum(axis=1))) &
                        (self.dt.loc[:, lst].sum(axis=1) >= 2)]

        return data1

    def concat2dt(self,data1,data2):
        data = pd.concat([data1, data2])
        return data


    def findAdvanced(self,data):
        # Checked: Worked Properly
        advData = data[(data.loc[:, "Adenocarcinoma"] == 0) & ((data.loc[:, "Villous"] != 0) |
                (data.loc[:, "Tubular Villous"] != 0) | (data.loc[:, "High Grade Dysplasia"] != 0))]

        return advData


    def findNonAdv(self,data):
        # Checked: Worked Properly
        nonAdvdata = data[(data.loc[:, "Adenocarcinoma"] == 0) & (data.loc[:, "Villous"] == 0) &
                (data.loc[:, "Tubular Villous"] == 0) & (data.loc[:, "High Grade Dysplasia"] == 0) &
                (data.loc[:, "Adenoma"] != 0)]
        return nonAdvdata

