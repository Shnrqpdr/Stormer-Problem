import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure(1)
ax=fig.add_subplot(111)
#ax.set(xlim=(2.56, 2.995))
filePotential = pd.read_csv("potencialEfetivoP3.dat", header = 0, sep='\s+')

ax.plot(filePotential['rho'],filePotential['v_eff'], '-', linewidth=0.8, label="Potencial Efetivo")

plt.grid(linestyle='-', linewidth=1)
plt.xlabel(r'$\rho$')
plt.ylabel(r'$V_{eff}$')
plt.title("Potencial Efetivo no Limite Equatorial - Próton 3", fontdict=None)
plt.savefig('PotencialEfetivo_equatorial_P3.png')