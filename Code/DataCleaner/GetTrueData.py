from PolypExtractor                   import PolypExtractor
from PolypSizeCleaner                 import PolypSizeCleaner
from PolypSizeFixMultipleCategory     import PolypSizeFixMultipleCategory
from SelectValidData                  import SelectValidData
import pandas as pd
import numpy as np

originalDTPath = "./../datasets/Original DT/AnnArbor.csv"
cleanedDTPath  = "./../datasets/Capsules/cleanedDataSet.csv"

"""PolypExtractor(originalDTPath)        # Set dataset polyp based

SelectValidData(cleanedDTPath)        # Create a dataset which data which has no NA in size and polypNo

PolypSizeFixMultipleCategory(cleanedDTPath)  # Just to TEST. This line must not print anything. 

PolypSizeCleaner(cleanedDTPath)"""

dt = pd.read_csv(cleanedDTPath, error_bad_lines=False, index_col=False, dtype='unicode')
dt = dt[["Number of sessiles","Size of Sessile in Words"]]

dt = dt.groupby(["Number of sessiles","Size of Sessile in Words"]).size().reset_index(name='Count')

#print(dt)

def getRandomPolypNo(dt,size):
    dt = dt[dt["Size of Sessile in Words"]==size]
    sumCounts = np.sum(dt["Count"])
    dt["Count"] = dt["Count"]/sumCounts
    print(dt)
    noList = dt["Number of sessiles"].tolist()
    pro    = dt["Count"].tolist()
    randomPolypNo = np.random.choice(noList,1,p=pro)
    print("Generated Random PolypNo",randomPolypNo)

def getRandomPolypSize(dt,polypNo):
    dt = dt[dt["Number of sessiles"]==polypNo]
    sumCounts = np.sum(dt["Count"])
    dt["Count"] = dt["Count"]/sumCounts
    print(dt)
    noList = dt["Size of Sessile in Words"].tolist()
    pro    = dt["Count"].tolist()
    randomPolypNo = np.random.choice(noList,1,p=pro)
    print(randomPolypNo)

getRandomPolypNo(dt,"Small")
#getRandomPolypNo(dt,"Medium")
#getRandomPolypNo(dt,"Large")

#getRandomPolypSize(dt,"1")