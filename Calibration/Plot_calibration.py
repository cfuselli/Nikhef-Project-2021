# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:23:58 2021

@author: NoorKoster
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker


filename = 'C:/Users/NoorK/OneDrive/Documenten/Studie/Master/JAAR_1/Nikhef_Project/git/Nikhef-Project-2021/Calibration/Signal_Calibration/data/first_calibration_10steps.txt'                                               #datafile .txt you want to analyse
det_name = 'Noor'
fsize = 20
plt.close('all')

data_volt, volt, data, err = [], [],[], []

with open(filename) as f_in: 
    for line in f_in:
        if line[0] =='#' or str(line.split()[0]) == det_name: continue
        
        ADC = float(line.split()[2])
        trigger = str(line.split()[0])
        
        if trigger=='SET': 
            volt.append(ADC)
            mean_per_volt = np.mean(data_volt)
            std = np.std(data_volt)
            data.append(mean_per_volt)
            err.append(std)
            data_volt = []
            continue
            
        
        if trigger!='SET':
            data_volt.append(ADC)
            
mV = [i * 10**3 for i in volt]

plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fsize)
plt.title('Detector: %s'%det_name, size=fsize)
plt.errorbar(data,mV, xerr = err, fmt='o')
plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fsize)
plt.xlabel('Measured ADC value [0-1023]', size=fsize)    
            

    
    
    
    
    
    