import numpy        as np
import pandas       as pd
import numpy.random as random

import time
import statistics

from DataSet import DataSet
from Psi     import Psi
from FillNAs import FillNAs

#-------------------------------------------


stateNo          = list(range(10,30,10))
patientsNo       = 1000
missedPercentage = 0.4
Threshold        = 0.05
VisitNo          = 20

for s in stateNo:
    
    print("stateNo: "+str(s)+" patientsNo: "+str(patientsNo))
    
    dt = DataSet(s, 0.4, patientsNo, 20)                   # stateSize, missedPercentage, nRow, nCol
    psiLast = dt.firstPsi
    
    psiLast = Psi(dt.matrix, dt.stateSize)
    psiLast = psiLast.matrix
    
    fillNa = FillNAs(dt)
    dt.matrix = fillNa.fillNA_First_Iteration( dt,psiLast )
    psi       = Psi(dt.matrix, dt.stateSize)                         # Get a new Psi
    psiNew    = psi.matrix

    while(not(fillNa.isPSIsConverged(psiNew,psiLast,Threshold))):
        start_time = time.time()
    
        dt.matrix = fillNa.fillNA_After_First_Iteration(dt,psiNew )
    
        psiLast = psiNew                                  
        psi     = Psi(dt.matrix, dt.stateSize)                         
        psiNew  = psi.matrix

        fillNa.increaseCounter(psiNew,psiLast,np.round((time.time() - start_time),3))
    
    print("##--------------------------------------------------------------------------------##")    
    
    print( "Is the LAST Psi and the ORIGINAL Psi converged? "+ str(fillNa.isPSIsConverged(psiNew,psiLast,Threshold)))

    print( "Average time spent on each iteration "+ str(statistics.mean(fillNa.elapsedTime)))
    
    print("##--------------------------------------------------------------------------------##") 
    
    patientsNo = patientsNo + 1000
    