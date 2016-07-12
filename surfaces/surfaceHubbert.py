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


peakValue = 5
peakPoint = 5
slope = 3
widenning = 4


def fun(x, y):                      
                       
    return peakValue - (2 * peakValue / ( 1 + np.cosh(slope * \
                        (((x - peakPoint)/widenning)**2 + ((y - peakPoint)/widenning)**2)))) 


def main():    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(0, 10, 0.1)
    X, Y = np.meshgrid(x, y)
    zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    
    ax.plot_wireframe(X, Y, Z)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Height')
    
    plt.show()
    
main()
