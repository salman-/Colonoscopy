import numpy        as np
import time
import statistics

from Psi               import Psi
from FillNAs           import FillNAs
from StatisticRecorder import StatisticRecorder
from ColonoscopyDataSet import ColonoscopyDataSet

#------------------------------------------------------------
dtPath = './DataSets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv'
diffThershold = 0.2

dt = ColonoscopyDataSet(dtPath,7)

psiLast = Psi(dt.matrix,dt.stateList )
psiLast = psiLast.matrix

#------------------------------------------------------------

fillNa = FillNAs(dt, dt.stateList)
dt.matrix = fillNa.fillNA_First_Iteration( dt,psiLast )

psi       = Psi(dt.matrix, dt.stateList)                         # Get a new Psi
psiNew    = psi.matrix

sr = StatisticRecorder()


while (not ( sr.isPSIsConverged(psiNew, psiLast, diffThershold) )): #continue until convergance
    
    start_time = time.time()
    
    dt.matrix = fillNa.fillNA_After_First_Iteration(dt,psiNew )

    
    psiLast = psiNew                                  
    psi     = Psi(dt.matrix, dt.stateList)
    psiNew  = psi.matrix

    sr.increaseCounter(psiNew,psiLast,np.round((time.time() - start_time),3),diffThershold)
    

print("##--------------------------------------------------------------------------------##")    
""""""
""" 
print(" Last psi is: ")
print(psiNew)
#print( "Is the LAST Psi and the ORIGINAL Psi converged? "+ str(fillNa.isPSIsConverged(psiNew,dt.firstPsi,diffThershold)))

print( "Average time spent on each iteration "+ str(statistics.mean(sr.elapsedTime)))
"""