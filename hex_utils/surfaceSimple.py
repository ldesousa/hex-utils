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
y_top = 9.1208
xn = 8.2776
yn = 10.1108
dx = (xn - oo) / 1980.0
dy = -((yn - y_top) / 1980.0) 

wide01 = 310.0
wide02 = 320.0
wide03 = 340.0
wide04 = 360.0


def pitParabolic(x, y, x0, y0, depth, widening):

    return depth + (abs(x - x0)/widening)**(1.5) + (abs(y - y0)/widening)**(1.5)
    
    
def pitPyramid(x, y, x0, y0, depth, widening):
    
    return depth + abs((x - x0)/widening) + abs((y - y0)/widening)


def pitHubbert(x, y, x0, y0, bottom, depth, slope, widening):

    res = (bottom + depth) - (2 * depth / \
                     ( 1 + np.cosh(slope * \
                        (((x - x0)/widening)**2 + ((y - y0)/widening)**2)))) 
    
    # discard if too far from the bottom
    if (res - bottom) > (depth * 0.999):
        return np.Infinity
    else:
        return res 
    

def fun(x, y):

    z = []
    
    z.append(pitHubbert(x, y,  270,  250, 8.2052, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  270,  730, 8.5342, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  270, 1230, 8.8676, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  270, 1730, 9.2032, 1.3, 5, 350))
    
    z.append(pitHubbert(x, y,  770,  250, 7.9552, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  770,  730, 8.2866, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  770, 1230, 8.6176, 1.3, 5, 350))
    z.append(pitHubbert(x, y,  770, 1730, 8.9509, 1.3, 5, 350))
    
    z.append(pitHubbert(x, y, 1270,  250, 7.7052, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1270,  730, 8.0366, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1270, 1230, 8.3699, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1270, 1730, 8.7009, 1.3, 5, 350))
    
    z.append(pitHubbert(x, y, 1770,  250, 7.4552, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1770,  730, 7.7883, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1770, 1230, 8.1216, 1.3, 5, 350))
    z.append(pitHubbert(x, y, 1770, 1730, 8.4509, 1.3, 5, 350))
    
    z.append(oo + ((x - 10) * dx) - ((y - 10) * dy))
    
    z.sort()
    return z[0]


def main():    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(0, 2000, 5)
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
    
#main()
