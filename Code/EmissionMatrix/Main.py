from EmissionMatrix import EmissionMatrix
import pandas as pd

dtPath = "./../datasets/historyMatrixOfPaitentsWithMoreThan1Colnoscopy.csv"

#m = EmissionMatrix(7,dtPath)    # first parameter is the maximum number of polypes. eg. small+medium+large < 7
m = EmissionMatrix(-1, dtPath)   # -1 means we are going to extract the list of polyps from Dataset rather than generate them with maximum number of polyps