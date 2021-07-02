# class to read in calibration constants and convert ADC to mV
# 
# @haslbeck
# 25 June

import io
import numpy as np
import csv

import matplotlib.pyplot as plt

class Converter():
    """ convert ADC to mV using calibration data extracted by polynomial fit """
    
    def __init__(self, rfile = 'All_Fit_Params.csv', path = '../../Calibration/data/final_calib/',\
                detectors = ['Carlo','Florian','BenRevival','Franko','Niels',\
                             'M', 'Noor', 'rens', 'MattiaCosmicWatch', 'Cecile','Oline',\
                             'dummy'
                             ],
                rank = 11, header = 2, verbose = True
                ):
        """ save calibration constants per detector """
                
        # dict to store constants
        self.constants = {}
        for detector in detectors: self.constants[detector] = [] # ignore par errors
        
        # read in file
        detector = None
        if rfile[-4:] != '.csv': rfile+= '.csv'
        if path[-1] != '/': path+= '/'
    
        with open(path + rfile, encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(reader):
            
                if i < header : continue # skip header
                if len(line) == 0: continue # skip empty lines
                
                if str(line[0]) in detectors: detector = str(line[0])
                else: 
                    if float(line[0]) == 0. or float(line[0]) == -0.: continue
                    self.constants[detector].append(float(line[0]))
                pass
                
        # convert tp np array 
        for (detector, vals) in self.constants.items(): self.constants[detector] = np.asarray(vals,'f')
        
        # feedback
        if verbose:
            for (detector, vals) in self.constants.items(): print(detector, vals)

    def adc2mv(self, detector, adc):
        """ convert adc to mV using by evaluating the polynomial fit function """
        coeff = self.constants[detector]
        #coeff = np.flip(coeff)
        mv = np.polyval(coeff, adc)
        #mv  = 0.
        #for order,par in enumerate(coeff): mv+=par*np.power(adc,order)
        return mv


    
if __name__ == '__main__':
    c = Converter()
    print(c.adc2mv('Noor',159.))

    test = np.linspace(0,100,1000)
    print(c.constants["Noor"])
    #plt.figure(1)
    #plt.plot(test,c.adc2mv("Noor",test))
    #plt.yscale('log')
    #plt.show()
    #input()

    plt.figure(2)
    x = np.linspace(0,1000,1000)


    pars = [0.,0.,0.,0.,0.,-2.0000000e-06, 5.0299999e-04, -5.8260001e-02, 2.9504969e+00,1.7245186e+01]
    pars.reverse()
    print(pars)
    plt.plot(x,np.polyval(pars  , x))
    #plt.yscale('log')
    plt.show()
    input()
    



