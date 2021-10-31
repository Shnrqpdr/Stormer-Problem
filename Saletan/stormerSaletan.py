import numpy as np
import plot
import animationStormer

# def functionYnegativo(x):
    
#     y = -(1/2*np.sqrt(5))*np.log((2*x - np.sqrt(5)+1)/(2*x + np.sqrt(5)+1)) - (1/np.sqrt(2))*np.log(x*x - x + 1) - np.log(x)
    
#     return y

def functionYpositivo(x):
    
    y = (1/2*np.sqrt(5))*np.log((2*x - np.sqrt(5)+1)/(2*x + np.sqrt(5)+1)) + (1/np.sqrt(2))*np.log(x*x - x + 1) + np.log(x)
    
    return y

x = 2
h = 0.1
array_x1 = []
# array_x2 = []
array_y1 = []
# array_y2 = []

while x < 400:
    array_x1.append(x*np.cos(functionYpositivo(x)))
    # array_x2.append(x*np.cos(functionYnegativo(x)))
    array_y1.append(x*np.sin(functionYpositivo(x)))
    # array_y2.append(x*np.sin(functionYnegativo(x)))
    x = x+h

# plot.plotFigure(array_x1, array_x2, array_y1, array_y2, r'$x\cos(\phi)$', r'$x\sin(\phi)$', r'Problema de Stormer para $\gamma_{1} = \frac{1}{2}$', "stormer3.png", 1)
animationStormer.Animate(array_x1, array_y1)