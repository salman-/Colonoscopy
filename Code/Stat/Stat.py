import pandas as pd
import numpy as np
import collections

class Stat:

    def __init__(self, dataSetPath,outputDTPath):

        self.outputDTPath = outputDTPath
        self.dt = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.polypDistribution()
        self.countStateFrquency(self.dt)

    def polypDistribution(self):
        dt = self.dt.groupby(['Nr_Small', 'Nr_Medium', 'Nr_Large'], as_index=False).count()
        dt.to_csv("./../datasets/PolypDist.csv")



    def countStateFrquency(self, dt):
        states = dt["State"].tolist()
        overallNumberOfStates = len(states)

        statDT = self.buildDataset(dt)
        for index, row in statDT.iterrows():
            statDT.loc[index,'Frequency'] = states.count(row['State'])
            statDT.loc[index, 'Probability'] = statDT.loc[index,'Frequency']/overallNumberOfStates


        statDT.sort_values('stateIndex')
        self.saveOutputAsCSV(statDT)

    def buildDataset(self,dt):
        maxPolyp = self.getMaximumNumberOfPolyps(dt)
        stateList = self.generateStates(maxPolyp)
        stateIndex = list(range(len(stateList)))
        dict = {    "stateIndex" : stateIndex,
                    "State": stateList   }

        stat = pd.DataFrame(data=dict)
        stat["Frequency"] = np.nan
        stat["Probability"] =np.nan
        return stat

    def getMaximumNumberOfPolyps(self,dt):
        sum = dt["Nr_Small"].astype(float) + dt["Nr_Medium"].astype(float) + dt["Nr_Large"].astype(float)
        sumOfAllPolyps = int(np.max((sum).tolist()))
        return sumOfAllPolyps

    def addSumOfPolypSizeToDT(self,dt):
        dt["Nr_Sum"] = dt["Nr_Small"].astype(float) + dt["Nr_Medium"].astype(float) + dt["Nr_Large"].astype(float)
        return dt

    def generateStates(self, numberOfStates):

        stateList = []
        for small in range(0, numberOfStates):    # in method1: numberOfStates=7
            for medium in range(0, numberOfStates):
                for large in range(0, numberOfStates):
                    if small + medium + large > (numberOfStates - 1):
                        break
                    else:
                        state = str(small) + "_" + str(medium) + "_" + str(large)
                        stateList.append(state)
        #print(stateList)
        return stateList

    def saveOutputAsCSV(self,dt):
        dt.to_csv(self.outputDTPath, sep=',', encoding='utf-8', index=False)

    def getSizeDistribution(self, columnName):

        dtPath = "./../datasets/Final_CleanedDT.csv"
        dt = pd.read_csv(dtPath, error_bad_lines=False, index_col=False, dtype='unicode')
        #print(dt[columnName])
        dt = self.addSumOfPolypSizeToDT(dt)
        values = dt.loc[:,columnName].value_counts()
        sum = np.sum(values)
        pro = (values/sum).to_frame()
        pro.columns = [ 'Probability']
        pro.index.names = ['NumberOfPolyps']

        pro["Count"] = dt.loc[:,columnName].value_counts()
        pro.to_csv("./../datasets/"+columnName+"Distribution.csv", sep=',', encoding='utf-8', index=True)



    def getLocationDistribution(self,dtPath):

        dt = pd.read_csv(dtPath)
        dt.fillna(0, inplace=True)
        dt = self.removeAllRowsWith0NumberOfPolyps(dt)

        polypSum = np.sum((dt["Left_x"] + dt["Right _x"] + dt["Left_y"] + dt["Right _y"] +dt["Left"] + dt["Right "]).tolist())
        print("polypSum: "+str(polypSum))
        proximalSum = np.sum((dt["Right _x"] + dt["Right _y"] + dt["Right "]).tolist()) #right == proximal
        proximalPro = proximalSum / polypSum
        print("proximalSum: " + str(proximalSum)+ "proximalPro: "+str(proximalPro))
        #left == = distal
        distalSum = np.sum((dt["Left_x"] + dt["Left_y"] + dt["Left"]).tolist())
        distalPro = distalSum / polypSum
        print("distalSum: " + str(distalSum)+ " distalPro: "+str(distalPro))


        dict = {
            "Location" :  ["proximal","distal" ],
            "Frequency" : [proximalPro,distalPro]
        }

        dt = pd.DataFrame(dict)
        print(dt)
        dt.to_csv("./../datasets/Location-Distribution.csv", sep=',', encoding='utf-8', index=True)


    def getSizeLocationDistribution(self,dtPath):

        dt = pd.read_csv(dtPath)
        dt.fillna(0, inplace=True)
        dt = self.removeAllRowsWith0NumberOfPolyps(dt)

        # left == = distal   right == proximal
        smallSum = np.sum((dt["Left_x"] + dt["Right _x"]).tolist())
        smallDistallPro = np.sum((dt["Left_x"]).tolist())/smallSum
        smallProximalPro = np.sum((dt["Right _x"]).tolist())/smallSum
        print("smallSum: "+str(smallSum)+ " smallDistallPro: "+str(smallDistallPro)+ " smallProximalPro: "+str(smallProximalPro))

        mediumSum = np.sum((dt["Left_y"] + dt["Right _y"]).tolist())
        mediumDistallPro = np.sum((dt["Left_y"]).tolist())/mediumSum
        mediumProximalPro = np.sum((dt["Right _y"]).tolist())/mediumSum
        print("polypSum: "+str(mediumSum)+ " mediumDistallPro: "+str(mediumDistallPro)+ " mediumProximalPro: "+str(mediumProximalPro))

        largeSum = np.sum((dt["Left"] + dt["Right "]).tolist())
        largeDistallPro = np.sum((dt["Left"]).tolist())/largeSum
        largeProximalPro = np.sum((dt["Right "]).tolist())/largeSum
        print("largeSum: "+str(largeSum)+" largeDistallPro: "+str(largeDistallPro)+ " largeProximalPro: "+str(largeProximalPro))

        dict = {
            "Size": ["Small","Medium","Large"],
            "Distal" :  [smallDistallPro,mediumDistallPro,largeDistallPro ],
            "Proximal" : [smallProximalPro,mediumProximalPro,largeProximalPro]
        }

        dt = pd.DataFrame(dict)
        print(dt)
        dt.to_csv("./../datasets/Size-Location-Distribution.csv", sep=',', encoding='utf-8', index=True)


    def removeAllRowsWith0NumberOfPolyps(self,dt):                                     # If noPolyp is 0 the number of polyps in right and left must be 0

        for index, row in dt.iterrows():
            #print(dt.loc[index,'Nr_Small'], dt.loc[index,'Left_x'], dt.loc[index,'Right _x'])
            if not (row['Left_x'] + row['Right _x']) == row['Nr_Small'] :

                dt.loc[index,'Left_x'] = 0
                dt.loc[index, 'Right _x'] = 0

                dt.loc[index, 'Left_y'] = 0
                dt.loc[index, 'Right _y'] = 0

                dt.loc[index, 'Left'] = 0
                dt.loc[index, 'Right'] = 0

        return dt

