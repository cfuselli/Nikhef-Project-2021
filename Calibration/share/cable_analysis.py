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
parser.add_argument('-path',type=str,default='../data/cable_test/',required=False,
                    help='default ../data/cable_test/')

# output file
parser.add_argument('-out_name',type=str,default=None,required=False,
                    help='calibration constants')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=3,required=False,
                    help='default 3')

parser.add_argument('-fit',action='store_true',default=False,required=False,
                    help='perform an exponential fit to time spectrum, default FALSE)')
parser.add_argument('-norm',action='store_false',default=True,required=False,
                    help='normalise histograms, default True')

parser.add_argument('-dist',type=str,default="cable",required=False,
                    help='distinction keyword for classes eg. "cable" (default)')
parser.add_argument('-dist2',type=str,default=None,required=False,
                    help='distinction 2 keyword for classes eg. None (default)')

parser.add_argument('-label',type=str,default=None,required=False,
                    help='histogram label matching dist')
parser.add_argument('-labeld',type=str,default=None,required=False,
                    help='histogram label2 matching NOT dist ')
parser.add_argument('-labeld2',type=str,default=None,required=False,
                    help='histogram label2 matching dist2')


args = parser.parse_args()

hist_colors = ["blue", "red", "green"] 
#["darkblue", "darkred", "darkgreen"]
fit_colors = ["blue", "red", "green"] 


def fit_func(x, a, b):
    """ exp. pdf fct """
    y = a*np.exp(-b*x)
    return y

def exp_pdf_fit(xdata,ydata,xmin=None,xmax=None,p0=[0.1,0.05]):
    
    if xmin is not None: 
        ind = np.where(xdata > xmin)
        xdata = xdata[ind]
        ydata = ydata[ind]
    if xmax is not None:
        ind = np.where(xdata < xmax)
        xdata = xdata[ind]
        ydata = ydata[ind]
        
    popt, pcov = curve_fit(fit_func, xdata, ydata, p0 = p0, bounds=(0., [2., 2.]))
    
    # print out the fit params
    print('par, par err\n%s'%(20*'='))
    print('%.3e\t%.3e'%(popt[0],pcov[0][0]))
    print('%.3e\t%.3e'%(popt[1],pcov[1][1]))
    print(20*'=')
    
    vals , errs = (popt[0],popt[1]), (np.sqrt(pcov[0][0]),np.sqrt(pcov[1][1]))
    return vals , errs 
    


def make_hist(id,data,xname,bins=256,x_range=(0,1023),label=None,alpha=1, FIT = args.fit, NORM = args.norm, color_id = None):
    plt.figure(id)
    
    if color_id is not None: data, bin_x , _ = plt.hist(data,bins=bins,range=x_range,density=NORM,\
                                                        alpha=alpha,label=label,color = hist_colors[color_id],\
                                                        ec = hist_colors[color_id], histtype='step')
    else: data, bin_x , _ = plt.hist(data,bins=bins,range=x_range,density=NORM,alpha=alpha,label=label)

    plt.xlabel(xname)
    if NORM: plt.ylabel("Normalised Entries")
    else: plt.ylabel('Entries')
    if label is not None: plt.legend()

    
    # fit time diff distr
    if FIT:
        bin_centers = np.array([(bin_x[i]+bin_x[i+1]) for i in range(len(bin_x)-1)]) * 0.5
        
        if "Time" in xname: xmin, xmax , p0 = 0.5, 25, [0.1,0.05]
        elif "ADC" in xname: xmin, xmax, p0 = 50, 700, [0.01,0.001]
        else: xmin, xmax = -np.inf, np.inf
        vals, errs = exp_pdf_fit(bin_centers, data, xmin, xmax)
        xplot = np.linspace(xmin,xmax,bins*2)
        label="%s Fit $a * e^{-\lambda x}$\n"%label
        if "Time" in xname: 
            label+="$a$ = (%.1f$\pm$%.1f)\n"%(vals[0],errs[0])
            label+="$\lambda$ = (%.2f$\pm$%.2f)"%(vals[1],errs[1])
        elif "ADC" in xname:
            label+="$a$ = (%.1e$\pm$%.1e)\n"%(vals[0],errs[0])
            label+="$\lambda$ = (%.2e$\pm$%.2e)"%(vals[1],errs[1])
        if color_id is not None: 
            plt.plot(xplot, fit_func(xplot, *vals),\
                     label=label,linestyle='dashed',color = fit_colors[color_id]) 
        else: plt.plot(xplot, fit_func(xplot, *vals), label = label) 
    plt.legend()
    

DISTINCTION = args.dist
DISTINCTION_2 = args.dist2

# read in the data
files = args.f

# for combined plot
adc_scint, adc_cable = [] , []
timediff_cable, timediff_scint = [] , []
if DISTINCTION_2 is not None: adc_else, timediff_else = [] , [] # if 3rd alternative needed

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


    make_hist(1,adc,'ADC',label=f,bins=128,x_range=(0,1023), FIT = args.fit, NORM = args.norm)
    make_hist(2,timediff,'Time diff [s]',label=f,x_range=(0,5),bins=60, FIT = args.fit, NORM = args.norm)

    #make_hist(5,adc,'ADC',label=f,bins=16,x_range=(0,256), FIT = args.fit, NORM = args.norm)

#plots combining multiple files


# make nice labels
label_scint = 'total %s'%DISTINCTION if args.label is None else args.label

dist2_label = DISTINCTION_2 if DISTINCTION_2 is not None else "NOT %s"%DISTINCTION
label_cable = 'total %s'%dist2_label if args.labeld is None else args.labeld

adc_range, adc_bins = (0,1023), 32
make_hist(3,adc_cable,'ADC',label=label_cable,x_range=adc_range,bins=adc_bins,color_id = 0)
make_hist(3,adc_scint,'ADC',label=label_scint,x_range=adc_range,bins=adc_bins,color_id = 1)

# timediff
time_range , time_bins = (0,30), 30
make_hist(4,timediff_cable,'Time difference between two counts ($\geq$ 0.5s) [s]',label=label_cable,x_range=time_range,bins=time_bins,color_id = 0)
make_hist(4,timediff_scint,'Time difference between two counts ($\geq$ 0.5s) [s]',label=label_scint,x_range=time_range,bins=time_bins,color_id = 1)


if DISTINCTION_2 is not None:

    label_else = 'total rest' if args.labeld2 is None else args.labeld2
    make_hist(3,adc_else,'ADC',label=label_else,x_range=adc_range,bins=adc_bins,color_id = 2)
    make_hist(4,timediff_else,'Time difference between two counts ($\geq$ 0.5s) [s]',label=label_else,x_range=time_range,bins=time_bins,color_id = 2)


# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')


print('goodbye')

