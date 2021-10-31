import matplotlib.pyplot as plt
import pandas as pd

fig_1 = plt.figure(1)

ax1=fig_1.add_subplot(111)
# ax1.set(xlim=(-3, 4))

df_q3=pd.read_csv("dadosP1py2.dat", header = 0, sep='\s+')
df_q4=pd.read_csv("dadosP2py2.dat", header = 0, sep='\s+')
df_q5=pd.read_csv("dadosP3py.dat", header = 0, sep='\s+')

label_1='Proton P1'
label_2='Proton P2'
label_3='Proton P3'

'''Proton 1'''
ax1.plot(df_q3['x'],df_q3['y'], '-', label=label_1)
# ax1.scatter(df_q3['x'],df_q3['y'],marker='8',linewidth=0.1,label=label_1,s=4)
# plt.plot(df_q3['x'],df_q3['y'],linestyle='-',linewidth=0.1)


'''Próton 2'''
ax1.plot(df_q4['x'],df_q4['y'], '-', label=label_2, color='mediumseagreen')
# ax1.scatter(df_q4['x'],df_q4['y'],marker='8',linewidth=0.1,label=label_2,s=4, color='mediumseagreen')
# plt.plot(df_q4['x'],df_q4['y'],linestyle='-',linewidth=0.3, color='mediumseagreen')

a_circle = plt.Circle((0, 0), 0.85, color='gray')
ax1.add_artist(a_circle)

# '''Proton 3'''
# ax1.scatter(df_q5['x'],df_q5['y'],marker='8',linewidth=0.01,label=label_1,s=3)
# plt.plot(df_q5['x'],df_q5['y'],linestyle='-',linewidth=0.2)


plt.grid(linestyle='-', linewidth=0.7)
plt.xlabel("$x(t)$")
plt.ylabel("y(t)")
plt.text(-0.45, -0.15, 'Terra', fontsize = 15)
# plt.yscale("log")
# plt.xscale('log')


plt.title("Prótons no cinturão de radiação de Van Allen", fontdict=None,)
# plt.legend(loc="upper left",ncol=3,fontsize='small')

#plt.show()
plt.savefig('plotCerto.pdf')