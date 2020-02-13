import pandas as pd
import numpy as np
import json

class ObtainStateTransitions:

    def __init__(self,numberOfStates,dtPath):

        self.dtPath = dtPath
        self.mainDt = pd.read_csv(self.dtPath)
        self.stateList = []
        self.stateList  = self.generateStates(self.stateList,numberOfStates)
        self.transitionMatrix = self.createTransitionMatrix(self.stateList)
        self.patients = self.getUnqiuePatient(self.mainDt)
        self.obtainStateTransitionForEachPatient(self.mainDt, self.patients)
        self.writeToCSVFile(self.stateList,self.transitionMatrix)
        self.writeToJSONFile(json,self.stateList, self.transitionMatrix)
#-----------------------------------------------------------

    def generateStates(self, stateList, numberOfStates):

        for small in range(0, numberOfStates):    # in method1: numberOfStates=7
            for medium in range(0, numberOfStates):
                for large in range(0, numberOfStates):
                    if small + medium + large > (numberOfStates - 1):
                        break
                    else:
                        state = str(small) + "_" + str(medium) + "_" + str(large)
                        stateList.append(state)

        self.stateList.append('6_6_6')  # "6_6_6" is only used in the Method1
        self.stateList.append('9_9_9')  # "9_9_9" is only used in the Method1

        print("All Possible States Are: ")
        print(self.stateList)
        print("Number of states is: " + str(len(stateList)))
        return stateList


    def createTransitionMatrix(self,stateList):

        toState = {state: 0 for state in stateList}
        transitionMatrix = {state: toState.copy() for state in stateList} # matrix to keep state transitions
        return transitionMatrix

    def getUnqiuePatient(self,dt):

        patients = dt["patient_ID"].unique()
        print("Number of paitents: " + str(len(patients)))
        return patients

#-----------------------------------

    def updateStateTransitions(self, dataset):
        rowsNr = np.shape(dataset)[0]
        for i in list(range(0,rowsNr-1)):                      # Navigate throw DT
            fromState = dataset.iloc[i,8]                      # Column 8 is the "State" column in "paitent_State.csv"
            toState   = dataset.iloc[(i+1), 8]
            self.transitionMatrix[fromState][toState] = self.transitionMatrix[fromState][toState] + 1
            print("fromState is: "+str(fromState)+" toState is: "+str(toState))

    def obtainStateTransitionForEachPatient(self,dt,patients):

        for patient in patients:
            patientDT = dt[ dt.patient_ID == patient]
            if np.shape(patientDT)[0] > 1 :
                print(patientDT)
                patientDT.sort_values(['year', 'month'], ascending=[True, True],inplace=True)
                self.updateStateTransitions(patientDT)
                print("------------------------------")

#-------------------------------------------------------- Save transitionCounter into a .csv file

    def writeToCSVFile(self,stateList,transitionCounter):

        dt = pd.DataFrame(columns=stateList)
        dt.insert(0,"States",stateList)

        for fromState in stateList:
            for toState in stateList:
                dt.loc[dt["States"] == fromState,toState] = transitionCounter[fromState][toState]

        dt.to_csv("./Dataset/transitionCounter.csv", sep=',', encoding='utf-8', index=False)

#----------------------------------------------------- Save TransitionCounter into a .json file

    def writeToJSONFile(self,json,stateList,transitionCounter):

        json = json.dumps(transitionCounter)
        f = open("./Dataset/transitionCounter.json", "w")
        f.write(json)
        f.close()