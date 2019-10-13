import pandas as pd
import numpy as np
import json

#-----------------------------------------------------------------  Create States

stateList =[]
for small in range(0,7):
    for medium in range(0, 7):
        for large in range(0, 7):
            if small+medium+large > 6 :
                break
            else:
                state = str(small)+"_"+str(medium)+"_"+str(large)
                stateList.append(state)

stateList.append('666')

print("All Possible States Are: ")
print(stateList)

print("Number of states is: "+str(len(stateList)))
#-----------------------------------------------------------   Create matrix for keeping transitions

toState          = { state : 0  for state in stateList}
transitionCounter = { state : toState.copy()  for state in stateList}

#---------------------------------------------------------------
dtPath = "./../Dataset/paitent_State.csv"
mainDt = pd.read_csv(dtPath)

patients = mainDt["patient_ID"].unique()
print("Number of paitents: " + str(len(patients)))

def updateStateTransitions(dataset):
    rowsNr = np.shape(dataset)[0]
    for i in list(range(0,rowsNr-1)):
        fromState = dt.iloc[i,7]
        toState   = dt.iloc[(i+1), 7]
        transitionCounter[fromState][toState] = transitionCounter[fromState][toState] + 1
        print("fromState is: "+str(fromState)+" toState is: "+str(toState))

for patient in patients:

    dt = mainDt[ mainDt.patient_ID == patient]
    if np.shape(dt)[0] > 1 :
        print("Patient: "+str(patient))
        print(dt)
        dt.sort_values(['year', 'month'], ascending=[True, True],inplace=True)
        updateStateTransitions(dt)
        print("------------------------------")

#------------------------------------------------------- Save transitionCounter into a json file

json = json.dumps(transitionCounter)
f = open("./../Dataset/transitionCounter.json", "w")
f.write(json)
f.close()