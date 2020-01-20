
from PolypExtractor   import PolypExtractor
from PolypSizeCleaner import PolypSizeCleaner
from RestructureLocation import RestructureLocation
from QuantificationOfNumberOfSessiles import QuantificationOfNumberOfSessiles
from dataSeperator    import DataSeperator
from dataMerger       import DataMerger

#originalDTPath = "./datasets/Original DT/complete-non-cleaned-DT.csv"
#originalDTPath = "./datasets/Original DT/sample.csv"
originalDTPath = "./datasets/Original DT/Indianapolis-original.csv"
cleanedDTPath  = "./datasets/Capsules/cleanedDataSet.csv"

PolypExtractor(originalDTPath)        # Set dataset polyp based
PolypSizeCleaner(cleanedDTPath)       # Validate the Size of column before obtain the final status
RestructureLocation(cleanedDTPath)    # Colon has 13 different location. Here we categorize them into Right and Left

QuantificationOfNumberOfSessiles(cleanedDTPath)

DataSeperator(cleanedDTPath)         # Seprate different capsules and save them in .csv files

DataMerger()                         # Merge the seperated capsules in order to obtain the patient status
