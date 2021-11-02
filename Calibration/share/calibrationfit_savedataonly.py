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
                    help='data for plot (mV & adc)')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=1,required=False,
                    help='default 1')

args = parser.parse_args()
if '.csv' in args.in_name: args.in_name = args.in_name[:-4]


# read in the data
volt, adc = [], []
with open(args.in_path+args.in_name + '.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reader):
        # skip header
        if i < args.header : continue
        # FIXME: get detector name?
        # get pulsing ampltidude
        if len(line) == 2:
            _volt = float(line[1])
            print(_volt)
            continue

        # read in data
        elif len(line) == 1:
            if float(line[0]) > 60:
                adc.append(float(line[0]))
                volt.append(_volt)
        else: continue


print(len(volt),len(adc))

# convert to np.array
volt, adc= np.array(volt), np.array(adc)
# convert to mV
mV = volt * 1e3

new_name = args.in_name + '_comp'
savefile = open(args.out_path+new_name+'.csv','w')
savefile.write("ADC, mV %s \n"%args.in_name) # det_name contains linebreak
for v, e in zip(adc,mV): savefile.write("%f, %f\n"%(v,e))
savefile.close()
print('saved datapoints ADC & mV values to %s.csv'%new_name)
