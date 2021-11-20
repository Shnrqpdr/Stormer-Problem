from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

df_q3=pd.read_csv("dadosProton1.dat", header = 0, sep='\s+')
df_q4=pd.read_csv("dadosProton2.dat", header = 0, sep='\s+')
df_q5=pd.read_csv("dadosProton3.dat", header = 0, sep='\s+')


fig = plt.figure()

#print(np.asarray(x).shape)
ax = fig.add_subplot(projection='3d')

ax.scatter(df_q3['x'], df_q3['y'], df_q3['z'], s=1)
ax.scatter(df_q4['x'], df_q4['y'], df_q4['z'], s=1, color='mediumseagreen')

N=200
stride=2
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, color='grey')

ax.set_zlim(-3.25, 3.25)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
plt.title("Prótons no cinturão de radiação de Van Allen", fontdict=None,)
plt.savefig('ProtonsVanAllen3D.pdf')
plt.show()

