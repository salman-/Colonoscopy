
import numpy as np
import pandas as pd

class StatisticRecorder:
    
    def __init__(self):
        
        self.itterationsNo = 1
        self.elapsedTime   = [1] 
        
        self.results = pd.DataFrame( columns= ["PatientsNo","VisitNo","Threshold","StateNo",
                                     "missedPercentage","IterationNo","Time","IsConverged"] )
        
       
        
#----------------------------------------------

    def getAllValuesInDataframe(self,dt):
        states = dt.iloc[:, 0]  # Start by the first column and append the other columns to it
        columnNumber = len(dt.columns.tolist())

        for i in range(1, columnNumber):
            states = states.append(dt.iloc[:, i])

        res = states.values
        return res

    def isPSIsConverged(self,psiNew,psiLast,threshold):

        diff = abs(psiNew - psiLast )
        allElements = self.getAllValuesInDataframe(diff)
        res = np.sum(allElements > threshold)

        return (res == 0)
        
    def recordElapsedTime(self, time ):
        self.elapsedTime.append(time)
    

    def increaseCounter(self,psiNew,psiLast, elapsedTime,threshold):
        
        dtPsiNew = pd.DataFrame(psiNew)
        dtPsiNew.to_csv("psiNew.csv", encoding='utf-8', index=False)
        
        self.recordElapsedTime(elapsedTime)
        self.itterationsNo = self.itterationsNo + 1

        print("Iteration: " + str(self.itterationsNo))

        diff = abs(psiNew - psiLast )
        allElements = self.getAllValuesInDataframe(diff)

        mean = np.mean(allElements)
        print("Avg different value: "+ str(np.round( mean ,4)))

        absDiff = np.max(allElements)
        print("ABS Max Diff: "+ str(np.round( absDiff ,4)))

        number_of_Cells = np.round(np.sum(allElements > threshold) / len(allElements),2)
        print("Percentage of cells which are not Converged:  " + str(number_of_Cells))

        print("Elapsed time:" , str(elapsedTime) )

        print("________________________________________________________________________")
        
    def appendResults(self, patientsNo, VisitNo, Threshold, stateNo, missedPercentage, IterationNo,  averageTimePerIteration, IsConverged):
        
        record ={
                    "PatientsNo": patientsNo,
                    "VisitNo"   : VisitNo,
                    "Threshold" : Threshold,
                    "stateNo"   : stateNo,
                    "missedPercentage": missedPercentage,
                    "IterationNo"     : IterationNo,
                    "averageTimePerIteration" : averageTimePerIteration,
                    "IsConverged"             : IsConverged
                }
        
        self.results = self.results.append(record, ignore_index=True)
        self.results.to_csv("result.csv", sep=',', encoding='utf-8', index=False)
