#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 13:51:46 2021

@author: rensoudheusden
"""
import numpy as np
import matplotlib.pyplot as plt

def thetasquare1(x,y,l,h):
    theta = 2*np.arctan(0.5*(l+x)/h)
    return theta

def phisquare1(x,y,l,h):
    phi = 2*np.arctan(0.5*(l+y)/h)
    return phi

def thetasquare2(x,y,l,h):
    theta = 2*np.arctan(0.5*(l+x)/h)
    return theta

def phisquare2(x,y,l,h):
    phi = np.arctan(0.5*(l+3*y)/h) - np.arctan(0.5*(y-l)/h)
    return phi
    
def thetasquare3(x,y,l,h):
    theta = np.arctan(0.5*(l+3*x)/h) - np.arctan(0.5*(x-l)/h)
    return theta

def phisquare3(x,y,l,h):
    phi = 2*np.arctan(0.5*(l+y)/h)
    return phi

def thetasquare4(x,y,l,h):
    theta = np.arctan(0.5*(l+3*x)/h) - np.arctan(0.5*(x-l)/h)
    return theta

def phisquare4(x,y,l,h):
    phi = np.arctan(0.5*(l+3*y)/h) - np.arctan(0.5*(y-l)/h)
    return phi

def plott(function):
    x = 5  # dimensions of dector
    y = 5
    l = 5
    dh = 0.01
    height = np.linspace(dh, 150, int(150/dh))
    res = 1/function(x,y,l,height)
    
    plt.figure()
    plt.plot(height, res)
    plt.xlabel('Height [cm]')
    plt.ylabel('Resolution [1/rad]')
    plt.title(function.__name__)
    plt.draw()
    
def plot_nfunctions(functions=\
                    [thetasquare1,thetasquare2,thetasquare3,thetasquare4,\
                    phisquare1,phisquare2,phisquare3,phisquare4]):
    x = 5 
    y = 5
    l = 5
    dh = 0.01
    height = np.linspace(dh, 150, int(150/dh))
    
    
    for function in functions:
        name = function.__name__
        if 'theta' in name: 
            plt.figure(1)
        else: 
            plt.figure(2)
        res = 1/function(x,y,l,height)
        plt.plot(height, res, label=name[-1])
    #
    #plt.title(function.__name__)
    plt.figure(1)
    plt.xlabel('Height [cm]')
    plt.ylabel('Resolution $\\theta_{zx}$ [1/rad]')
    plt.legend()
    plt.draw()
    
    plt.figure(2)
    plt.xlabel('Height [cm]')
    plt.ylabel('Resolution $\\theta{zy}$ [1/rad]')
    plt.legend()
    plt.draw()
    
if __name__ == '__main__':
    # get resolution for each detector cell
    plot_nfunctions()
    
    #plott(thetasquare1)
    #plott(phisquare1)
    
    plt.draw()
    #try:
    #    plt.savefig("%s_%s.png"%(args.nfiles, args.list))
    #except:
    #    plt.savefig("%s.png"%args.plotname)
    plt.pause(1)
    input('press any key to close')
    plt.close('all')
    
    
    