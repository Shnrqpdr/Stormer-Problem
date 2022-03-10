import numpy as np
import matplotlib.pyplot as plt

def potencial(rho, c20, alpha1, m):
    
    y = ((c20*c20)/((2*m*m)*rho*rho) - (alpha1*c20)/(m*rho*rho*rho) + (alpha1*alpha1)/(2*rho*rho*rho*rho))
    return y

c20 = 1.84379e-24
alpha1 = 3.037e3
m = 1.6726219e-27
x = 0.01
h = 0.00001
array_x1 = []
array_y1 = []

while x < 10.0:
    array_x1.append(x)
    array_y1.append(potencial(x, c20, alpha1, m))
    #print(x, potencial(x, c20, alpha1, m))
    x = x+h
    
#print(array_x1, array_y1)
fig = plt.figure(1)

ax = fig.add_subplot()
 
ax.set(ylim=(0, 8000))
ax.set(xlim=(1.0, 7.0))
ax.set_xlabel(r'$\rho$')
ax.set_ylabel(r'$V_{eff}$')
    
ax.plot(array_x1, array_y1, '-')
    
# plt.xscale('log')
# plt.yscale("log")
    
plt.grid(linestyle='-', linewidth=0.7)
# plt.legend(loc="upper right",ncol=3,fontsize='small')
plt.title("Potencial Efetivo para o caso do limite equatorial", fontdict=None)
plt.savefig("Potencial_Efetivo_equatorial.png") 