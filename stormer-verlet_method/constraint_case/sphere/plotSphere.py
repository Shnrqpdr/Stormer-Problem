from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

fileProton=pd.read_csv("data/sphere.dat", header = 0, sep='\s+')

label_1='Particle'

fig = plt.figure()

ax = fig.add_subplot(projection='3d')
ax.plot(fileProton['x'], fileProton['y'], fileProton['z'], '-', label = label_1, linewidth=2, color='blue')

# ESFERA
N=200
stride=2
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = 10.0*np.outer(np.cos(u), np.sin(v))
y = 10.0*np.outer(np.sin(u), np.sin(v))
z = 10.0*np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, color='grey', alpha = 0.2)
#

ax.set_xlim(-11.0, 11.0)
ax.set_ylim(-11.0, 11.0)
ax.set_zlim(-11.5, 11.5)

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
plt.title("Particle constraint in a sphere", fontdict=None,)
plt.legend(loc="upper right",fontsize='small')
#plt.savefig('SpherePlot.pdf')
plt.show()