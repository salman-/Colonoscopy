import numpy as np
from   InformationMatrix import InformationMatrix


class FillNAs:
    
    
    def __init__(self,dataSet):
        
        self.dataSet  = dataSet
        self.im       = InformationMatrix()
        
        
#--------------------------------------------------------------
      
        
    def fillNA_First_Iteration(self,dataSet, currentPsi):
   
        for elm in dataSet.missedIndices:
            row = int(elm / dataSet.nCol)
            col = int(elm % dataSet.nCol)
            previousState = dataSet.matrix[row,col-1]

            if col % (dataSet.nCol-1) == 0:                                     # missed index in First column
                
                dataSet.matrix[row,col] = np.random.choice(np.arange(dataSet.stateSize),1)[0]
            else:
                
                rowId = dataSet.randomlyChooseState(currentPsi[previousState,:])
                dataSet.matrix[row,col] = self.im.getRandomStateFromInformationMatrix(rowId)


        return dataSet.matrix

    
    def fillNA_After_First_Iteration(self, dataSet,currentPsi):
        
        previousState = 0
        nextState     = 0
        
        for elm in dataSet.missedIndices:                                        # Fill all the NAs
            row = int(elm / dataSet.nRow)
            col = int(elm % dataSet.nCol)
            if col % (dataSet.nCol-1) == 0:                                              # missed index in LAST column
                previousState = dataSet.matrix[row,col-1] 
                nextState = 1
            elif col % dataSet.nCol == 0 :                                                # missed index in First column
                nextState = dataSet.matrix[row,col+1]
                previousState = 1
            else:
                previousState = dataSet.matrix[row,col-1]                                # previous state in current data matrix
                nextState = dataSet.matrix[row,col+1]                                    # next PREDICTED state 

            chanceMatrix = self.getChanceMatrix(dataSet,previousState,nextState,currentPsi,elm)
            
            
            rowId  = dataSet.randomlyChooseState(chanceMatrix)
            dataSet.matrix[row,col] = self.im.getRandomStateFromInformationMatrix(rowId)


        return dataSet.matrix

    
    def getChanceMatrix(self,dataSet,previousState,nextState,psi, index):
        
        row = int(index / dataSet.nCol)
        col = int(index % dataSet.nCol)

        if col % (dataSet.nCol-1) == 0:                                          # missed index in last column
            mul = psi[previousState,:]
        elif col % dataSet.nCol   == 0:                                             # missed index in First column
            mul = psi[nextState,:]
        else:                                                            # minssed index is NoT in First ,or Last  Column
            mul = psi[previousState,:] * psi[:,nextState]


        weightedProb =  mul /  sum(mul) 
        return weightedProb


    def isPSIsConverged(self,psiNew,psiLast,threshold):
        
        return (abs(psiNew-psiLast)<=threshold).all() #return true if all the difference between all the enteries is less than 0.02

  

        