import pandas as pd
import numpy as np

'''

'''


dt = pd.read_csv(r'C:\Users\salma\Desktop\all\Ali-Dataset-PaitentStatistic\1.csv')
dt.head()

dt["PeriodBetween2Visits"] = (dt["year"].mul(12).add(dt["month"]).groupby(dt['patient_ID']).diff().fillna(0).astype(int))
dt["NumberOfVisits"] = dt.groupby(['patient_ID'])['patient_ID'].transform('size')
#dt.head()

#----------------------------------------------------------------------
dt = dt.groupby(['facility','patient_ID']).agg(
                 Min_PeriodBetween2Visits=('PeriodBetween2Visits','min'),
                 Max_PeriodBetween2Visits=('PeriodBetween2Visits','max'),
                 NumberOfVisits=('NumberOfVisits','first')).reset_index()
dt.head()


dt.to_csv("./report.csv", sep=',', encoding='utf-8', index=False)
