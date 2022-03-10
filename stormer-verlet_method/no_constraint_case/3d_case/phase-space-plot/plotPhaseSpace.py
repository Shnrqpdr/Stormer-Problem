import matplotlib.pyplot as plt
import pandas as pd

fig_1 = plt.figure(1)

ax1=fig_1.add_subplot(111)

contador = 20

while(contador <= 23):
    fileProton=pd.read_csv(f'data-PlotPhaseSpace/phaseSpaceProton{contador}.dat', header = 0, sep='\s+')
    label = 'Proton'
    ax1.plot(fileProton['rho'],fileProton['drho'], '-', label=label, linewidth = 0.4)
    contador = contador+1


#ax1.set(xlim=(2, 4)) # se for plotar com 2 protons, retirar essa linha
ax1.set(ylim=(-100, 100)) # se for plotar com 2 protons, retirar essa lin
plt.grid(linestyle='-', linewidth=0.7)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$\dot{\rho}$')


plt.title("Espaço de Fase", fontdict=None,)
#plt.legend(loc="upper right",ncol=3,fontsize='small')

plt.show()
plt.savefig('phaseSpace20-23.pdf', dpi=600)