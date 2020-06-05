import pandas as pd
import numpy  as np
import pandasql as ps

class DataSeperator:

    def __init__(self,cleanedDTPath):

        self.dataset = pd.read_csv(cleanedDTPath)
        #print("=======================  DataSeperator ============================")
        #print(self.dataset.columns)
        self.seperatePatient()
        self.createPaitentPolypTable()
        self.seperatePolyp()
        #self.seperateSymptoms()
        #self.seperateTherapy()
        self.sperateLocation()
        self.sperateCancerStatus()

    def seperatePatient(self):
        col = ['facility', 'record #', 'patient_ID', 'year', 'month', 'dt', 'manual?', 'row - indications', 'row - findings', 'row - pathology', 'Unnamed: 10']
        dt = self.dataset.loc[:, col]

        #dt = self.dataset.iloc[:, 0:11]
        #print("=======================  seperatePatient ============================")
        #print(dt.columns)

        paitentGroupQuery = """    select facility,patient_ID, year, month,dt, count(*) as `Number of Capsules`
                                   from dt
                                   group by patient_ID, year, month """

        patient = ps.sqldf(paitentGroupQuery)

        patient.to_csv("./../datasets/Capsules/patient.csv", sep=',', encoding='utf-8', index=False)

    def createPaitentPolypTable(self):
        col = ['patient_ID','PolypID']
        dt = self.dataset.iloc[:, np.r_[1, 3]]  # Col 1 is PolypID and 3 is patient_ID
        """print("=======================  createPaitentPolypTable ============================")
        print(dt.columns)"""

        dt.to_csv("./../datasets/Capsules/patientPolyp.csv", sep=',', encoding='utf-8', index=False)

    def seperateSymptoms(self):
        symptoms = self.dataset.drop_duplicates(self.dataset.columns[np.r_[2, 10:40]]).iloc[:, np.r_[70, 10:40]]     # 81 = PolyID
        symptoms.to_csv("./../datasets/Capsules/symptoms.csv", sep=',', encoding='utf-8', index=False)

    def seperatePolyp(self):
        col = ['PolypID', 'Number of sessiles', 'Size of Sessile in Words', 'Shape']
        #polyp = self.dataset.loc[:, col]
        polyp = self.dataset.iloc[:, np.r_[1, 42:45]]                                                   # 1 = PolyID
        #print("======================= seperatePolyp ============================")
        #print(polyp.columns)
        polyp.to_csv("./../datasets/Capsules/polyp.csv", sep=',', encoding='utf-8', index=False)

    def sperateLocation(self):
        col = ['PolypID','cecum', 'ascending colon', 'ileocecal valve', 'hepatic flexure', 'transverse colon', 'splenic flexure',
       'descending colon', 'sigmoid colon', 'rectum', 'appendix', 'rectosigmoid', 'Left', 'Right ']
        location = self.dataset.iloc[:, np.r_[1, 48:61]]                                             # 1 = PolyID
        #location = self.dataset.loc[:, col]
        #print("======================= sperateLocation ============================")
        #print(location.columns)
        location.to_csv("./../datasets/Capsules/location.csv", sep=',', encoding='utf-8', index=False)

    def seperateTherapy(self):
        therapy = self.dataset.iloc[:, np.r_[70, 46, 60:72]]                              # 81 = PolyID and  46= At Cm
        therapy.to_csv("./../datasets/Capsules/therapy.csv", sep=',', encoding='utf-8', index=False)

    def sperateCancerStatus(self):
        col = ['PolypID', 'Adenocarcinoma', 'Villous', 'adenoma', 'high grade dysplasia', 'Biopsy', 'adenomatous', 'Adenomatous', 'Tubular']
        #cancerStatus = self.dataset.loc[:, col]
        cancerStatus = self.dataset.iloc[:, np.r_[1, 74:82]]                   # 2 = Paitent_ID and 81 = Tubular
        #print("======================= sperateCancerStatus ============================")
        #print(cancerStatus.columns)

        cancerStatus = cancerStatus.rename(columns={'Adenomatous':'Adenomatous-capital'})
        cancerStatus.to_csv("./../datasets/Capsules/cancerStatus.csv", sep=',', encoding='utf-8', index=False)

    def printColumns(self,fromColumn,toColumn):
        print(self.dataset.columns(np.r_[fromColumn:toColumn]))