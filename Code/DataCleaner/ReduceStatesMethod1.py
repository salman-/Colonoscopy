import pandas as pd
import pandas as np

"""
Method1 reduces the the number of states performs as below:
1. Obtain sum of all polyps (let's call it "sum of polyps") in different sizes (Small,Medium,Large)
2. If the "Sum of Polyps" is more than 6 then consider the state as 666
"""


class ReduceStatesMethod1:

    def __init__(self,inputDTPath):

        self.dtPath = inputDTPath
        self.mainDt = pd.read_csv(self.dtPath)
        self.mainDt = self.mainDt[["facility","patient_ID","year","month","dt",
                                   "Nr_Small","Adenocarcinoma_x_x",
                                   "Nr_Medium","Adenocarcinoma_x_y",
                                   "Nr_Large","Adenocarcinoma_y"]]
        self.mainDt.fillna(0,inplace=True)
        dt = self.mainDt.iloc[:,1:11].astype(int).astype(str)
        self.mainDt["State"] = dt["Nr_Small"]+"_"+dt["Nr_Medium"]+"_"+dt["Nr_Large"]     # Add State column
        self.mainDt["Adenocarcinoma"] = dt["Adenocarcinoma_x_x"].astype(float)+dt["Adenocarcinoma_x_y"].astype(float)+dt["Adenocarcinoma_y"].astype(float)
        self.mainDt.drop(['Adenocarcinoma_x_x', 'Adenocarcinoma_y','Adenocarcinoma_x_y'], axis=1, inplace=True)

    def labelThePaitentsWithMoreThan6PolypsAs6_6_6(self):  #
        recordsWith6PolypsOrMore = list(state > 6 for state in [sum(map(float, s.split('_'))) for s in self.mainDt.State])
        self.mainDt.loc[recordsWith6PolypsOrMore,["State"]] = '6_6_6'

    def labelThePaitentsWithCancersAs9_9_9(self):
        self.mainDt.loc[self.mainDt["Adenocarcinoma"]>0,["State"]] = '9_9_9'


    def output(self,outputDTPath):
        self.mainDt.to_csv(outputDTPath, sep=',', encoding='utf-8', index=False)

