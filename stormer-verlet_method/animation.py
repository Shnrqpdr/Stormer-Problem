from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
from sys import argv

#file = argv[1]

#data = np.loadtxt('Wave.dat')

#x = data[:0]

#y = data[:1]

#z = data[:2]

tam = 60
temp = 5998

df_q3=pd.read_csv("dadosProton1.dat", header = 0, sep='\s+')

x,y,z = np.loadtxt('CosmicStringData.dat', unpack = True)

#t2 = np.split(t,100)
#x2 = np.split(x,(tam - 2)*(tam - 2))
#y2 = np.split(y,(tam - 2)*(tam - 2))
#z2 = np.split(z,(tam - 2)*(tam - 2))
x2 = np.split(x,temp)
y2 = np.split(y,temp)
z2 = np.split(z,temp)

for i in range(1,temp-2):
	
	df = pd.DataFrame({'x':x2[i],'y':y2[i],'z':z2[i]})

	fig = plt.figure()

	#print(np.asarray(x).shape)

	ax = Axes3D(fig)
	ax.set_zlim(-1.6, 1.6)
	# ax.set_axis_off()
	# ax.set_facecolor((0,0,0))
	ax.set_zlim(-1, 4)
	ax.set_xlim(-1, 3500)
	ax.set_ylim(-1, 4)

	surf = ax.scatter(df.x,df.y,df.z, cmap = cm.jet, linewidth = 0.1)

#	fig.colorbar(surf, shrink = 0.5, aspect = 0.5)
	
	# plt.savefig('imagens/'+str(i)+'.png', dpi = 300)

	plt.show()