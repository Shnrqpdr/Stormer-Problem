from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

fileProton=pd.read_csv("data/sphere.dat", header = 0, sep='\s+')

label_1='Particle path'

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(projection='3d')
ax.set_aspect('auto')
ax.plot(fileProton['x'], fileProton['y'], fileProton['z'], '-', label = label_1, linewidth=2, color='blue')

# ESFERA (R=10 como no artigo)
N = 200
R = 10.0
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = R * np.outer(np.cos(u), np.sin(v))
y = R * np.outer(np.sin(u), np.sin(v))
z = R * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, edgecolor='#a0a0a0', lw=0.2, rstride=4, cstride=4, color='#e0e0e0', alpha=0.2)

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
# Câmera: ângulo (elev, azim) e distância (maior = mais longe)
ax.view_init(elev=22, azim=-48)
ax.dist = 13  # padrão ~10; aumentar deixa a câmera mais longe

plt.title("Particle constraint in a sphere", fontdict=None,)
plt.legend(loc="upper right", fontsize='small')

# Nome do arquivo: via linha de comando ou padrão
outfile = argv[1] if len(argv) > 1 else 'sphere_plot.png'
plt.savefig(outfile, dpi=300)
# plt.show()