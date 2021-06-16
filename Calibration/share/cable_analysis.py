# -*- coding: utf-8 -*-
"""
# analysis script for cable test
@author: @haslbeck
"""

import argparse
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

parser = argparse.ArgumentParser(description='calibration fit')
# input file
parser.add_argument('-f',type=str, nargs='+', 
                    help='csv filename with timestamp, ADC counts')
parser.add_argument('-path',type=str,default='../data/cable/',required=False,
                    help='default ../data/cable/')
# output file
parser.add_argument('-out_name',type=str,default=None,required=False,
                    help='calibration constants')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=3,required=False,
                    help='default 3')
parser.add_argument('-dist',type=str,default="cable",required=False,
                    help='distinction keyword for classes eg. "cable" (default)')
parser.add_argument('-dist2',type=str,default=None,required=False,
                    help='distinction 2 keyword for classes eg. None (default)')


args = parser.parse_args()



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
    

def make_hist(id,data,xname,bins=256,range=(0,1023),label=None,alpha=0.35):
    plt.figure(id)
    plt.hist(data,bins=bins,range=range,density=True,alpha=alpha,label=label)
    plt.xlabel(xname)
    plt.ylabel('Entries')
    if label is not None: plt.legend()

DISTINCTION = args.dist
DISTINCTION_2 = args.dist2

# read in the data
files = args.f

# for combined plot
adc_scint, adc_cable = [] , []
timediff_cable, timediff_scint = [] , []
if DISTINCTION_2 is not None:    adc_else, timediff_else = [] , [] # if 3rd alternative needed

for f in files: 
    # remove additional .csv
    if '.csv' in f: f = f[:-4]
    
    timestamp, adc = [], []
    with open(args.path+ f + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(reader):
            # skip header
            if i < args.header : continue
            # read in data
            timestamp.append(float(line[0]))
            adc.append(float(line[1]))
    
    timediff = [timestamp[i+1]-timestamp[i] for i in range(len(timestamp)-1)]        
        
    print(len(timestamp),len(adc),len(timediff))
    
    if DISTINCTION in f:
        adc_scint.extend(adc)
        timediff_scint.extend(timediff)
    else:
        if DISTINCTION_2 is None:
            adc_cable.extend(adc)
            timediff_cable.extend(timediff)
        else:
            if DISTINCTION_2 in f:
                adc_cable.extend(adc)
                timediff_cable.extend(timediff)
            else:
                adc_else.extend(adc)
                timediff_else.extend(timediff)


    make_hist(1,adc,'ADC',label=f,bins=128)
    make_hist(2,timediff,'Time diff [s]',label=f,range=(0,60),bins=60)

dist2_label = DISTINCTION_2 if DISTINCTION_2 is not None else "NOT %s"%DISTINCTION

make_hist(3,adc_cable,'ADC',label='total %s'%DISTINCTION,bins=128)
make_hist(3,adc_scint,'ADC',label='total %s'%dist2_label,bins=128)

make_hist(4,timediff_cable,'Time diff [s]',label='total %s'%DISTINCTION,range=(0,60),bins=60)
make_hist(4,timediff_scint,'Time diff [s]',label='total %s'%dist2_label,range=(0,60),bins=60)


if DISTINCTION_2 is not None:
    make_hist(3,adc_else,'ADC',label='total rest',bins=128)
    make_hist(4,timediff_scint,'Time diff [s]',label='total rest',range=(0,60),bins=60)

# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')


print('goodbye')

