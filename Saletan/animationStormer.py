import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import FuncAnimation
from matplotlib import rc

plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'

def Animate(x, y):

    fig,ax = plt.subplots(1, 1, 1, projection="3d")

    ax.set(xlim=(-200, 200), ylim=(-200, 400))

    # plt.style.use('dark_background')
    plt.title(r'Animação: Problema de Stormer para $\gamma_{1} = \frac{1}{2}$')
    # plt.grid(linestyle='-', linewidth=0.7)
    
    ax.set_xlabel("x",fontsize=14)
    ax.set_ylabel("y",fontsize=14)
    ax.set_zlabel("z",fontsize=14)
 
    plt.close()
    
    def init():
        return 10

    y_copy = y[:].copy()
    x_copy = x[:].copy()
    bolinha=[ax.scatter(x_copy[0], y_copy[0], 0, color="tab:blue",marker="o",s=100, label="Particle")]
    
    def anim(i):
        bolinha[0].remove()
        traco=ax.plot(x_copy[:i],y_copy[:i],color="tab:blue")
        bolinha[0]=ax.scatter(x_copy[i],y_copy[i], 0, color="tab:orange",marker="o",s=50,label="Particle")
        return traco, bolinha
    
    anim = FuncAnimation(fig, anim, init_func=init, interval=10, blit=False, save_count=4000) 
    anim.save('stormer_animacao2.mp4', fps=30, extra_args=['-vcodec', 'libx264'])