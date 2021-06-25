# class to read in calibration constants and convert ADC to mV

import io
import numpy as np
import csv

class Converter():
    """ convert ADC to mV using calibration data """
    
    def __init__(self, rfile = 'test_calib_const.csv', path = '../../Calibration/data/',\
                detectors = ['Carlo','Florian','BenRevival','Franko','Niels',\
                            'M', 'Noor', 'rens', 'MattiaCosmicWatch', 'Cecile', 'ZenBenMaster'],
                rank = 11, header = 1, verbose = True
                ):
        """ constructor """
        # load csv file and save
        
        # dict to store constants
        self.constants = {}
        for detector in detectors: self.constants[detector] = [] # ignore par errors
  
        if rfile[-4:] != '.csv': rfile+= '.csv'
        if path[-1] != '/': path+= '/'
        
        detector = None
        with open(path + rfile) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(reader):
                # skip header
                if i < header : continue
                if len(line) == 0: continue
                
                # new line
                if str(line[0]) in detectors: detector = str(line[0])
                else: 
                    const = float(line[0])
                    
                    #print(const,type(const)) #FIXME
                    
                    self.constants[detector].append(const)
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
    



