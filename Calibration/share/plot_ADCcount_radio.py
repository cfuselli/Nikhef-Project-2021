# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:09:25 2021
Analysis of detector signals
@NookKosterUVa, @haslbeck
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import argparse
import csv




parser = argparse.ArgumentParser()
parser.add_argument('-f',type=str,default = None, help='name patter csv')
parser.add_argument('-p',type=str,default='../data/',help='path to txt file w muon signal')
parser.add_argument('-n',type=int,default=1,help='number of files')
args = parser.parse_args()

path_to_files = args.p
plt.close('all')

 
def get_data(fname):
    """ Get data (voltage and time measurements) from csv-file: start at peak, just after t=0 """

    print('get', fname)


    adc = []
    fpath = "../data/"
    file_loc = (fpath+fname)
    print (file_loc)
    with open(file_loc) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter= ',')
        for i,row in enumerate(csv_reader):
            if i<6: continue  # skip header
            adc.append(float(row[2]))
            pass

        index_max = adc.index(max(adc))     #cut all data before peak (~t=0)
        peak = adc[index_max:]
    fig = plt.figure(figsize=(12,7))
    plt.xlabel("ADC")
    plt.title("ADC count for radioactive source")
    plt.hist(adc)
    plt.savefig("adc_radioactive_histogram.png")
    return peak, adc_hist
