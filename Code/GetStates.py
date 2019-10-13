import pandas as pd

dtPath = "./../Dataset/cleanedData.csv"
mainDt = pd.read_csv(dtPath)

mainDt = mainDt[["facility","patient_ID","year","month","Nr_Small","Nr_Medium","Nr_Large"]]
mainDt.fillna(0,inplace=True)
dt = mainDt.iloc[:,1:7].astype(int).astype(str)
mainDt["State"] = dt["Nr_Small"]+"_"+dt["Nr_Medium"]+"_"+dt["Nr_Large"]     # Add State column

recordsWith6PolypsOrMore = list(state > 6 for state in [sum(map(float, s.split('_'))) for s in mainDt.State])
mainDt.loc[recordsWith6PolypsOrMore,["State"]] = '666'

mainDt.to_csv("./../Dataset/paitent_State.csv", sep=',', encoding='utf-8', index=False)

