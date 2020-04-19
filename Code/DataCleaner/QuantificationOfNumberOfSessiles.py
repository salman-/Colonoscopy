import numpy as np
import pandas as pd
import math



class QuantificationOfNumberOfSessiles:

    def __init__(self,dataSetPath):

        self.cleanedDataSet = pd.read_csv(dataSetPath, error_bad_lines=False, index_col=False, dtype='unicode')
        self.cleanedDataSet.loc[:, 'Number of sessiles'] = self.replaceThreePlusWithOtherNumbers(self.cleanedDataSet)  # Replace all 3_ with a random value

        self.distributeTheNumberOfSessileIntoLocations()
        self.writeToFile()


    def replaceThreePlusWithOtherNumbers(self,data):

        allEvents = data.loc[:, 'Number of sessiles'].tolist()
        listOfUniqueNumberOfPolypsToBeReplaced = self.getListOfUniqueNumberOfPolypsToBeReplaced(data)
        probability = self.probabilityCalculator(listOfUniqueNumberOfPolypsToBeReplaced, data)
        for index, value in enumerate(allEvents):
            if value == '3+':
                rand = list(np.random.choice(listOfUniqueNumberOfPolypsToBeReplaced, size=1, p=probability))
                allEvents[index] = str(rand[0])

        print(allEvents)
        return allEvents

    # block 2
    ## counts this list  [3,4,5,...,10]   Then calculate each elemnt frequency

    def probabilityCalculator(self,listOfUniqueNumberOfPolypsToBeReplaced, data):
        count = []

        allEvents = data.loc[:, 'Number of sessiles'].dropna(axis = 0, how ='any').tolist()
        allEvents = list(filter(lambda x: x != '3+' and x != '0' and x != '1' and x != '2' and x != '3', allEvents))

        for i in listOfUniqueNumberOfPolypsToBeReplaced:
            print("Event: "+ str(i)+" Freq: "+str( allEvents.count(str(i))   ))
            count.append(allEvents.count(str(i)))

        prob = list(map(lambda x: (x / (len(allEvents))), count))

        return prob

    # Block 3
    ## creates a list of all number of polyps in the data set and bring back an slice of that list of

    def getListOfUniqueNumberOfPolypsToBeReplaced(self,data):
        allEvents = data.loc[:, 'Number of sessiles'].dropna(axis = 0, how ='any')
        uniqEvents = allEvents.unique().tolist()

        uniqEvents.remove('3+')

        uniqEvents = [int(i) for i in uniqEvents]
        uniqEvents.sort()
        sliced_part = uniqEvents[3:]
        return sliced_part


    def distributeTheNumberOfSessileIntoLocations(self):

        self.cleanedDataSet.fillna(0, inplace=True)
        self.cleanedDataSet['Right '] = self.cleanedDataSet['Right '].astype(float)
        self.cleanedDataSet['Left'] = self.cleanedDataSet['Left'].astype(float)
        self.cleanedDataSet['Number of sessiles'] = self.cleanedDataSet['Number of sessiles'].astype(float)

        rightLocationProbability = (self.cleanedDataSet["Right "] / (self.cleanedDataSet["Right "] + self.cleanedDataSet["Left"])).fillna(0)
        self.cleanedDataSet["Right "] = np.random.binomial(self.cleanedDataSet["Number of sessiles"], rightLocationProbability )

        self.cleanedDataSet["Left"] = self.cleanedDataSet["Number of sessiles"] - self.cleanedDataSet["Right "]

    def writeToFile(self):
        self.cleanedDataSet.to_csv("./../datasets/Capsules/cleanedDataSet.csv", sep=',', encoding='utf-8', index=False)
