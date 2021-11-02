#!/usr/bin/env python3
# angle analysis considering errors in angles and counts
#
# @haslbeck
# 5 July

import pandas as pd
import numpy as np
from scipy import odr
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# read in data
data = pd.read_csv('../data/counts_angle.csv', skiprows = 1, header = 0, names = ['folder', 'angle', 'height', 'counts', 'time', 'angle_err'])
data = data.sort_values(by = ['angle']).reset_index()

counts = data['counts'].values
times = data['time'].values
angles = data['angle'].values
angles_errs = data['angle_err'].values
norm_counts = counts /times
norm_counts_errs = np.sqrt(counts) / times


print(
    type(counts), len(counts),
    type(times), len(times),
    type(angles), len(angles),
    type(norm_counts), len(norm_counts),
    type(norm_counts_errs), len(norm_counts_errs),
    
)


def func(x, a):
    return a * np.cos(x) ** 2 #+ c

'''   
# Model object
model = odr.Model(func)

# Create a RealData object
data = odr.RealData(angles, norm_counts, sx=angles_errs, sy=norm_counts_errs) #FIXME

# Set up ODR with the model and data and intial guess
odr = odr.ODR(data, model, beta0=[0.1])

# Run the regression.
out = odr.run()

#print fit parameters and 1-sigma estimates
popt = out.beta
perr = out.sd_beta
print('fit parameter 1-sigma error')
print('———————————–')
for i in range(len(popt)): print('%s +- %s'%(popt[i],perr[i]))

# prepare confidence level curves
nstd = 5. # to draw 5-sigma intervals
popt_up = popt + nstd * perr
popt_dw = popt - nstd * perr
# fit line to draw
x_fit = np.linspace(min(angles), max(angles), 100)
fit = func(popt, x_fit)
fit_up = func(popt_up, x_fit)
fit_dw= func(popt_dw, x_fit)
''' 
    
def fit(func, xdata = angles, ydata = norm_counts, yerrs = norm_counts_errs, p0 = None):
    """ perform a chi2 fit """
    
    popt, pcov = curve_fit(func, xdata, ydata, sigma = yerrs, absolute_sigma = True, p0 = p0)
    npars = len(popt)
    
    # goodness of the fit
    res = (ydata - func(xdata, *popt))
    chi2 = np.sum((res/yerrs)**2)
    chi2red = chi2/(len(xdata)-len(popt))
    
    
    # fit values
    print(20*'=')
    print('%s, par, par err\n%s'%(func.__name__,20*'-'))
    print('chi2 %.2f chi2red %.2f'%(chi2,chi2red))
    for i in range(npars): print('p%i:\t%.3f\t%.3f'%(i,popt[i],np.sqrt(pcov[i][i])))
    print(20*'=')
    
    vals , errs = np.asarray([popt[i] for i in range(npars)]), np.asarray([np.sqrt(pcov[i][i]) for i in range(npars)])
    return vals , errs, chi2red
    
'''
# std fit
#popt, pcov = curve_fit(func, angles, norm_counts)
popt, pcov = curve_fit(func, angles, norm_counts, sigma = norm_counts_errs, absolute_sigma = True, p0 = [0.06])
print('I = %.3f'%popt[0])
print('I_err = %.3f'%np.sqrt(pcov[0][0]))
'''

def cos2(x, a):
    return a * np.cos(x) ** 2 
    
def cos2plusb(x, a,b):
    return a * np.cos(x) ** 2 + b

v1, e1, c1 = fit(cos2)
v2, e2, c2 = fit(cos2plusb)





#plot
xplot = np.linspace(min(angles), max(angles), 100)

plt.figure()
#rcParams['font.size']= 20
plt.errorbar(angles, norm_counts, yerr=norm_counts_errs, xerr=angles_errs,  ecolor='k', fmt='ok')

# fits



plt.plot(xplot, cos2plusb(xplot,*v2), 'r', lw=2, label="$I_{0}~cos(x)^2 + c$ and 3(5)$\sigma$, $\chi^2_{red}$=%.1f\n"%c2 + \
                                                       "$I_{0}$=(%.1f$\pm$%.1f)$10^{-2}$ [$\\frac{N}{s}$]\n"%(v2[0]*100,e2[0]*100) + \
                                                       "$c$ =(%.1f$\pm$%.1f)$10^{-2}$ [$\\frac{N}{s}$]"%(v2[1]*100,e2[1]*100))
plt.fill_between(xplot, cos2plusb(xplot,*(v2-3*e2)), cos2plusb(xplot,*(v2+3*e2)),\
                color="red",alpha=0.25,edgecolor="r",hatch='||')

plt.fill_between(xplot, cos2plusb(xplot,*(v2-5*e2)), cos2plusb(xplot,*(v2+5*e2)), \
                color="red",alpha=0.2,edgecolor="r")
                
                




plt.plot(xplot, cos2(xplot,*v1), 'b', lw=2, label="$I_{0} ~cos(x)}^2$ and 3(5)$\sigma$, $\chi^2_{red}$=%.1f\n"%c1 + \
                                                  "$I_{0}$=(%.1f$\pm$%.1f)$10^{-2}$ [$\\frac{N}{s}$]"%(*v1*100,*e1*100))
plt.fill_between(xplot, cos2(xplot,*(v1-3*e1)), cos2(xplot,*(v1+3*e1)), color='blue',alpha=.25, hatch = '---')

plt.fill_between(xplot, cos2(xplot,*(v1-5*e1)), cos2(xplot,*(v1+5*e1)), color='blue',alpha=.2)
                                                  
plt.plot(xplot, cos2plusb(xplot,*v2), 'r' , lw=2)


plt.ylim(-.005,0.09)
#plt.xlim(-.05,1.8)




plt.legend(loc='best',fontsize=10, frameon = False)
plt.xlabel('Zenith angle [Radians]', fontsize=12)
plt.ylabel('Count rate [$\\frac{N}{s}$ $\pm$ $\\frac{\sqrt{N}}{s}$]  ', fontsize=12)

plt.savefig('../data/angle_fit.png',dpi=300, bbox_inches='tight')



# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')
print('goodbye')

  