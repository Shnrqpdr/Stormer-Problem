from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

fig = plt.figure(figsize=(12,12))

ax=fig.add_subplot()
#ax.set(xlim=(-5.1, 15)) # se for plotar com 2 protons, retirar essa linha

fileProton1=pd.read_csv("data-files/dadosProton1Animacao.dat", header = 0, sep='\s+')
fileProton2=pd.read_csv("data-files/dadosProton2Animacao.dat", header = 0, sep='\s+')
fileProton3=pd.read_csv("data-files/dadosProton3Animacao.dat", header = 0, sep='\s+')

label_1='Proton 1'
label_2='Proton 2'
label_3='Proton 3'

ax.plot(fileProton1['x'],fileProton1['y'], '-', label=label_1)
# ax.scatter(fileProton1['x'],fileProton1['y'],marker='8',linewidth=0.1,label=label_1,s=4)
# plt.plot(fileProton1['x'],fileProton1['y'],linestyle='-',linewidth=0.1)

ax.plot(fileProton2['x'],fileProton2['y'], '-', label=label_2, color='mediumseagreen')
# ax.scatter(fileProton2['x'],fileProton2['y'],marker='8',linewidth=0.1,label=label_2,s=4, color='mediumseagreen')
# plt.plot(fileProton2['x'],fileProton2['y'],linestyle='-',linewidth=0.3, color='mediumseagreen')

ax.plot(fileProton3['x'],fileProton3['y'], '-', label=label_3)
#ax.scatter(fileProton3['x'],fileProton3['y'],marker='8',linewidth=0.01,label=label_1,s=3)
# plt.plot(fileProton3['x'],fileProton3['y'],linestyle='-',linewidth=0.2)

a_circle = plt.Circle((0, 0), 1, color='gray')
ax.add_artist(a_circle)

plt.grid(linestyle='-', linewidth=0.7)
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.text(-0.40, -0.075, 'Earth', fontsize = 25) #-0.45 e -0.15 fontsize = 15 é o padrão para plotar com 2 protons

plt.title("Particles under magnetical force influence", fontdict=None,)
plt.legend(loc="upper right",ncol=3,fontsize='small')

plt.savefig('plot3DPlano.pdf')

fileProton1=pd.read_csv("data-files/dadosProton1Animacao.dat", header = 0, sep='\s+')
fileProton2=pd.read_csv("data-files/dadosProton2Animacao.dat", header = 0, sep='\s+')
fileProton3=pd.read_csv("data-files/dadosProton3Animacao.dat", header = 0, sep='\s+')

label_1='Proton 1'
label_2='Proton 2'
label_3='Proton 3'

fig = plt.figure(figsize=(12,12))

ax = fig.add_subplot(projection='3d', )
ax.plot(fileProton1['x'], fileProton1['y'], fileProton1['z'], '-', label = label_1, linewidth=0.65)
ax.plot(fileProton2['x'], fileProton2['y'], fileProton2['z'], '-', label = label_2, color='mediumseagreen', linewidth=0.65)
ax.plot(fileProton3['x'], fileProton3['y'], fileProton3['z'], '-', label = label_3, linewidth=0.65, color = '#ff7f0e')

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

#ax.view_init(18, -25)
#ax.set_xlim(-3.90, 3.90)
#ax.set_ylim(-3.90, 3.90)
ax.set_zlim(-3.00, 3.00)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
plt.title("Particles under magnetical force influence", fontdict=None,)
plt.legend(loc="upper right",fontsize='small')
plt.savefig('Protons3D-Article.pdf')

protons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

fig = plt.figure(figsize=(12,12))

ax = fig.add_subplot(projection='3d')

# ESFERA
N=200
stride=2
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, color='grey')

for proton in protons:
    fileProton = pd.read_csv(f'dadosProton{proton}Animacao.dat', header = 0, sep='\s+')

    labelProton = f'Proton {proton}'

    ax.plot(fileProton['x'], fileProton['y'], fileProton['z'], '-', label = labelProton, linewidth=1)

#ax.view_init(18, -25)
ax.set_xlim(-5.90, 5.90)
ax.set_ylim(-5.90, 5.90)
ax.set_zlim(-5.00, 5.00)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
plt.title("Particles under magnetical force influence", fontdict=None,)
plt.legend(loc="upper right",fontsize='small')
plt.savefig('Protons3D-Article-4.pdf')
plt.show()

protons = [1, 2, 3, 4, 5, 6]

fig = plt.figure(figsize=(12,12))

ax=fig.add_subplot()

for proton in protons:
    fileProton = pd.read_csv(f'dadosProton{proton}Animacao.dat', header = 0, sep='\s+')

    labelProton = f'Proton {proton}'

    ax.plot(fileProton['x'], fileProton['y'], '-', label = labelProton, linewidth=1)

a_circle = plt.Circle((0, 0), 1, color='gray')
ax.add_artist(a_circle)

plt.grid(linestyle='-', linewidth=0.7)
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.text(-0.40, -0.075, 'Earth', fontsize = 25) #-0.45 e -0.15 fontsize = 15 é o padrão para plotar com 2 protons

plt.title("Particles under magnetical force influence", fontdict=None,)
plt.legend(loc="upper right",ncol=3,fontsize='small')

# plt.savefig('plot3DPlano.pdf')