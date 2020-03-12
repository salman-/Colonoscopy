import unittest
import numpy as np
import os
import sys  

os.chdir('..')
parentDirectory = os.path.abspath(os.curdir)
sys.path.append(parentDirectory)

from DataSet import DataSet

class TestDataSet(unittest.TestCase):
    
    def setUp(self):
        self.dt = DataSet(3, 0.6, 80, 20)
        
#------------------------------------------------------------------------------
    
    def test_getMissingIndex(self):
        
        NumberOfMissedIndecies = len(self.dt.getMissingIndex())
        self.assertEqual(NumberOfMissedIndecies ,
                         self.dt.nCol * self.dt.nRow * self.dt.missPercentage )
        # Test2: There should not be any index biger than Maximum Matrix index
        # Test3: There should not be any index less than 0
             
#------------------------------------------------------------------------------
            
    def test_getOriginalPsi(self):
        
        psi = self.dt.getOriginalPsi()
     
        psiNrow=np.shape(psi)[0]
        self.assertEqual(psiNrow,self.dt.stateSize)
        
        psiNcol=np.shape(psi)[1]
        self.assertEqual(psiNcol,self.dt.stateSize)
        
        sumOfPsiColumns = np.sum(psi[1,:])
        self.assertAlmostEqual( sumOfPsiColumns ,1.0) 
        
#------------------------------------------------------------------------------
    
    def test_createDataSetWithNULLs(self):
        
        self.assertEqual(self.dt.nRow,80)
        self.assertEqual(self.dt.nCol,20)

#------------------------------------------------------------------------------



  #  def test_writeFirstColumn(self):     
                                     # Test1: First column should NOT be -1
                                     # Test2: First column should be filled with valid states
                                     # Test3: Other columns should be -1
                                     

#------------------------------------------------------------------------------
            
  #  def test_writeAllColumns(self):
        
                                     # Test1: It must fill column 2 and next columns
                                     # Test2: The enteries should be filled with valid state
                                     # Test3: The filled value should be based on PREVIOUS STATE 

                                     
#------------------------------------------------------------------------------
  #  def test_omitEnteries(self):
                                   # Test1: All the omited elements must be -1
                                   # Test2: Returned matrix must have the same Nrow as original matrix
                                   # Test3: Returned matrix must have the same Ncol as original matrix

#------------------------------------------------------------------------------

    def test_randomlyChooseState(self):
        
        randomState = self.dt.randomlyChooseState([.1,.3,.6])
        #print("Random state: "+str(randomState))
                                   # Test1: Random state should be a valid state between 0 and stateSize-1
        
        
                                   # Test2: The state with higher weight must  be more in 10 calls 
        counter0 = 0
        counter1 = 0
        counter2 = 0
        for i in range(100000):
            if self.dt.randomlyChooseState([.1,.3,.6]) == 0:
                counter0 = counter0+1
            elif self.dt.randomlyChooseState([.1,.3,.6]) == 1:
                counter1 = counter1 +1
            else:
                counter2 = counter2 + 1 
                
        percent0 = round( counter0 / 100000, 1)
        percent1 = round( counter1 / 100000, 1)
        percent2 = round( counter2 / 100000, 1)
        
        print("Percent0:   " + str(percent0)+" Percent1:  " +str(percent1)+ "  Percent2:  " +str(percent2)) 
        self.assertAlmostEqual(percent0,.1)                        
        self.assertAlmostEqual(percent1,.3)
        self.assertAlmostEqual(percent2,.6)