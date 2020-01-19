import unittest
import numpy  as np
import pandas as pd

import os
os.chdir("..")

import sys
sys.path.append(os.path.abspath(os.curdir))

from PolypExtractor import PolypExtractor


class TestDataSetCleaner( unittest.TestCase ):


    def setUp(self):
        self.dt = PolypExtractor("../cleanedData/cleanedDataSet.csv")
    
    def test_isAllCellsNULL(self):
       
        res = self.dt.isAllCellsNULL(1,2,81,122)
        #print( "Result: " + str(res) )
        self.assertEqual(res,True)

    def test_getCapsulRange(self):
        
        res = self.dt.getCapsulRange(1)
        print("Capsul Begin: "+str(res[0])+" Capsul End: "+str(res[1]) )
        self.assertEqual(res[1]-res[0],8)

    def test_getCapsul(self):
        self.dt.getCapsul(1,40,81)