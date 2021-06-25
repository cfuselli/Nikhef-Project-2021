# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:23:58 2021

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
parser.add_argument('-in_name',type=str,
                    help='csv filename with ADC vs V counts')
parser.add_argument('-in_path',type=str,default='../data/',required=False,
                    help='default ../data/')
# output file
parser.add_argument('-out_name',type=str,default=None,required=False,
                    help='calibration constants')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=1,required=False,
                    help='default 1')
                    
args = parser.parse_args()
if '.csv' in args.in_name: args.in_name = args.in_name[:-4]


#def fit_func(x, *coeffs):
#    y = np.polyval(coeffs, x)
#    return y
    
def fit_func(x, p0,p1,p2,p3):
    y = p0 + p1*x + p2*x**2 + p3*x**3  
    
    
    return y

def polyfit(xdata,ydata,p0=None,rank=11):
    
    popt, pcov = curve_fit(fit_func, xdata, ydata, p0 = np.zeros(rank))
    
    # print out the fit params
    print('name, par, par err\n%s'%(20*'='))
    for i in range(rank): print('p%i:\t%.3f\t%.3f'%(i,popt[i],pcov[i][i]))
    print(20*'=')
    
    vals , errs = [popt[i] for i in range(rank)], [pcov[i][i] for i in range(rank)]
    return vals , errs 
    


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
            print(_volt)
            continue
        else: continue
        volt.append(_volt)
    
print(len(volt),len(adc))

# convert to np.array
volt, adc= np.array(volt), np.array(adc)
# convert to mV
mV = volt * 1e3 


# fit
vals , errs = polyfit(adc, mV, rank=6)


# save values to file

if args.out_name is None: args.out_name = args.in_name + '_calibration'
savefile = open(args.out_path+args.out_name+'.csv','w')
#savefile.write("Calibration %s"%det_name) # det_name contains linebreak
for v, e in zip(vals,errs): savefile.write("%f, %f\n"%(v,e))
savefile.close()
print('saved calibration values to %s'%args.out_path+args.out_name+'.csv')




# plot
fontsize = 20 
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
#plt.title('Detector: %s'%det_name, size=fontsize)
plt.scatter(adc,mV) # weird x y choice on purpose

xplot = np.linspace(np.min(adc),np.max(adc),1000)
#plt.plot(xplot, fit_func(xplot, *vals), color='r', label='%i'%len(vals))
#plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fontsize)
plt.xlabel('Measured ADC value [0-1023]', size=fontsize)
plt.legend()

# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

print('goodbye')
