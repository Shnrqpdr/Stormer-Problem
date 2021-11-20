import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation
from matplotlib import rc
import numpy as np
import pandas as pd

#plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe' PRO WINDOWS


df_q3=pd.read_csv("dadosProton1.dat", header = 0, sep='\s+')
df_q4=pd.read_csv("dadosProton2.dat", header = 0, sep='\s+')

x1 = df_q3['x']
y1 = df_q3['y']
z1 = df_q3['z']

x2 = df_q4['x']
y2 = df_q4['y']
z2 = df_q4['z']

fig = plt.figure(figsize=(12,12))

ax = fig.add_subplot(projection='3d')

ax.set_xlim(-5.0, 5.0)
ax.set_ylim(-5.0, 5.0)
ax.set_zlim(-3.25, 3.25)

N=200
stride=2
u = np.linspace(0, 2 * np.pi, N)
v = np.linspace(0, np.pi, N)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, color='grey')


    
ax.set_xlabel("x",fontsize=14)
ax.set_ylabel("y",fontsize=14)
ax.set_zlabel("z",fontsize=14)
#plt.style.use('dark_background')
plt.title(r'Prótons no cinturão de radiação de Van Allen')

plt.close()
    
def init():
    return 5000

x1_copy = x1[:].copy()
y1_copy = y1[:].copy()
z1_copy = z1[:].copy()

x2_copy = x2[:].copy()
y2_copy = y2[:].copy()
z2_copy = z2[:].copy()

bolinha1=[ax.scatter(x1_copy[0], y1_copy[0], z1_copy[0], color="tab:blue",marker="o",s=5, label="Particle")]
bolinha2=[ax.scatter(x2_copy[0], y2_copy[0], z2_copy[0], color="mediumseagreen",marker="o",s=5, label="Particle")]
    
def anim(i):
    bolinha1[0].remove()
    bolinha2[0].remove()
    traco1=ax.plot(x1_copy[:i],y1_copy[:i], z1_copy[:i], color="tab:blue")
    traco2=ax.plot(x2_copy[:i],y2_copy[:i], z2_copy[:i], color="mediumseagreen")
    bolinha1[0]=ax.scatter(x1_copy[i],y1_copy[i], z1_copy[i], color="tab:orange",marker="o",s=5, label="Particle")
    bolinha2[0]=ax.scatter(x2_copy[i],y2_copy[i], z2_copy[i], color="tab:red",marker="o",s=5, label="Particle")
    return traco1, traco2, bolinha1, bolinha2
    
anim = FuncAnimation(fig, anim, 2000, interval=100, blit=False)
anim.save('stormer3D_2.mp4', fps=30, extra_args=['-vcodec', 'libx264'])