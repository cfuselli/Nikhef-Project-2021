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


def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
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
volt, adc, volt_one = [], [], []
with open(args.in_path+args.in_name + '.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reader):
        # skip header
        if i < args.header : continue
        # FIXME: get detector name?
        count=0
        # read in data

        # get pulsing ampltidude
        if len(line) == 2 :
            # Make a list of al the voltages
            _volt = float(line[1])
            print(_volt)
            volt_one.append(_volt)
            continue
        elif len(line)==1 and count<12:
            if float(line[0]) > 60:
                adc.append(float(line[0]))
                count+=1

        else: continue
        #volt.append(_volt)

print(len(volt_one),len(adc))

# For each voltage we have 12 measurements so make a list of 12 elements having a single voltage
for i in range(len(volt_one)):
    for j in range(12):
        volt.append(volt_one[i])

#Now delete all the extra values
volt = volt[:len(adc)]



# convert to np.array
volt, adc= np.array(volt), np.array(adc)
# convert to mV
mV = volt * 1e3


# fit
vals , errs = polyfit(adc, mV, rank=6)

chi2 = np.sum((mV-fit_func(adc))**2/fit_func(adc))
print('chi2 = ', chi2)

# save values to file

if args.out_name is None: args.out_name = args.in_name + '_calibration_params'
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
plt.title('%s'%args.in_name, size=fontsize)
plt.scatter(adc,mV, s=6) # weird x y choice on purpose

xplot = np.linspace(np.min(adc),np.max(adc),1000)
plt.plot(xplot, fit_func(xplot, *vals), color='r', label='%i-th order polynomial'%len(vals))
plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fontsize)
plt.xlabel('Measured ADC value [0-1023]', size=fontsize)
plt.legend()
plt.savefig('%s.png' %args.in_name)

# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

print('goodbye')
