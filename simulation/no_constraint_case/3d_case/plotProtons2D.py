import matplotlib.pyplot as plt
import pandas as pd

fig_1 = plt.figure(1)

ax1=fig_1.add_subplot(111)
#ax1.set(xlim=(-5.1, 15)) # se for plotar com 2 protons, retirar essa linha

fileProton1=pd.read_csv("dadosProton3D_1.dat", header = 0, sep='\s+')
fileProton2=pd.read_csv("dadosProton3D_2.dat", header = 0, sep='\s+')
fileProton3=pd.read_csv("dadosProton3D_3.dat", header = 0, sep='\s+')

label_1='Proton 1'
label_2='Proton 2'
label_3='Proton 3'

'''Proton 1'''
ax1.plot(fileProton1['x'],fileProton1['y'], '-', label=label_1)
# ax1.scatter(fileProton1['x'],fileProton1['y'],marker='8',linewidth=0.1,label=label_1,s=4)
# plt.plot(fileProton1['x'],fileProton1['y'],linestyle='-',linewidth=0.1)


'''Próton 2'''
ax1.plot(fileProton2['x'],fileProton2['y'], '-', label=label_2, color='mediumseagreen')
# ax1.scatter(fileProton2['x'],fileProton2['y'],marker='8',linewidth=0.1,label=label_2,s=4, color='mediumseagreen')
# plt.plot(fileProton2['x'],fileProton2['y'],linestyle='-',linewidth=0.3, color='mediumseagreen')

'''Proton 3'''
ax1.plot(fileProton3['x'],fileProton3['y'], '-', label=label_3)
#ax1.scatter(fileProton3['x'],fileProton3['y'],marker='8',linewidth=0.01,label=label_1,s=3)
# plt.plot(fileProton3['x'],fileProton3['y'],linestyle='-',linewidth=0.2)

a_circle = plt.Circle((0, 0), 0.85, color='gray')
ax1.add_artist(a_circle)

plt.grid(linestyle='-', linewidth=0.7)
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.text(-0.45, -0.15, 'Terra', fontsize = 15) #-0.45 e -0.15 fontsize = 15 é o padrão para plotar com 2 protons
# plt.yscale("log")
# plt.xscale('log')


plt.title("Particles under magnetical force influence", fontdict=None,)
plt.legend(loc="upper right",ncol=3,fontsize='small')

plt.savefig('plot3DPlano.pdf')
plt.show()