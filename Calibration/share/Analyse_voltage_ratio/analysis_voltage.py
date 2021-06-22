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

parser = argparse.ArgumentParser(description='Plot ratio Output [mV] over Input [mV]. Input is voltage dispayed on pulse generator, output is voltage measured from BNC output.')
# input file
parser.add_argument('-in_name',type=str,
                    help='csv filename with input voltages and measured voltages')
parser.add_argument('-in_path',type=str,default='../data/',required=False,
                    help='default ../data/')
# output file
parser.add_argument('-out_name',type=str,default=None,required=False,
                    help='.csv file with: ratio(out/in), std ratio, input voltage per line')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,
                    help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=0,required=False,
                    help='default 0')


args = parser.parse_args()
if '.csv' in args.in_name: args.in_name = args.in_name[:-4]



# read in the data
output_per_step, output,output_std, input1 = [], [],[],[]
with open(args.in_path+args.in_name + '.csv') as csvfile:

    reader = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reader):
        # skip header
        if i < args.header : continue
        # FIXME: get detector name?

        # read in data
        if len(line) == 1:
            _output = float(line[0])

            output_per_step.append(_output)

        # get pulsing ampltidude
        elif len(line) == 2:
            _input = float(line[1])
            if len(output_per_step)>0:
                # print(output_per_step)
                output_mean = np.mean(output_per_step)
                std_mean = np.std(output_per_step)

                output.append(output_mean)
                output_std.append(std_mean)
                output_per_step=[]

            input1.append(_input)
            continue
        else: continue

output_mean = np.mean(output_per_step)
std_mean = np.std(output_per_step)

output.append(output_mean)
output_std.append(std_mean)

# print(output,input)

#convert to np.array
input1, output, output_std = np.array(input1), np.array(output), np.array(output_std)
ratio_out_in, ratio_out_in_std= [],[]

print(output)
print(input1)

for i in range(len(input1)):
    ratio_out_in.append(output[i]/input1[i])
    ratio_out_in_std.append(output_std[i]/input1[i])

print('ratio = ', ratio_out_in)
print('std = ', ratio_out_in_std)

# # save values to file
#
if args.out_name is None: args.out_name = args.in_name + '_ratio'
savefile = open(args.out_path+args.out_name+'.csv','w')
#savefile.write("Calibration %s"%det_name) # det_name contains linebreak
for v, e, inp in zip(ratio_out_in, ratio_out_in_std, input1): savefile.write("%f, %f, %f\n"%(v,e, inp))
savefile.close()
print('saved voltage values to %s'%args.out_path+args.out_name+'.csv')
#
#
#
#
# plot
fontsize = 20
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
#plt.title('Detector: %s'%det_name, size=fontsize)

plt.errorbar(input1, ratio_out_in, yerr = ratio_out_in_std, fmt='o') # weird x y choice on purpose
#plt.grid(True, which="both")
plt.xlabel(r'Input[mV]', size=fontsize)
plt.ylabel('Ratio [Output/Input]', size=fontsize)
plt.title(args.in_name, size=fontsize)

# close the plot when pressing a key
plt.draw()
plt.savefig('%s_ratio.png'%args.in_name)
plt.pause(1)
input('press any key to close')
plt.close(fig)

#   plt.close('all')

# print('goodbye')
