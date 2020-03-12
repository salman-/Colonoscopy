import unittest
import numpy as np
import os
import sys  

os.chdir('..')
parentDirectory = os.path.abspath(os.curdir)
sys.path.append(parentDirectory)

from Psi import Psi
from   DataSet import DataSet



class TestPsi(unittest.TestCase):
    
    def setUp(self):
        
        self.matrix= [[-1, -1,  3,  3, -1],
                      [ 1,  2, -1,  4,  1],
                      [ 3,  4, -1, -1,  4],
                      [-1,  3,  3,  3,  3],
                      [-1, -1,  2, -1,  3]]
        self.psi = Psi(self.matrix,5)
        
#---------------------------------------------------
    
   # def test_obtainPsi(self):
                                   # Test1: Number of columns of Psi is equal to Number of States
                                   # Test2: Number of rows of Psi is equal to Number of States
                                   # Test3: Sum of a row in Psi is almost equal to 1.0
                                   
        
        
        
#------------------------------------------------------        
        
    def test_stateChangeCounter(self):
        
        actualResult = self.psi.stateChangeCounter(self.matrix,3,3)
        self.assertEqual(4,actualResult)
        actualResult = self.psi.stateChangeCounter(self.matrix,1,2)
        self.assertEqual(1,actualResult)
        
#---------------------------------------------------     
        
    def test_createStateChangeMatrix(self):
        
        res = self.psi.createStateChangeMatrix(self.matrix,5)
        expectedAnswer = np.array([[0, 0, 0, 0, 0],
                                   [0, 0, 1, 0, 0],
                                   [0, 0, 0, 0, 0],
                                   [0, 0, 0, 4, 1],
                                   [0, 1, 0, 0, 0]])
        self.assertEqual((expectedAnswer == res).all(),True)
        