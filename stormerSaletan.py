import numpy as np
import plot
import animationStormer

def functionY(x):
    
    y = (1/2*np.sqrt(5))*np.log((2*x - np.sqrt(5)+1)/(2*x + np.sqrt(5)+1)) + (1/np.sqrt(2))*np.log(x*x - x + 1) + np.log(x)
    
    return y

x = 2
h = 0.1
array_x = []
array_y = []

while x < 400:
    array_x.append(x*np.cos(functionY(x)))
    array_y.append(x*np.sin(functionY(x)))
    x = x+h

# plot.plotFigure(array_x, array_y, r'$x\cos(\phi)$', r'$x\sin(\phi)$', r'Problema de Stormer para $\gamma_{1} = \frac{1}{2}$', "stormer.png", 1)
animationStormer.Animate(array_x, array_y)