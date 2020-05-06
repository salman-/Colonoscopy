
import numpy as np
import pandas as pd

class StatisticRecorder:
    
    def __init__(self):
        
        self.itterationsNo = 1
        self.elapsedTime   = [1] 
        
        self.results = pd.DataFrame( columns=         
                                    ["PatientsNo","VisitNo","Threshold","StateNo",
                                     "missedPercentage","IterationNo","Time","IsConverged"] )
        
       
        
#----------------------------------------------
        
    def recordElapsedTime(self, time ):
        self.elapsedTime.append(time)
    

    def increaseCounter(self,psiNew,psiLast, elapsedTime,threshold):
        
        dtPsiNew = pd.DataFrame(psiNew)
        dtPsiNew.to_csv("psiNew.csv", encoding='utf-8', index=False)
        
        self.recordElapsedTime(elapsedTime)
        self.itterationsNo = self.itterationsNo + 1

        print("Iteration: " + str(self.itterationsNo))

        diff = [abs(i) for i in (psiNew - psiLast).values.tolist()[0]]
        mean = np.mean(diff)
        print("Avg different value: "+ str(np.round( mean ,4)))

        absDiff = np.max(diff)
        print("ABS Max Diff: "+ str(np.round( absDiff ,4)))

        number_of_Cells = np.sum([elm >= threshold for elm in diff ])
        print("Num cells which are not Converged:  " + str(number_of_Cells))

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
