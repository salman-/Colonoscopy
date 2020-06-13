from PolypExtractor                   import PolypExtractor
from PolypSizeCleaner                 import PolypSizeCleaner
from PolypSizeFixMultipleCategory     import PolypSizeFixMultipleCategory
from SelectValidData                  import SelectValidData
from FilterUnusefullData              import FilterUnusefullData
import pandas as pd
import numpy as np

originalDTPath = "./../datasets/Original DT/sample.csv"
cleanedDTPath  = "./../datasets/Capsules/cleanedDataSet.csv"

FilterUnusefullData(originalDTPath)

PolypExtractor(cleanedDTPath)               # Set dataset polyp based

SelectValidData(cleanedDTPath)               # Create a dataset which data which has no NA in size and polypNo

PolypSizeFixMultipleCategory(cleanedDTPath)  # Just to TEST. This line must not print anything.

PolypSizeCleaner(cleanedDTPath)   #-----------

