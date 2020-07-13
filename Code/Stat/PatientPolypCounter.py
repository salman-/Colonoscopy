import pandas as pd
import numpy as np


class PolyppatientCounter:

    def __init__(self):
        self.dt = pd.read_csv('../datasets/Capsules/Indianapolis_filteredInvalid_filteredSize.csv')
        self.filter3Plus()
        nonAdvData = self.filterNonAdv()
        advData = self.filterAdv()
        self.polypDistribution(nonAdvData, "./../datasets/patient_Polyp_NOnAdv_Dist.csv")
        self.polypDistribution(advData, "./../datasets/patient_Polyp_Adv_Dist.csv")


    def polypDistribution (self, data, dtPath):
        gr = self.groupByPatients(data)
        dist = self.patientPolypCounter(gr)
        self.wirteToFile(dist, dtPath)




    def filterNonAdv(self):
        data = self.dt[(self.dt['Adenocarcinoma'] == 0) & (self.dt['High Grade Dysplasia'] == 0) &
                          (self.dt['Tubular Villous'] == 0) & (self.dt['Villous'] == 0) & (self.dt['Adenoma'] == 1)]
        return data

    def filterAdv(self):
        data = self.dt[(self.dt['Adenocarcinoma'] == 0) & ((self.dt['High Grade Dysplasia'] == 1 ) |
                          (self.dt['Tubular Villous'] == 1 ) | (self.dt['Villous'] == 1))]
        return data

    def filter3Plus(self):
        self.dt = self.dt[~(self.dt['Number of sessiles'] == '3+')]
        self.dt['Number of sessiles'] = self.dt['Number of sessiles'].astype(float)

    def groupByPatients(self,data):
        groupedDataSet = data.groupby(['facility', 'patient_ID', 'year', 'month'], as_index=False).sum()
        return groupedDataSet

    def patientPolypCounter(self,dt):
        patientPolypDist = dt['Number of sessiles'].value_counts()
        return patientPolypDist

    def wirteToFile(self,data, dtPath):
        data = data.sort_values()
        data.to_csv(dtPath, sep=',', encoding='utf-8', index=True)


