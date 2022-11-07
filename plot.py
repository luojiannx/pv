import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys
a=pd.read_csv(sys.argv[1])
n=int(sys.argv[2])
b=a.iloc[0:365,6:102]
c=b.T
d=c.iloc[0:96,n:(n+1)]
d.plot()
plt.show()
