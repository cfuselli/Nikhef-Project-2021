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
    theta = np.arctan(0.5*(l+3*x)/h) - np.arctan(0.5*(x-h)/h)
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
    x = 5
    y = 5
    l = 5
    dh = 0.01
    height = np.linspace(dh, 150, int(150/dh))
    res = 1/function(x,y,l,height)
    plt.plot(height, res)