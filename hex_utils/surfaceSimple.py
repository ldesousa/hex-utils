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

def well(x, y, x0, y0, depth):

    return depth + ((x - x0)/300.0)**(2) + ((y - y0)/300.0)**(2)

def fun(x, y):

    z = []
    z.append(well(x, y,  250,  250, 9.4))
    z.append(well(x, y,  250,  750, 9.1))
    z.append(well(x, y,  250, 1250, 8.9))
    z.append(well(x, y,  250, 1750, 8.6))
    z.append(well(x, y,  750,  250, 9.2))
    z.append(well(x, y,  750,  750, 8.9))
    z.append(well(x, y,  750, 1250, 8.7))
    z.append(well(x, y,  750, 1750, 8.4))
    z.append(well(x, y, 1250,  250, 8.9))
    z.append(well(x, y, 1250,  750, 8.6))
    z.append(well(x, y, 1250, 1250, 8.4))
    z.append(well(x, y, 1250, 1750, 8.1))
    z.append(well(x, y, 1750,  250, 8.7))
    z.append(well(x, y, 1750,  750, 8.4))
    z.append(well(x, y, 1750, 1250, 8.1))
    z.append(well(x, y, 1750, 1750, 7.9))
    z.append(10 - (x/1900.0) - (y/1900.0))
    
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
