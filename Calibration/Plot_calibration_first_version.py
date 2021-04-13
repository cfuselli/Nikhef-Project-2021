# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:23:58 2021

@author: NoorKoster
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np




ADC_per_mV, ADC, ADC_err = [], [],[]
gap=50                                                                          #gap betweeb ADC values for different voltages
filename = 'tr1_10mV_10per10.txt'                                               #datafile .txt you want to analyse
voltage = [10,20,30,40,50,60,70,80,90]                                          #in mV : Manually put all the voltages you want to measure



with open(filename) as f_in: 
    
    for i in range(18):                                                         #Skip the first lines in the file, we don't want to use them
        firstline = f_in.readline()
        
    lines = list(line for line in (l.strip() for l in f_in) if line)
#    print(lines)
    
    for i in range(len(lines)-1):                                               #Split lines and take the 4th argument, this is the ADC
       a=lines[i].split()[4]
       b = lines[i+1].split()[4]
       
       if int(b) < int(a)+gap:                                                  #Group together all ADCs from same voltage. If your gaps are smaller than 50 inbetween, change the gap!
               ADC_per_mV.append(int(a))
               
       else:
           mean_ADC_per_mV = sum(ADC_per_mV)/len(ADC_per_mV)                    #Determine mean ADC value per voltage
           std = np.std(ADC_per_mV)                                             #Determine standard deviation 
           ADC.append(mean_ADC_per_mV)
           ADC_err.append(std)
           ADC_per_mV = []
              
       
print(ADC)
#print(ADC_err)

#Make a plot. 
plt.figure()
plt.errorbar(voltage,ADC,ADC_err,0,'none')
plt.scatter(voltage,ADC)
plt.title("Callibration")

  