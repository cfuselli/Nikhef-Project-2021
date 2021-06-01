# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:23:58 2021

@author: NoorKoster
@author: @haslbeck

# FIXME: rename data to sth meaninful
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy.polynomial.polynomial as poly

def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y

def polyfit(xdata,ydata,p0=None,rank=11):
    
    
    popt  = poly.polyfit(xdata,ydata,rank) #, cov='unscaled')
    print(popt)
    # print out the fit params
    #print('name, par, par err\n%s'%(20*'='))
    #for i in range(rank): print('p%i:\t%.3f\t%.3f'%(i,popt[i],pcov[i][i]))
    
    # create fitfunc
    fitfunc = np.polyval(popt[::-1], xdata)
    
    #vals , errs = [popt[i] for i in range(rank)], [pcov[i][i] for i in range(rank)]
    #return vals , errs , fitfunc
    return fitfunc
    


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
args = parser.parse_args()
if '.txt' in args.in_name: args.in_name = args.in_name[:-4]
print(args.in_name)

# read in the data
data_volt, volt, data, err = [], [],[], []
with open(args.in_path+args.in_name+'.txt') as file_in: 
    for i, line in enumerate(file_in):
        if i < 5 : continue
        if i == 5: 
            det_name = line
            continue
        adc = float(line.split()[2])
        trigger = str(line.split()[0])
        # get the trigger steps
        if trigger=='SET': 
            volt.append(adc)
            # calc ADC mean & std dev per voltage step
            data.append(np.mean(data_volt))
            err.append(np.std(data_volt))
            data_volt = []
            continue
        else: data_volt.append(adc)


# convert to np.array
data_volt, volt, data, err = np.array(data_volt), np.array(volt), np.array(data), np.array(err)
# convert to mV
mV = volt * 1e3 


# fit
#vals , errs , fitfunc = polyfit(volt,data, rank=2)
fitfunc = polyfit(volt,data)

# save values to file
""""
if args.out_name is None: args.out_name = args.in_name + '_calibration'
savefile = open(args.out_path+args.out_name+'.csv','w')
savefile.write("Calibration %s"%det_name) # det_name contains linebreak
for v, e in zip(vals,errs): savefile.write("%f, %f\n"%(v,e))
savefile.close()
print('saved calibration values to %s'%args.out_path+args.out_name+'.csv')
"""

# plot
fontsize = 20 
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
plt.title('Detector: %s'%det_name, size=fontsize)
plt.errorbar(data,mV, xerr = err, fmt='o')
plt.plot(data, fitfunc, color='r')#, label='%i'%len(vals))
plt.yscale('log')
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