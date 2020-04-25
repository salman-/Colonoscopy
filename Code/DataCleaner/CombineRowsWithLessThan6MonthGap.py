import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)


class CombineRowsWithLessThan6MonthGap():

    def __init__(self,dtPath):

        self.dt = pd.read_csv(dtPath)
        self.dt["id"] = [x for x in range(1, len(self.dt)+1)]
        patients = self.dt.loc[:,"patient_ID"]

        for patient in patients:
            patientDT = self.dt[self.dt.patient_ID == patient]
            if np.shape(patientDT)[0] > 1:

                patientDT.sort_values(['year', 'month'], ascending=[True, True], inplace=True)
                print(patientDT)
                first2Rows = self.getTheFirst2rows(patientDT)
                res = self.isTheTimeDifferenceMoreThan6Month(first2Rows)
                if res:
                    aggregatedRow = self.sumPolyps(first2Rows)
                    self.dt = self.dt[~self.dt.id.isin(first2Rows.id.tolist())]
                    self.dt = self.dt.append(aggregatedRow, ignore_index=True)
                print("------------------------------")
        self.saveOutPut()


    def getTheFirst2rows(self,patientDT):
        return patientDT.iloc[:2, :]

    def isTheTimeDifferenceMoreThan6Month(self,dt):
        dt = dt.reset_index(drop=True)
        firstVisitDate = dt.loc[0,"year"]*12 + dt.loc[0,"month"]
        secondVisitDate = dt.loc[1,"year"]*12 + dt.loc[1,"month"]
        timeDifference = secondVisitDate - firstVisitDate
        res = timeDifference < 180
        print("firstVisitDate: "+ str(firstVisitDate) +" secondVisitDate: "+ str(secondVisitDate) +" Is Time Gap > 6: "+ str(res))
        return res

    def sumPolyps(self,dt):
        dt = dt.reset_index(drop=True)
        dt.loc[0,"Nr_Small"]  = dt.loc[0,"Nr_Small"]+dt.loc[1,"Nr_Small"]
        dt.loc[0,"Nr_Medium"] = dt.loc[0,"Nr_Medium"]+dt.loc[1,"Nr_Medium"]
        dt.loc[0,"Nr_Large"]  = dt.loc[0,"Nr_Large"]+dt.loc[1,"Nr_Large"]
        dt.loc[0, "State"] = str(dt.loc[0,"Nr_Small"]) + "_" + str(dt.loc[0, "Nr_Medium"]) + "_" + str(dt.loc[1, "Nr_Large"])
        return dt.loc[0,:]

    def saveOutPut(self):
        self.dt.to_csv("./../datasets/Final_CleanedDT2.csv", sep=',', encoding='utf-8', index=False)