from matplotlib.pyplot import polar
import numpy as np

# DECLARATION OF VARIABLE AND CONSTANTS

p = []
dp = []
phi = []
dphi = 10.0
p.append(3.0)
dp.append(10.0)
phi.append(0.0)
m = 1.6726219e-27
alpha1 = 3.037e3
c20 = m*(p[0]*p[0])*dphi + m*alpha1*(1/p[0])

# FUNCTIONS

def cart2polar(x, y):
    p = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(p, phi)

def polar2cart(p, phi):
    x = p * np.cos(phi)
    y = p * np.sin(phi)
    return(x, y)

def dVdp(p):
    return (c20*c20)/(m*m)*(1/(p*p*p)) - (3*alpha1*c20)/(m)*(1/(p*p*p*p)) + (2*alpha1*alpha1)/(p*p*p*p*p)

def stormer_verlet_method(p, dp, phi, deltaT):
    for n in range (1, 20000):
        p[n] = p[n-1] + deltaT*dp[n-1] + (deltaT*deltaT*dVdp(p[n-1]))/2
        dp[n] = dp[n-1] + (deltaT/2)*dVdp(p[n-1]) + (deltaT/2)*dVdp(p[n])
        phi[n] = phi[n-1] + deltaT*((c20/(m*p[n-1]*p[n-1])) - (alpha1/(p[n-1]*p[n-1]*p[n-1])))
        
        print('%s %s %s', n, p, dp)
        
    return (p, dp, phi)

deltaT = 0.0001

stormer_verlet_method(p, dp, phi, deltaT)

x = []
y = []
z = np.zeros()

(x, y) = polar2cart(p, phi)

print('%s %s', x, y)

