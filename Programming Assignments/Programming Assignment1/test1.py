#
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

theta = np.arange(-100,100,0.1)
rho = -theta/(1+theta**2)
plt.figure()
plt.plot(theta,rho)
plt.show()