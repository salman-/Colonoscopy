import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)


class CombineRowsWithLessThan6MonthGap:

    def __init__(self,dtPath):

        self.mainDT = pd.read_csv(dtPath)
        self.mainDT["id"] = [x for x in range(1, len(self.mainDT) + 1)]
        patients = self.mainDT.loc[:, "patient_ID"].unique()

        for patient in patients:
            patientDT = self.mainDT[self.mainDT.patient_ID == patient]    # Group by patient_ID

            if np.shape(patientDT)[0] > 1:                  # Only consider patient with more than 1 colonoscopy
                rowIndex = 0
                while rowIndex < (len(patientDT)-1):            #  ّFor each colonoscopy of a given patient

                    patientDT.sort_values(['year', 'month'], ascending=[True, True], inplace=True)
                    selectedRows = self.get2rows(patientDT,rowIndex)
                    rowIndex = rowIndex + 1

                    res = self.isTheTimeDifferenceMoreThan6Month(selectedRows)
                    if res:
                        aggregatedRow = self.sumPolyps(selectedRows)
                        self.mainDT = self.mainDT[~self.mainDT.id.isin(selectedRows.id.tolist())]
                        self.mainDT = self.mainDT.append(aggregatedRow, ignore_index=True).reindex()
                        rowIndex = 0                                            #  َAfter removing 2 rows and adding new one, start again

                    patientDT = self.mainDT[self.mainDT.patient_ID == patient]  # Again get all colonscopy of a given patient

                print("------------------------------")

        self.saveOutPut()


    def get2rows(self, patientDT,index):
        return patientDT.iloc[index:(index+2), :]

    def isTheTimeDifferenceMoreThan6Month(self,dt):
        dt = dt.reset_index(drop=True)
        firstVisitDate =  dt.loc[0, "year"] * 12 + dt.loc[0, "month"]
        secondVisitDate = dt.loc[1,"year"]  * 12 + dt.loc[1,"month"]
        timeDifference = secondVisitDate - firstVisitDate
        res = timeDifference <= 6
        return res

    def sumPolyps(self,dt):
        dt = dt.reset_index(drop=True)
        dt.loc[0,"Nr_Small"]  = dt.loc[0,"Nr_Small"]+dt.loc[1,"Nr_Small"]
        dt.loc[0,"Nr_Medium"] = dt.loc[0,"Nr_Medium"]+dt.loc[1,"Nr_Medium"]
        dt.loc[0,"Nr_Large"]  = dt.loc[0,"Nr_Large"]+dt.loc[1,"Nr_Large"]
        dt.loc[0, "State"] = str(dt.loc[0,"Nr_Small"]) + "_" + str(dt.loc[0, "Nr_Medium"]) + "_" + str(dt.loc[1, "Nr_Large"])
        return dt.loc[0,:]

    def saveOutPut(self):
        self.mainDT = self.mainDT.groupby(by=['patient_ID'], as_index=False).apply(lambda x: x.reset_index(drop = True))
        self.mainDT.sort_values(['patient_ID','year', 'month'], ascending=[True,True, True], inplace=True)
        self.mainDT = self.mainDT.drop(['id'], axis=1)
        self.mainDT.to_csv("./../datasets/Final_CleanedDT1.csv", sep=',', encoding='utf-8', index=False)