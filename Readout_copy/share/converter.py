# class to read in calibration constants and convert ADC to mV
# 
# @haslbeck
# 25 June

import io
import numpy as np
import csv

class Converter():
    """ convert ADC to mV using calibration data extracted by polynomial fit """
    
    def __init__(self, rfile = 'test_calib_const.csv', path = '../../Calibration/data/',\
                detectors = ['Carlo','Florian','BenRevival','Franko','Niels',\
                            'M', 'Noor', 'rens', 'MattiaCosmicWatch', 'Cecile', 'ZenBenMaster'],
                rank = 11, header = 1, verbose = False
                ):
        """ save calibration constants per detector """
                
        # dict to store constants
        self.constants = {}
        for detector in detectors: self.constants[detector] = [] # ignore par errors
        
        
        # read in file
        detector = None
        if rfile[-4:] != '.csv': rfile+= '.csv'
        if path[-1] != '/': path+= '/'
    
        with open(path + rfile) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(reader):
            
                if i < header : continue # skip header
                if len(line) == 0: continue # skip empty lines
                
                if str(line[0]) in detectors: detector = str(line[0])
                else: self.constants[detector].append(float(line[0]))
                pass
                
        # convert tp np array 
        for (detector, vals) in self.constants.items(): self.constants[detector] = np.asarray(vals,'f')
        
        # feedback
        if verbose:
            for (detector, vals) in self.constants.items(): print(detector, [type(val) for val in vals])

    def adc2mv(self, detector, adc):
        """ convert adc to mV using by evaluating the polynomial fit function """
        coeff = self.constants[detector]
        mv = np.polyval(coeff, adc)
        return mv


    
if __name__ == '__main__':
    c = Converter()
    print(c.adc2mv('Carlo',2))
    



