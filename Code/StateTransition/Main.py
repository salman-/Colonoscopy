from ReduceStatesMethod1 import ReduceStatesMethod1
from ObtainStateTransitions import ObtainStateTransitions
from ReduceStatesMethod2 import ReduceStatesMethod2

inputDTPath  = "./Dataset/cleanedData.csv"
outputDTPath = "./Dataset/paitent_State_Reduced_State_By_Method1.csv"

rsm1 = ReduceStatesMethod1(inputDTPath)
rsm1.reduce_state_method1()
rsm1.output(outputDTPath)


#rsm2 = ReduceStatesMethod2()
#rsm2.output()

#dtPath = "./../Dataset/paitent_State_Reduced_State_By_Method2.csv"


#dtPath = "./../../Dataset/1.csv"
#dtPath = "./../../Dataset/2.csv"



#ost = ObtainStateTransitions(7,dtPath)

