# -*- coding: utf-8 -*-
"""

@author: NoorKoster
@author: @haslbeck

# FIXME: rename data to sth meaninful
"""

import argparse
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.optimize import curve_fit

parser = argparse.ArgumentParser(description='calibration fit')
# input file
parser.add_argument('-in_name',type=str, help='csv filename with ADC vs V counts')
parser.add_argument('-in_path',type=str,default='../data/',required=False, help='default ../data/')
# output file
parser.add_argument('-out_name',type=str,default=None,required=False, help='calibration constants')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False, help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=1,required=False, help='default 1')
                    
args = parser.parse_args()
if '.csv' in args.in_name: args.in_name = args.in_name[:-4]


def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y

def polyfit(xdata,ydata,p0=None,rank=11):
    
    def chisquared(xdata,ydata,weights,sigma=1,verbose=False):
      """ calc. chi squared with sigma defined by the noise generator
      input:  array xdata
              array ydata
              array fit_weights: polynomial fit weights of order len(fit_weights)
              float sigma = 0.25:  sigma of the data points, 0.25 by the generator
      return: float chi_sq
      """
      M = len(weights) # order pol.
      pred = fit_func(xdata,*weights) # predictions from fit

      chi_sq = np.sum(np.power(ydata-pred,2)) / np.power(sigma,2)
      dof = len(ydata) + M # degree of freedoms
      chi_sq_red = chi_sq/dof

      if verbose: print("pol fit order %i: chi squared reduced %.3f"%(M,chi_sq_red))
      return chi_sq_red
    
    popt, pcov = curve_fit(fit_func, xdata, ydata, p0 = np.zeros(rank))
    chi2red = chisquared(xdata,ydata,popt)
    # print out the fit params
    print('name, par, par err\n%s'%(20*'='))
    for i in range(rank): print('p%i:\t%.3e\t%.3e'%(i,popt[i],np.sqrt(pcov[i][i])))
    print(chi2red)
    print(20*'=')
    
    vals , errs = [popt[i] for i in range(rank)], [np.sqrt(pcov[i][i]) for i in range(rank)]
    return vals , errs , chi2red
    


# read in the data
volt, adc = [], []
with open(args.in_path+args.in_name + '.csv') as csvfile:
    
    reader = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reader):
        # skip header
        if i < args.header : continue
        # FIXME: get detector name? 
        
        # read in data
        if len(line) == 1: adc.append(float(line[0]))
        # get pulsing ampltidude
        elif len(line) == 2:
            _volt = float(line[1])
            continue
        else: continue
        volt.append(_volt)
    
print(len(volt),len(adc))

# convert to np.array
volt, adc= np.array(volt), np.array(adc)
# convert to mV
mV = volt * 1e3 


# fit: degree ranging from degree mmin to mmax
mmin , mmax = 2, 8
result = {m: {} for m in range(mmax)}
print(result)
for m in range(mmin,mmax-1): result[m]['vals'], result[m]['errs'], result[m]['c2r'] = polyfit(adc, np.log(mV), rank=m)
    

# plot
fontsize = 20 
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize-3)
ax.tick_params(axis = 'both', which = 'minor', labelsize = 0)
#plt.title('Detector: %s'%det_name, size=fontsize)
plt.scatter(adc,mV, color = 'k', marker = '.') # weird x y choice on purpose


xplot = np.linspace(50,np.max(adc),1000)
for m in range(mmin,mmax-1):
    vals , c2r = result[m]['vals'], result[m]['c2r']
    plt.plot(xplot, np.exp(fit_func(xplot, *vals)), lw = 2, color=None, label='Polyfit deg. %i, $\chi^2_{red}$=%.1e'%(m,c2r))


plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fontsize)
plt.xlabel('Measured ADC value [0-1023]', size=fontsize)
plt.xticks(np.arange(50, 1000, step=50))
plt.legend()

# close the plot when pressing a key
plt.draw()
plt.pause(1)
savem = int(input('which degree should be saved? '))
print('save ... ',savem)
plt.close('all')



# save user defined best degree values to file
if args.out_name is None: args.out_name = args.in_name + '_calibration'
savefile = open(args.out_path+args.out_name+'.csv','w')
#savefile.write("Calibration %s"%det_name) # det_name contains linebreak
for v, e in zip(result[savem]['vals'],result[savem]['errs']): savefile.write("%s, %s\n"%(v,e))
savefile.close()
print('saved calibration values to %s'%args.out_path+args.out_name+'.csv')


print('goodbye')
