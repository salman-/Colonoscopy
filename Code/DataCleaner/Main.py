from PolypExtractor   import PolypExtractor
from PolypSizeCleaner import PolypSizeCleaner
from RestructureLocation import RestructureLocation
from QuantificationOfNumberOfSessiles import QuantificationOfNumberOfSessiles
from DataSeperator    import DataSeperator
from DataMerger       import DataMerger
from ReduceStatesMethod1 import ReduceStatesMethod1


originalDTPath = "./../datasets/Original DT/sample.csv"
cleanedDTPath  = "./../datasets/Capsules/cleanedDataSet.csv"

PolypExtractor(originalDTPath)        # Set dataset polyp based

PolypSizeCleaner(cleanedDTPath)       # Validate the Size of column before obtain the final status
RestructureLocation(cleanedDTPath)    # Colon has 13 different location. Here we categorize them into Right and Left

QuantificationOfNumberOfSessiles(cleanedDTPath)


DataSeperator(cleanedDTPath)         # Seprate different capsules and save them in .csv files

DataMerger()                         # Merge the seperated capsules in order to obtain the patient status


inputDTPath  = "./../datasets/Final DT/MergedDT.csv"
outputDTPath = "./../datasets/Final_CleanedDT.csv"

rsm1 = ReduceStatesMethod1(inputDTPath)
rsm1.labelThePaitentsWithMoreThan6PolypsAs6_6_6()
rsm1.labelThePaitentsWithCancersAs9_9_9()
rsm1.output(outputDTPath)


















