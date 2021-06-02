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


    t, voltage, peak, t_peak = [],[],[],[] 
    if "NewFile" in fname: voltage2, peak2, t_peak2 = [] , [] , []
    with open(fname ) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter= ',')
        for i,row in enumerate(csv_reader): 
            if "NewFile" in fname:
                if i<2: continue  # skip header
                t.append(float(row[0])*1e9)
                voltage.append(float(row[2]))
                #voltage2.append(float(row[2]))
            else:
                t.append(float(row[3])*10**9)
                voltage.append(float(row[4]))
            pass

        index_max = voltage.index(max(voltage))     #cut all data before peak (~t=0)
        peak = voltage[index_max:]
        t_peak = t[index_max:]

        timemax = 2000
        for i,t in enumerate(reversed(t_peak)): 
            if t < timemax: 
                index_tmax = t
                break
        peak = peak[:-i]
        t_peak = t_peak[:-i]
    return t_peak, peak



def exp_fit(xdata,ydata,p0=np.array([1e-4,1e-3]),plot=False):
    """ fit exp. to signal to extract lambda 
    p0 is inital guess """
    
    xdata = np.array(xdata) # covert to numpy array
    ydata = np.array(ydata)
    
    # fit
    def fit_func(x,a,b):
        return a*np.exp(-b*x)    
    popt, pcov = curve_fit(fit_func, xdata, ydata , p0 = p0)
    a , aerr = popt[0], pcov[0][0]
    l , lerr = popt[1], pcov[1][1]
    if plot: 

        plt.plot(xdata, fit_func(xdata, *popt),
                 label='$a\cdot exp(-\lambda x)$\na: %.2e$\pm$%.2e\n$\lambda$: %.2e $\pm$ %.2e'%(a,aerr,l,lerr),
                 color='r',linewidth = 2)
        plt.legend()
    print(l, lerr, '          ', a, aerr)
    return l, lerr, a, aerr



def plot_signal(xdata, ydata):
    fig = plt.figure()       
    plt.plot(xdata,ydata,'k', marker = '.', linestyle = 'None')
    plt.title(r'Muon Signal',fontsize=10)
    plt.xlabel("time (ns)",fontsize=10)
    plt.ylabel("U(V)",fontsize=10)
    plt.tick_params(labelsize=10)
    plt.grid()
    plt.legend()
    #plt.show()
    return fig


def analysis(lambdas,lambda_errs, ampl, ampl_errs):
    """ Plot histogram of lambdas
        Plot lambda vs peak voltage to check for correlations"""
    
    l, lerrs = np.array(lambdas), np.array(lambda_errs)
    a, aerrs = np.array(ampl), np.array(ampl_errs)
    lerr_mean = sum(i*i for i in lerrs)

    plt.figure()
    plt.hist(l,bins=10,label='mean %.3e'%l.mean())
    plt.ylabel('Entries')
    plt.xlabel(r'$\lambda$')

    print(l)
    
    plt.figure()
    plt.errorbar(a,l, xerr=aerrs, yerr=lerrs,fmt='o')
    #plt.ylim(0.0025, 0.0050)
    plt.ylabel(r'$\lambda$')
    plt.xlabel('V')
    
    print(r'The mean lambda is: ' , l.mean() , r' +/- ', lerr_mean)
    return l.mean()

def plot_multiple_waves(fpath, number_of_measurements=10, PLOT=False, Analysis=True, filename = 'lambdas.txt' ):
    
    ls, lerrs, a_s, aerrs = [],[],[],[]
    fnames = []
    
    start, stop = 0, number_of_measurements

    print(stop)
    
    for i in range(start,stop):
        print('here', i)
        if args.f is None: fname = 'TEK000%i'%i if i < 10 else 'TEK00%i'%i
        else: fname = '%s%i'%(args.f,i)
        print(fname)
        fnames.append(fname)
        fname = fpath + '/' + fname + '.csv'
        time, voltage = get_data(fname)
        if PLOT: plot_signal(time,voltage)
            
        l, lerr, a , aerr = exp_fit(time,voltage,p0=np.array([max(voltage),1e-3]),plot=PLOT)
        ls.append(l)
        lerrs.append(lerr)
        a_s.append(a)
        aerrs.append(aerr)
    
    if Analysis:
        analysis(ls,lerrs,a_s,aerrs)    
    
        # save the calibration constants to file
        with open(filename, "w") as fwrite:
            fwrite.write('Filename, Lambda, Lambda error, Amplitude, Amplitude error\n')
            for i,l in enumerate(ls):
                fwrite.write('%s, %s, %s, %s, %s\n'%(fnames[i],l,lerrs[i], a_s[i], aerrs[i]))
            
    print('processed %s'%fnames)
    
    return 0

#Do not plot single waveforms and fits, only analise
print(args.n)
#plot_multiple_waves(path_to_files,
#                    number_of_measurements=args.n, PLOT=True) 

#Do not analyse, only plot single waveforms and fits

plot_multiple_waves(path_to_files,                  
                    number_of_measurements=args.n,
                    PLOT=True, 
                    Analysis=True) 


# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')


print('goodbye')

