import matplotlib.pyplot as plt

def plotFigure(x1, x2, y1, y2, xlabel, ylabel, title, name, param):
    
    fig = plt.figure(param)
    ax = fig.add_subplot(111)
    
    ax.set(ylim=(-150, 150))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.plot(x1, y1, '-', label=r'$\frac{1}{2 \sqrt{5}}log\left(\frac{2x - \sqrt{5} + 1}{2x + \sqrt{5} + 1}\right)$')
    ax.plot(x2, y2, '-', label=r'$\frac{1}{2 \sqrt{5}}log\left(\frac{2x - \sqrt{5} + 1}{2x + \sqrt{5} + 1}\right)$')
    
    # plt.xscale('log')
    # plt.yscale("log")
    
    plt.grid(linestyle='-', linewidth=0.7)
    # plt.legend(loc="upper right",ncol=3,fontsize='small')
    plt.title(title, fontdict=None)
    plt.savefig(name) 
    