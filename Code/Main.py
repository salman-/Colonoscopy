from ReduceStatesMethod1 import ReduceStatesMethod1
from ObtainStateTransitions import ObtainStateTransitions
from ReduceStatesMethod2 import ReduceStatesMethod2

#rsm1 = ReduceStatesMethod1()
#rsm1.reduce_state_method1()
#rsm1.output()


#rsm2 = ReduceStatesMethod2()
#rsm2.output()

dtPath = "./../Dataset/paitent_State_Reduced_State_By_Method2.csv"

ost = ObtainStateTransitions(4,dtPath)

