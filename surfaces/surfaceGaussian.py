'''
Created on 30 May 2016

@author: lads
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from surfaces.pitGaussian import Gaussian

oo = 9.2676
y_top = 9.1208
xn = 8.2776
yn = 10.1108
dx = (xn - oo) / 1980.0
dy = -((yn - y_top) / 1980.0) 

depth = 1.3
slope = 5
widenning = 300

p1  = Gaussian( 270,  250, 8.2052, depth, slope, widenning)
p2  = Gaussian( 270,  730, 8.5342, depth, slope, widenning)
p3  = Gaussian( 270, 1230, 8.8676, depth, slope, widenning)
p4  = Gaussian( 270, 1730, 9.2032, depth, slope, widenning)
    
p5  = Gaussian( 770,  250, 7.9552, depth, slope, widenning)
p6  = Gaussian( 770,  730, 8.2866, depth, slope, widenning)
p7  = Gaussian( 770, 1230, 8.6176, depth, slope, widenning)
p8  = Gaussian( 770, 1730, 8.9509, depth, slope, widenning)
    
p9  = Gaussian(1270,  250, 7.7052, depth, slope, widenning)
p10 = Gaussian(1270,  730, 8.0366, depth, slope, widenning)
p11 = Gaussian(1270, 1230, 8.3699, depth, slope, widenning)
p12 = Gaussian(1270, 1730, 8.7009, depth, slope, widenning)
    
p13 = Gaussian(1770,  250, 7.4552, depth, slope, widenning)
p14 = Gaussian(1770,  730, 7.7883, depth, slope, widenning)
p15 = Gaussian(1770, 1230, 8.1216, depth, slope, widenning)
p16 = Gaussian(1770, 1730, 8.4509, depth, slope, widenning)
    

def fun(x, y):

    z = []
    
    z.append(p1.fun(x, y,  True))
    z.append(p2.fun(x, y,  True))
    z.append(p3.fun(x, y,  True))
    z.append(p4.fun(x, y,  True))
    
    z.append(p5.fun(x, y,  True))
    z.append(p6.fun(x, y,  True))
    z.append(p7.fun(x, y,  True))
    z.append(p8.fun(x, y,  True))
        
    z.append(p9.fun(x, y,  True))
    z.append(p10.fun(x, y,  True))
    z.append(p11.fun(x, y,  True))
    z.append(p12.fun(x, y,  True))
        
    z.append(p13.fun(x, y,  True))
    z.append(p14.fun(x, y,  True))
    z.append(p15.fun(x, y,  True))
    z.append(p16.fun(x, y,  True))
        
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
