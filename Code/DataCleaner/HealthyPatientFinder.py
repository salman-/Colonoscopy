import pandas as pd
import numpy as np

class HealthyPatientFinder:

    #dataSethPath = "./../datasets/Original DT/sample_Detroit.csv"

    # dt = dt.iloc[1:3, [35,36,56,57,58,59,60,62, 63, 83, 84, 85, 86, 87,89, 90, 110, 111, 112, 113, 114,
    #            116, 117, 137, 138, 139, 140, 141,143, 144, 164, 165, 166, 167, 168,170, 171, 191, 192, 193, 194, 195]]

    def __init__(self, dataSethPath):
        self.dt = pd.read_csv(dataSethPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.findHealthyPatients()
        #self.all6CapsulesZero()
        self.wirteToFile()

    def findHealthyPatients(self):
        self.dt['new'] = np.nan
        for i in range(len(self.dt)):
            self.dt.iloc[i, 196] = all(self.dt.iloc[i, [35, 36, 56, 57, 58, 59, 60,
                                                        62, 63, 83, 84, 85, 86, 87,
                                                        89, 90, 110, 111, 112, 113, 114,
                                                        116, 117, 137, 138, 139, 140, 141,
                                                        143, 144, 164, 165, 166, 167, 168,
                                                        170, 171, 191, 192, 193, 194, 195]] == "0")
        self.dt = self.dt[self.dt['new'] == True]
        self.dt.drop(['new'], axis=1, inplace=True)

    def wirteToFile(self):
        self.dt.to_csv("./../datasets/patientWithState0_0_0.csv", sep=',', encoding='utf-8', index=False)


