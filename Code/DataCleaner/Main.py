from PolypExtractor                   import PolypExtractor
from PolypSizeCleaner                 import PolypSizeCleaner
from QuantificationOfNumberOfSessiles import QuantificationOfNumberOfSessiles
from DataSeperator                    import DataSeperator
from DataMerger                       import DataMerger
from ReduceStatesMethod1              import ReduceStatesMethod1
from CombineRowsWithLessThan6MonthGap import CombineRowsWithLessThan6MonthGap
from PolypSizeFixMultipleCategory     import PolypSizeFixMultipleCategory
from FilterInvalidData              import FilterInvalidData




originalDTPath = "./../datasets/Original DT/Detroit_150.csv"
cleanedDTPath  = "./../datasets/Capsules/cleanedDataSet.csv"

PolypExtractor(originalDTPath)        #Set dataset polyp based

FilterInvalidData(cleanedDTPath)  #Not needed

QuantificationOfNumberOfSessiles(cleanedDTPath)

PolypSizeFixMultipleCategory(cleanedDTPath)

PolypSizeCleaner(cleanedDTPath)       # Validate the Size of column before obtain the final status
"""
#DataMergerNoneAdvanced()
"""
DataMerger(0)                         # Merge the seperated capsules in order to obtain the patient status

#DataMerger(1)                        # MergedDT for ADVANCED DT
#DataMerger(2)                        #MergedDT for NON-ADVANCED

#"""
#----------------------------------------

inputDTPath  = "./../datasets/Final DT/MergedDT.csv"
outputDTPath = "./../datasets/Final_CleanedDT.csv"

rsm1 = ReduceStatesMethod1(inputDTPath)   #Obtain the result of each colonscopy as an state
#rsm1.labelThePaitentsWithMoreThan6PolypsAs6_6_6()
rsm1.labelThePaitentsWithCancersAs9_9_9()
rsm1.output(outputDTPath)

#----------------------------------------
"""
inputDTPath  = "./../datasets/Final_CleanedDT.csv"
arwlt6mg = CombineRowsWithLessThan6MonthGap(inputDTPath)

#----------------------------------------
"""