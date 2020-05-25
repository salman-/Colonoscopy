from Stat import Stat


inputDTPath  = "./../datasets/Final_CleanedDT.csv"
outputDTPath = "./../datasets/StatDT.csv"
stat = Stat(inputDTPath,outputDTPath)

stat.getSizeDistribution("Nr_Sum")      # Get distribution of small polyps
stat.getSizeDistribution("Nr_Small")    # Get distribution of small polyps
stat.getSizeDistribution("Nr_Medium")   # Get distribution of medium polyps
stat.getSizeDistribution("Nr_Large")    # Get distribution of large polyps

inputDTPath  = "./../datasets/Final DT/MergedDT.csv"
#stat.getLocationDistribution(inputDTPath)
#stat.getSizeLocationDistribution(inputDTPath)