#!/usr/bin/env python
#############################################
# SerialCom 
# Base serial communication class
#
# Carlos.Solans@cern.ch
# Abhishek.Sharma@cern.ch
# February 2016
#############################################

import io
import serial
import base64

class SerialCom:
    com = None
    sio = None
    trm = None
    def __init__(self,
                 portname,
                 baudrate=19200,
                 terminator="\r\n",
                 timeout=0.5,
                 bytesize=8,
                 parity='N',
                 stopbits=1,
                 xonxoff=False,
                 dtr=True,
                 rts=True,
                 errors=None):
        self.com = serial.Serial(port=portname,
                                 baudrate=baudrate,
                                 timeout=timeout,
                                 bytesize=bytesize,
                                 parity=parity,
                                 stopbits=stopbits,
                                 xonxoff=xonxoff)
        self.com.dtr=dtr
        self.com.rts=rts
        self.errors = errors
        self.trm = terminator
        self.verbose = False
        if portname!=None: self.init()
        pass

    def setVerbose(self,verbose):
        self.verbose = verbose
        pass

    def init(self):
        if self.errors==None:
            self.sio = io.TextIOWrapper(io.BufferedRWPair(self.com,self.com),"utf-8")
            pass
        else:
            self.sio = io.TextIOWrapper(io.BufferedRWPair(self.com,self.com),
                                        errors=self.errors)
            pass
        pass
    
    def open(self):
        if not self.com.is_open: self.com.open()
        self.init()
        pass

    def close(self):
        self.com.close()
        pass

    def getSerial(self):
        return self.com
    
    def read(self):
        s=None
        s=self.sio.reconfigure( errors='replace', newline='\n',line_buffering=True, write_through=True)
        s=self.sio.readline()
        return s.replace('\n','').replace('\r','')

    def write(self,cmd):
        cmd=cmd#.replace("\r","").replace("\n","")
        if self.verbose: print ("SerialCom::write: %s" %cmd)
        raw_cmd=bytes(cmd+self.trm, encoding='utf-8')  # not used, should be commented out
        self.sio.write(cmd+self.trm)#.decode('utf-8'))
        self.sio.flush()
        pass

    def writeAndRead(self,cmd):
        self.write(cmd)
        return self.read()

    def rawWriteAndRead(self,cmd):
        if self.verbose: print ("SerialCom::write: %s" %cmd)
        self.sio.write(unicode(cmd.decode().encode('utf-8')))
        self.sio.flush()
        try:
            s=self.sio.readline()
            if self.verbose: print ("SerialCom::read : %s" % s)
            pass
        except:
            if self.verbose: print ("SerialCom::read : TIMEOUT")
            pass
        return s

