import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc

plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'


def Animate(x, y):

    fig,ax = plt.subplots(1, 1, figsize=(7,7))

    # plt.style.use('dark_background')
    plt.title('Animação: Problema de Stormer')
    plt.grid(linestyle='-', linewidth=0.7)
    plt.close()
    
    def init():
        return 100000

    y_copy = y[:].copy()
    x_copy = x[:].copy()
    bolinha=[ax.scatter(x_copy[0], y_copy[0], color="tab:blue",marker="o",s=100, label="Particle")]
    
    def anim(i):
        bolinha[0].remove()
        traco=ax.plot(x_copy[i],y_copy[i],color="tab:blue")
        bolinha[0]=ax.scatter(x_copy[i],y_copy[i],color="tab:blue",marker="o",s=100,label="Particle")
        
        return traco, bolinha
    
    anim = FuncAnimation(fig, anim, init_func=init, interval=50, blit=False) 
    anim.save('stormer_animacao.mp4', fps=30, extra_args=['-vcodec', 'libx264'])