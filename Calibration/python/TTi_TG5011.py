#!/usr/bin/env python
#############################################
# TTI 50MHz Function/Arbitrary/Pulse Generator
# Model TG5011
# based on TTi.py
# April 2021
# Flo
#############################################

import time
from SerialCom import SerialCom


class TTi_TG5011:
    """ python class for TTI 50MHz Function/Arbitrary/Pulse Generator, model TG5011(A)
        based on PySerialComm
    """
    sc = None
    def __init__(self,portname,baudrate=19200,timeout=0):
        self.sc = SerialCom(portname, baudrate=baudrate, xonxoff=False, timeout=timeout)
    
    def __del__(self):
        self.enableOutput('OFF')
        print('Deconstructor disabled output. Goodbye.')


    def setVerbose(self, enable):
        self.sc.setVerbose(enable)
    
    def setLocal(self):
        """ enable local operation and unlock keyboard """
        self.sc.write("LOCAL")
        
    def beep(self): 
        self.sc.write("BEEP")
        
    """ * * * * * * * * * * * * * * * * 
        continous carrier wave commands 
        * * * * * * * * * * * * * * * *
    """
    def setWaveType(self, wave):
        """ output wave of type *waves* """
        waves = ['SINE', 'SQUARE', 'RAMP', 'TRIANG', 'PULSE', 'NOISE']
        if wave not in waves: 
            print("%s not available in %s"%(wave,waves))
            return False
        self.sc.write("WAVE %s"%wave)

    def setFrequency(self, hertz):
        """ frequency float [hertz] for continous carrier (sine) """
        self.sc.write("FREQ %e"%hertz)
        
    def setAmplitudeUnit(self,unit):
        units = ['VPP', 'VRMS', 'DBM']
        if unit not in units:
            print("%s not available in %s"%(unit,units))
            return False
        self.sc.write("AMPUNIT %s"%unit)
    
    def setAmplitude(self, ampl):
        """ amplitude in units as specified by setAmplitudeUnit """
        self.sc.write("AMPL %f"%ampl)

    def setPhase(self, phase):
        """ phase in deg """
        self.sc.write("PHASE %f"%phase)
    
    def enableOutput(self, output):
        outputs = ['ON','OFF','NORMAL',"INVERT"]
        if output not in outputs:
            print("%s not available in %s"%(output,outputs))
            return False
        self.sc.write("OUTPUT %s"%output)
        
    def setOutputLoad(self, ohm):
        """ Set the output load for amplitude and dc offset entries  """
        ohm_range = [1,10000]
        if ohm >=1 and ohm <= 10000: self.sc.write("ZLOAD %i"%ohm)
        else: 
            print("%i out of range [1,10000] Ohm")
            return False      
    
    def syncType(self, synctype):
        """ set the sync output type """
        types = ['AUTO', 'CARRIER', 'MODULATION', 'SWEEP', 'BURST', 'TRIGGER']
        if synctype not in types:
            print("%s not available in %s"%(synctype,types))
            return False
        self.sc.write("SYNCTYPE %s"%synctype)

    def syncOut(self, output):
        """ set sync output ON or OFF """
        self.sc.write("SYNCOUT %s"%output)


    """ * * * * * * * * * * * * * * * * 
        arbitray wave form commands 
        * * * * * * * * * * * * * * * *
    """
    def setArbWaveform(self, name):
        """ set output waveform to *types* or *username* """
        types = ['DC', 'SINC', 'EXPRISE', 'LOGRISE', 'RAMPUP', 'RAMPDN', 'TRIANG', 'SQUARE',\
                 'ARB1', 'ARB2', 'ARB3', 'ARB4']
        if name not in types: print('%s not in %s, make sure %s is defined. Proceed anyway.'%(name,types,name))  
        self.sc.write("ARBLOAD %s"%name)

    """ * * * * * * * * * * * * * * * * 
        burst mode commands 
        * * * * * * * * * * * * * * * *
    """
    def setBurstCount(self, count):
        """ set the burst count"""
        self.sc.write('BSTCOUNT %i'%count)

    def burst(self, mode):
        """ select burst type"""
        modes = ['OFF', 'NCYC', 'GATED', 'INFINITE']
        if mode not in modes:
            print("%s not available in %s"%(mode,modes))
            return False
        self.sc.write('BST %s'%mode)

    def setBurstPhase(self, degree):
        self.sc.write("BSTPHASE %f"%degree)

    def setBurstPeriod(self, seconds):
        self.sc.write("BSTPER %f"%seconds)


    """ * * * * * * * * * * * * * * * * 
        debugging mode commands 
        * * * * * * * * * * * * * * * *
    """
    def write(self,msg):
        """ generic write, debugging tool """
        self.sc.write(msg)
   
