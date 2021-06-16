# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 08:32:44 2021

@author: NoorK
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 22:17:03 2021

@author: NoorK
"""


import argparse
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.optimize import curve_fit


parser = argparse.ArgumentParser(description='calibration fit')
# input file
parser.add_argument('-list','--list', nargs='+', required=True,
                    help='csv filenames with ADC vs mV (Use like: -list_fnames name1 name2 name3')
parser.add_argument('-in_path',type=str,default='../data/',required=False,
                    help=' path for both files: default ../data/')
parser.add_argument('-nfiles',type=str,default='2',required=False,
                    help=' Number of files you want to compare: default 2')

# output file
parser.add_argument('-header',type=int,default=1,required=False,
                    help='default 1')
parser.add_argument('-plotname',type=str,default='plot',required=False,
                    help='Plot name if file names fails')

args = parser.parse_args()


for filename in args.list:
    if '.csv' in filename: filename = filename[:-4]
print('list of files: ',args.list)

# read in the data
def mV_vs_adc(filename):
    volt, adc = [], []
    with open(args.in_path+filename + '.csv') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(reader):
            # skip header
            if i < args.header : continue
            # get pulsing ampltidude
            volt.append(float(line[1]))
            adc.append(float(line[0]))
    
    print(len(volt),len(adc))
    
    # convert to np.array
    volt, adc= np.array(volt), np.array(adc)
    return volt,adc

# make list of lists witd volt (in mV) and adc of each file
datalist=[]
for filename in args.list:
    datalist.append(mV_vs_adc(filename))
    
    
# plot
fontsize = 20
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
#plt.title('Detector: %s'%det_name, size=fontsize)
#plot data for all files
for i in range(int(args.nfiles)):
    plt.scatter(datalist[i][1],datalist[i][0], label = '%s' %args.list[i])


xplot = np.linspace(np.min(datalist[:][0]),np.max(datalist[:][0]),1000)
plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fontsize)
plt.xlabel('Measured ADC value [0-1023]', size=fontsize)
plt.legend()

# close the plot when pressing a key
plt.draw()
try:
    plt.savefig("%s_%s.png"%(args.nfiles, args.list))
except:
    plt.savefig("%s.png"%args.plotname)
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

print('goodbye')
