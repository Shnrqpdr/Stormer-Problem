import matplotlib.pyplot as plt
import pandas as pd

fig_1 = plt.figure(1)

ax1=fig_1.add_subplot(111)

contador = 80

while(contador <= 85):
    fileProton=pd.read_csv(f'phaseSpaceProton{contador}.dat', header = 0, sep='\s+')
    label = 'Proton'
    ax1.plot(fileProton['rho'],fileProton['drho'], '-', label=label, linewidth = 0.4)
    contador = contador+1


#ax1.set(xlim=(2, 4)) # se for plotar com 2 protons, retirar essa linha
ax1.set(ylim=(-100, 100)) # se for plotar com 2 protons, retirar essa lin
plt.grid(linestyle='-', linewidth=0.7)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$\dfrac{d\rho}{dt}$')


plt.title("Mapas de Poincaré associados à constante de movimento", fontdict=None,)
#plt.legend(loc="upper right",ncol=3,fontsize='small')

plt.show()
plt.savefig('phaseSpace2.pdf')