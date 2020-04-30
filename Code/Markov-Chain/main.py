import numpy        as np

import time
import statistics

from DataSet           import DataSet
from Psi               import Psi
from FillNAs           import FillNAs
from StatisticRecorder import StatisticRecorder
from ColonoscopyDataSet import ColonoscopyDataSet

#------------------------------------------------------------

#dt = DataSet(40, 0.4, 4000, 20)                   # stateSize, missedPercentage, nRow, nCol
dt = ColonoscopyDataSet()
#psiLast = dt.firstPsi


psiLast = Psi(dt.matrix, dt.stateSize)
psiLast = psiLast.matrix

#------------------------------------------------------------

fillNa = FillNAs(dt)
dt.matrix = fillNa.fillNA_First_Iteration( dt,psiLast )
"""
psi       = Psi(dt.matrix, dt.stateSize)                         # Get a new Psi
psiNew    = psi.matrix

#------------------------------------------------------------

sr = StatisticRecorder()

while(not(fillNa.isPSIsConverged(psiNew,psiLast,0.02))): #continue until convergance
    
    start_time = time.time()
    
    dt.matrix = fillNa.fillNA_After_First_Iteration(dt,psiNew )

    
    psiLast = psiNew                                  
    psi     = Psi(dt.matrix, dt.stateSize)                         
    psiNew  = psi.matrix

    sr.increaseCounter(psiNew,psiLast,np.round((time.time() - start_time),3),0.02)
    

print("##--------------------------------------------------------------------------------##")    
 
#print(" Last psi is: ")
#print(psiNew)      
#print( "Is the LAST Psi and the ORIGINAL Psi converged? "+ str(fillNa.isPSIsConverged(psiNew,dt.firstPsi,0.4)))

print( "Average time spent on each iteration "+ str(statistics.mean(sr.elapsedTime)))

"""