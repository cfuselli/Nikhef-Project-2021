#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: NoorKoster
@author: @haslbeck

regularised linear regression

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
parser.add_argument('-in_name',type=str,help='csv filename with ADC vs V counts')
parser.add_argument('-in_path',type=str,default='../data/',required=False, help='default ../data/')
# output file
parser.add_argument('-out_name',type=str,default=None,required=False, help='calibration constants')
parser.add_argument('-out_path',type=str,default='../data/calibration/',required=False,help='default ../data/calibration/')
parser.add_argument('-header',type=int,default=1,required=False, help='default 1')
                    
args = parser.parse_args()
if '.csv' in args.in_name: args.in_name = args.in_name[:-4]




def reg_fit_polynomial(x,t,M,rw):
  """ max. likelihood polynomial fit
  input:  array x: input vector [0,1] in n steps
          array t: data points sin + noise
          int M:   max order for the polynomial
          float rw: regularizer weight, gives importance to the penalty term
  return: array weights: fitted weigths up to order M
  """

  def designMatrix(x,M):
    """ design matrix with first colum 1s, then xi, then xi**2,...
    input:  array x: input vector
            int M:   max order for the polynomial
    return: design matrix 
    """
    cols = [np.power(x,m) for m in range(0,M+1)] # list of individual cols (arrays)
    phi = np.column_stack(tuple(cols)) # create the matrix
    return phi
  
  phi = designMatrix(x,M) # get design matrix
  # calc weight
  weights = np.linalg.inv(phi.T @ phi + rw*np.identity(np.shape(phi)[1])) @ phi.T @ t 
  return weights


def reg_fit(x,t,M,rw,color='red',verbose=False,label=None, xplot = np.linspace(0,1024,1024)):
  """ fit and plot """
  weights = reg_fit_polynomial(x,t,M,rw)
  if verbose: print("M %i rw %.0e: "%(M,rw),weights)
  
  plot_fit(weights,xplot, color, label)
  return weights
  
  
def fit_line(xplot,weights):
  """ get the fitline up to order M in weights 
  input:  array xplot: x axis steps to plot on
          array weights: fit params
  return: array fit_line
  """
  M = len(weights) # fit order
  # create a fit line array
  fitline = 0 # init as float
  for m in range(0,M): fitline += (np.power(xplot,m)*weights[m])
  return fitline


def plot_fit(weights,xplot=np.linspace(0,1024,1000), color='red',label=None):
  """ plot the fit line using the polynomial weight  """

  fitplot = fit_line(xplot,weights) # get fit plot line
  if label == None: label='fit M %i (incl. 0th)'%(len(weights)-1)
  plt.plot(xplot, np.exp(fitplot),label=label,color=color)


def chisquared(xdata,ydata,fit_weights,sigma=0.25,verbose=False):
  """ calc. chi squared with sigma defined by the noise generator
  input:  array xdata
          array ydata
          array fit_weights: polynomial fit weights of order len(fit_weights)
          float sigma = 0.25:  sigma of the data points, 0.25 by the generator
  return: float chi_sq
  """
  M = len(fit_weights) # order pol.
  pred = fit_line(xdata,weights) # predictions from fit

  chi_sq = np.sum(np.power(ydata-pred,2)) / np.power(sigma,2)
  dof = len(ydata) + M # degree of freedoms
  chi_sq_red = chi_sq/dof

  if verbose: print("pol fit order %i: chi squared reduced %.3f"%(M,chi_sq_red))
  return chi_sq_red



def fit_func(x, *coeffs):
    y = np.polyval(coeffs, x)
    return y

def polyfit(xdata,ydata,p0=None,rank=11):
    
    popt, pcov = curve_fit(fit_func, xdata, ydata, p0 = np.zeros(rank))
    
    # print out the fit params
    print('name, par, par err\n%s'%(20*'='))
    for i in range(rank): print('p%i:\t%.3f\t%.3f'%(i,popt[i],np.sqrt(pcov[i][i])))
    print(20*'=')
    
    vals , errs = [popt[i] for i in range(rank)], [np.sqrt(pcov[i][i]) for i in range(rank)]
    return vals , errs 



# read in the data
volt, adc = [], []
with open(args.in_path+args.in_name + '.csv') as csvfile:
    
    reader = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reader):
        # skip header
        if i < args.header : continue
        # FIXME: get detector name? 
        
        # read in data
        if len(line) == 1: adc.append(float(line[0]))
        # get pulsing ampltidude
        elif len(line) == 2:
            _volt = float(line[1])
            #print(_volt)
            continue
        else: continue
        volt.append(_volt)
    
print(len(volt),len(adc))

# convert to np.array
volt, adc= np.array(volt), np.array(adc)
ind = np.where(adc<1000, True, False)
volt_fit, adc_fit = volt[ind], adc[ind]


# convert to mV
mV = volt * 1e3 
mV_fit = volt_fit * 1e3

# fit
plt.figure()
plt.yscale('log')

plt.scatter(adc,mV)
vals , errs = polyfit(adc_fit, np.log(mV_fit), rank=11)
xplot = np.linspace(0,1000,1000)
plt.plot(xplot, np.exp(fit_func(xplot, *vals)), color='b', label='fit log(mv) -> rel. error %i'%len(vals))



vals , errs = polyfit(adc_fit, (mV_fit), rank=11)
xplot = np.linspace(0,1000,1000)
plt.plot(xplot, (fit_func(xplot, *vals)), color='r', label='-> abs error %i'%len(vals))

#rw = 0.0 # regularisation weight
m = 11
#weights = reg_fit(adc,mV,m,rw,color=None,label='$\lambda$ %.0e'%rw,verbose=True, xplot = xplot)

#rw = 0.1 # regularisation weight
#m = 11
#weights = reg_fit(adc,mV,m,rw,color=None,label='$\lambda$ %.0e'%rw,verbose=True, xplot = xplot)

#rw =# regularisation weight
#m = 11
#weights = reg_fit(adc,mV,m,rw,color=None,label='$\lambda$ %.0e'%rw,verbose=True, xplot = xplot)


for rw in [0.,0.1,0.01,0.001,0.0001,0.00001,0.000001]:
       weights = reg_fit(adc_fit,np.log(mV_fit),m,rw,color=None,label='$\lambda$ %.0e'%rw,verbose=True, xplot = xplot)

plt.legend()

## for m=9 calc chi2red for independent test dataset
#if m == 9:
#      csr1 = chisquared(xtrain_reg,ttrain_reg,weights) 


# save values to file
'''
if args.out_name is None: args.out_name = args.in_name + '_calibration'
savefile = open(args.out_path+args.out_name+'.csv','w')
#savefile.write("Calibration %s"%det_name) # det_name contains linebreak
for v, e in zip(vals,errs): savefile.write("%f, %f\n"%(v,e))
savefile.close()
print('saved calibration values to %s'%args.out_path+args.out_name+'.csv')




# plot
fontsize = 20 
fig = plt.figure(figsize=(12,7))
ax = plt.gca()
ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize)
ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize)
#plt.title('Detector: %s'%det_name, size=fontsize)
plt.scatter(adc,mV) # weird x y choice on purpose

xplot = np.linspace(np.min(adc),np.max(adc),1000)
#plt.plot(xplot, fit_func(xplot, *vals), color='r', label='%i'%len(vals))
#plt.yscale('log')
plt.grid(True, which="both")
plt.ylabel(r'Input pulse amplitude [mV]', size=fontsize)
plt.xlabel('Measured ADC value [0-1023]', size=fontsize)
plt.legend()

'''

# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
#plt.close(fig)

plt.close('all')

print('goodbye')
