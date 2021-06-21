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

parser = argparse.ArgumentParser(description='Plot multiple ratios vs. input voltage. -FIRST RUN: analysis_voltage.py to get the right .csv files')
# input files
parser.add_argument('-list','--list', nargs='+', required=True,
                    help='csv filenames with voltage in- and output (Use like: -list_fnames name1 name2 name3')
parser.add_argument('-in_path',type=str,default='../data/',required=False,
                    help='default ../data/')
# output file
parser.add_argument('-out_name',type=str,default='Naamloos',required=False,
                    help='figure name')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=0,required=False,
                    help='default 0')


args = parser.parse_args()
for filename in args.list:
    if '.csv' in filename: filename = filename[:-4]
print('list of files: ',args.list)


def get_list_ratio_input(filename):
    # read in the data
    volt_in, ratio, std_ratio = [], [], []
    with open(args.in_path+filename + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(reader):
            ratio.append(float(line[0]))
            std_ratio.append(float(line[1]))
            volt_in.append(float(line[2]))

    #convert to np.array
    ratio, std_ratio, volt_in = np.array(ratio), np.array(std_ratio),  np.array(volt_in)

    return ratio, std_ratio, volt_in


datalist = []
for filename in args.list:
    datalist.append(get_list_ratio_input(filename))

# plot
fontsize = 20
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
#plt.title('Detector: %s'%det_name, size=fontsize)
for i in range(len(args.list)):
    plt.errorbar(datalist[i][2],datalist[i][0], yerr = datalist[i][1], fmt='o', label = args.list[i]) # weird x y choice on purpose
#plt.grid(True, which="both")
plt.xlabel(r'Input [mV]', size=fontsize)
plt.ylabel('Ratio [Output/Input]', size=fontsize)
plt.legend(fontsize=15)

# close the plot when pressing a key
plt.draw()
plt.savefig('%s.png'%args.out_name)
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

# print('goodbye')
