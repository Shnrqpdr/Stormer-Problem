from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

fileProton1=pd.read_csv("dadosProton3D_1.dat", header = 0, sep='\s+')
fileProton2=pd.read_csv("dadosProton3D_2.dat", header = 0, sep='\s+')
fileProton3=pd.read_csv("dadosProton3D_3.dat", header = 0, sep='\s+')

label_1='Proton 1'
label_2='Proton 2'
label_3='Proton 3'

fig = plt.figure()

ax = fig.add_subplot(projection='3d')
ax.plot(fileProton1['x'], fileProton1['y'], fileProton1['z'], '-', label = label_1)
ax.plot(fileProton2['x'], fileProton2['y'], fileProton2['z'], '-', label = label_2, color='mediumseagreen')
ax.plot(fileProton3['x'], fileProton3['y'], fileProton3['z'], '-', label = label_3)

# ESFERA
N=200
stride=2
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, color='grey')
#

ax.set_xlim(-6.25, 6.25)
ax.set_ylim(-6.25, 6.25)
ax.set_zlim(-3.25, 3.25)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
plt.title("Prótons no cinturão de radiação de Van Allen", fontdict=None,)
plt.legend(loc="upper right",fontsize='small')
plt.savefig('ProtonsVanAllen3D4.png')
plt.show()

