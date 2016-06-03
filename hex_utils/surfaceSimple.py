'''
Created on 30 May 2016

@author: lads
'''

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
import random

oo = 9.2676
xn = 8.2776
yn = 10.1108
dx = (xn - oo) / 2000.0
dy = (yn - oo) / 2000.0 

def pit(x, y, x0, y0, depth, widening):

    return depth + ((x - x0)/widening)**(2) + ((y - y0)/widening)**(2)

def fun(x, y):

    z = []
    z.append(pit(x, y,  270,  250, 8.2052, 200.0))
    z.append(pit(x, y,  270,  730, 8.5342, 215.0))
    z.append(pit(x, y,  270, 1230, 8.8676, 230.0))
    z.append(pit(x, y,  270, 1730, 9.2032, 245.0))
    z.append(pit(x, y,  770,  250, 7.9552, 200.0))
    z.append(pit(x, y,  770,  730, 8.2866, 215.0))
    z.append(pit(x, y,  770, 1230, 8.6176, 230.0))
    z.append(pit(x, y,  770, 1730, 8.9509, 245.0))
    z.append(pit(x, y, 1270,  250, 7.7052, 200.0))
    z.append(pit(x, y, 1270,  730, 8.0366, 215.0))
    z.append(pit(x, y, 1270, 1230, 8.3699, 230.0))
    z.append(pit(x, y, 1270, 1730, 8.7009, 245.0))
    z.append(pit(x, y, 1770,  250, 7.4552, 200.0))
    z.append(pit(x, y, 1770,  730, 7.7883, 215.0))
    z.append(pit(x, y, 1770, 1230, 8.1216, 230.0))
    z.append(pit(x, y, 1770, 1730, 8.4509, 245.0))
    
    z.append(oo + (x * dx) - (y * dx))
    
    z.sort()
    return z[0]

    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.arange(0, 2000, 2)
X, Y = np.meshgrid(x, y)
zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')

ax.plot_surface(X, Y, Z, facecolors=rgb)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Height')

plt.show()
