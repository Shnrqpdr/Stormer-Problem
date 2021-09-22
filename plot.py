import matplotlib.pyplot as plt

def plotFigure(x, y, xlabel, ylabel, title, name, param):
    
    fig = plt.figure(param)
    ax = fig.add_subplot(111)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.plot(x, y, '-', label=r'$\frac{1}{2 \sqrt{5}}log\left(\frac{2x - \sqrt{5} + 1}{2x + \sqrt{5} + 1}\right)$')
    
    # plt.xscale('log')
    # plt.yscale("log")
    
    plt.grid(linestyle='-', linewidth=0.7)
    # plt.legend(loc="upper right",ncol=3,fontsize='small')
    plt.title(title, fontdict=None)
    plt.savefig(name) 
    