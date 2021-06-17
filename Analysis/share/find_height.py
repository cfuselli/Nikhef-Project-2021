# numerical analysis to get idea how far to distance the detector layers
# @haslbeck
# 17 June 2021

import numpy as np
import matplotlib.pyplot as plt

heights = np.linspace(5,150,145)

def normed_events(h=heights):
    """ normalised to unity events """
    def events(h=h):
        """ calc events to arb. unit """
        def invTan(h):
            return np.arctan(10/h)
    
        it = invTan(h)
        return (it + np.sin(it) * np.cos(it) )
        
    # normalise 
    e = events()
    norm = 1/e.max()
    e_norm = e * norm
    return e_norm
    
def normed_resolution(h=heights):
    """ normalised to unity events """
    def resolution(x=5,y=5,l=5,h=h):
        theta = np.arctan(0.5*(l+3*x)/h) - np.arctan(0.5*(x-l)/h)
        res = 1/theta
        return res
        
    r = resolution()
    norm = 1/r.max()
    r_norm = r * norm
    return r_norm
    
def normed_angle(h=heights):
    """ normalised to unity angle theta """
    def theta(h=h):
        return np.arctan(10/h)
    
    t = theta()
    norm = 1/t.max()
    t_norm = t * norm
    return t_norm



plt.plot(heights, normed_events(), label = 'normalised events')
plt.plot(heights, normed_resolution(), label = 'normalised resolution')
plt.plot(heights, normed_angle(), label = 'normalised angle $\\theta$')
plt.xlim(0,160)
plt.xlabel("distance between scintillator layers [cm]")
plt.ylabel("[a.u.]")
plt.legend()

plt.draw()
plt.savefig("../data/find_height.png")

plt.pause(1)
input('press any key to close')
plt.close('all')


print('goodbye')
