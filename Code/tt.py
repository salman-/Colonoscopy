import numpy as np
import pandas as pd

stateList = ['0_0_0', '0_0_1', '0_0_2', '0_0_3', '0_0_4']
toState          = { state : 0  for state in stateList}
transitionCounter = { state : toState.copy()  for state in stateList}

transitionCounter['0_0_0']['0_0_2'] = transitionCounter['0_0_0']['0_0_2'] + 1

print(transitionCounter)