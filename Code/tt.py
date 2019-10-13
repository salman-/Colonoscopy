import numpy as np
import pandas as pd


dict = {"State":np.random.randint(low=1,high=20,size=30)}
dt = pd.DataFrame(data=dict)

options = np.random.choice([True,False],30)

print(options)

print(dt[options].State)

