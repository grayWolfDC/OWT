# This program implements a clustering algorithm to sort out optical water types.
# It takes water types as inputs and applies (for now -- change later) a simple 
# k-means clustering algorithm. Future clustering implementations will include 
# fuzzy c-means.

import numpy as np
from mpl.toolikts.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
#ts = np.loadtxt('training.txt',delimiter=' ')
#band1 = ts[:,2] # 443nm
#band2 = ts[:,3] # 510nm
#band3 = ts[:,4] # 555nm
c = 'k'
m = 'o'
# First plot
ax.scatter


