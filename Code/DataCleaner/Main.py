from PolypExtractor                   import PolypExtractor
from PolypSizeCleaner                 import PolypSizeCleaner
from RestructureLocation              import RestructureLocation
from QuantificationOfNumberOfSessiles import QuantificationOfNumberOfSessiles
from DataSeperator                    import DataSeperator
from DataMerger                       import DataMerger
from ReduceStatesMethod1              import ReduceStatesMethod1
from CombineRowsWithLessThan6MonthGap import CombineRowsWithLessThan6MonthGap
from PolypSizeFixMultipleCategory     import PolypSizeFixMultipleCategory
from SelectValidData                  import SelectValidData

originalDTPath = "./../datasets/Original DT/sample.csv"
cleanedDTPath  = "./../datasets/Capsules/cleanedDataSet.csv"

PolypExtractor(originalDTPath)        # Set dataset polyp based

SelectValidData(cleanedDTPath)        # Create a dataset which data which has no NA in size and polypNo

#PolypSizeFixMultipleCategory(cleanedDTPath)

"""

QuantificationOfNumberOfSessiles(cleanedDTPath)

PolypSizeCleaner(cleanedDTPath)       # Validate the Size of column before obtain the final status


DataSeperator(cleanedDTPath)         # Seprate different capsules and save them in .csv files

DataMerger()                         # Merge the seperated capsules in order to obtain the patient status


#----------------------------------------

inputDTPath  = "./../datasets/Final DT/MergedDT.csv"
outputDTPath = "./../datasets/Final_CleanedDT.csv"

rsm1 = ReduceStatesMethod1(inputDTPath)   #Obtain the result of each colonscopy as an state
#rsm1.labelThePaitentsWithMoreThan6PolypsAs6_6_6()
rsm1.labelThePaitentsWithCancersAs9_9_9()
rsm1.output(outputDTPath)

#----------------------------------------

inputDTPath  = "./../datasets/Final_CleanedDT.csv"
arwlt6mg = CombineRowsWithLessThan6MonthGap(inputDTPath)

#----------------------------------------
"""