import serial # make sure to pip3 install pyserial (NOT pip3 install serial !)
import time
import glob
import sys
import os
import os.path
import signal
from datetime import datetime
from multiprocessing import Process

import numpy as np
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import multiprocessing
import math
import random
import _thread as thread # instead of import thread in python3
from serial import Serial

'''
This is a Websocket server that forwards signals from the detector to any client connected.
It requires Tornado python library to work properly.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
Run it with `python detector-server.py`
Written by Pawel Przewlocki (pawel.przewlocki@ncbj.gov.pl).
Based on http://fabacademy.org/archives/2015/doc/WebSocketConsole.html
''' 

def print_help1():
    print('\n===================== HELP =======================')
    print('This code looks through the serial ports. ')
    print('You can select multiple ports with by separating the port number with commas.')
    print('You must select which port contains the Arduino.\n')
    print('If you have problems, check the following:')
    print('1. Is your Arduino connected to the serial USB port?\n')
    print('2. Check that you have the correct drivers installed:\n')
    print('\tMacOS: CH340g driver (try: https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver)')
    print('\tWindows: no dirver needed')
    print('\tLinux: no driver needed')


clients = [] ## list of clients connected
queue = multiprocessing.Queue() #queue for events forwarded from the device

class DataCollectionProcess(multiprocessing.Process):
    def __init__(self, queue):
        #multiprocessing.Process.__init__(self)
        self.queue = queue
        self.comport = serial.Serial(port_name_list[0]) # open the COM Port
        self.comport.baudrate = 9600          # set Baud rate
        self.comport.bytesize = 8             # Number of data bits = 8
        self.comport.parity   = 'N'           # No parity
        self.comport.stopbits = 1 

    def close(self):
        self.comport.close()
        
    def nextTime(self, rate):
        return -math.log(1.0 - random.random()) / rate

def RUN(bg):
    print('Running...')
    while True:
        data = bg.comport.readline()
        bg.queue.put(str(datetime.now())+" "+data)
    
class WSHandler(tornado.websocket.WebSocketHandler):
    def __init__ (self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)
        self.sending = False

    def open(self):
        print('New connection opened from ' + self.request.remote_ip)
        clients.append(self)
        print('%d clients connected' % len(clients))
      
    def on_message(self, message):
        print('message received:  %s' % message)
        if message == 'StartData':
            self.sending = True
        if message == 'StopData':
            self.sending = False
 
    def on_close(self):
        self.sending = False
        clients.remove(self)
        print('Connection closed from ' + self.request.remote_ip)
        print('%d clients connected' % len(clients))
 
    def check_origin(self, origin):
        return True

def checkQueue():
    while not queue.empty():
        message = queue.get()
        ##sys.stdout.write('#')
        for client in clients:
            if client.sending:
                client.write_message(message)
 

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    ComPort.close() # TODO throws error message: has no .close()
    file.close() 
    sys.exit(0)
    
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
        sys.exit(0)
    result = []
    for port in ports:
        try: 
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#If the Arduino is not recognized by your MAC, make sure you have
#   installed the drivers for the Arduino (CH340g driver). Windows and Linux don't need it.

print('\n             Welcome to:   ')
print('CosmicWatch: The Desktop Muon Detector\n')

print("Record data on the computer")


#mode = str(input("\nSelected operation: ")) 
#mode = str(input("\nSelected operation: ")) # change to py3
mode = 1
port_list = serial_ports()

print('Available serial ports:')
for i in range(len(port_list)):
    print('['+str(i+1)+'] ' + str(port_list[i]))

ArduinoPort = input("Selected Arduino port (comma separated): ")

ArduinoPort = ArduinoPort.split(',')
nDetectors = len(ArduinoPort)
port_name_list = []

for i in range(len(ArduinoPort)):
    port_name_list.append(str(port_list[int(ArduinoPort[i])-1]))

print("The selected port(s) is(are): ")
for i in range(nDetectors):	 
    print('\t['+str(ArduinoPort[i])+']' +port_name_list[i])


if mode == 1:
    cwd = os.getcwd()
    fname = input("Enter file name (default: "+cwd+"/CW_data.txt):")

    detector_name_list = []

    if fname == '':
        fname = cwd+"/CW_data.txt"
    
    # TODO: add .txt automatically

    print('Saving data to: '+fname)

    ComPort_list = np.ones(nDetectors)
    for i in range(nDetectors):
        signal.signal(signal.SIGINT, signal_handler)
        globals()['Det%s' % str(i)] = serial.Serial(str(port_name_list[i]))
        globals()['Det%s' % str(i)].baudrate = 9600    
        globals()['Det%s' % str(i)].bytesize = 8             # Number of data bits = 8
        globals()['Det%s' % str(i)].parity   = 'N'           # No parity
        globals()['Det%s' % str(i)].stopbits = 1 

        time.sleep(1)
        #globals()['Det%s' % str(i)].write('write')  

        counter = 0

        header1 = globals()['Det%s' % str(i)].readline()     # Wait and read data 

        if b'SD initialization failed' in header1: # header is a byte literal
            print('...SDCard.ino detected.')
            print('...SDcard initialization failed.')
            # This happens if the SDCard.ino is uploaded but it doesn't see an sdcard.
            header1a = globals()['Det%s' % str(i)].readline()
            header1 = globals()['Det%s' % str(i)].readline()
        
        if b'CosmicWatchDetector' in header1:
            print('...SDCard.ino code detected.')
            print('...SDcard intialized correctly.')
            # This happens if the SDCar.ino is uploaded and it sees an sdcard.
            header1a = globals()['Det%s' % str(i)].readline()
            globals()['Det%s' % str(i)].write('write') 
            header1b = globals()['Det%s' % str(i)].readline()
            header1 = globals()['Det%s' % str(i)].readline()
            #header1 = globals()['Det%s' % str(i)].readline()
            
        header2 = globals()['Det%s' % str(i)].readline()     # Wait and read data 
        header3 = globals()['Det%s' % str(i)].readline()     # Wait and read data 
        header4 = globals()['Det%s' % str(i)].readline()     # Wait and read data 
        header5 = globals()['Det%s' % str(i)].readline()     # Wait and read data 

        #det_name = globals()['Det%s' % str(i)].readline().replace('\r\n','')
        det_name = globals()['Det%s' % str(i)].readline().replace(b'\r\n',b'') # change to byte literal
        #print(det_name)
        #if 'Device ID: ' in det_name:
        if b'Device ID: ' in det_name:
            det_name = det_name.split('Device ID: ')[-1]
        detector_name_list.append(det_name)    # Wait and read data 


    #file = open(fname, "w",0)
    file = open(fname, "wt") # py3
    file.write(header1.decode('utf-8'))
    file.write(header2.decode('utf-8'))
    file.write(header3.decode('utf-8'))
    file.write(header4.decode('utf-8'))
    file.write(header5.decode('utf-8'))

    string_of_names = ''
    print("\n-- Detector Names --")
    print(detector_name_list)
    for i in range(len(detector_name_list)):
        print(detector_name_list[i].decode('utf-8'))
        if b'\xff' in detector_name_list[i] or b'?' in detector_name_list[i] :
            print('--- Error ---')
            print('You should name your CosmicWatch Detector first.')
            print('Simply change the DetName variable in the Naming.ino script,')
            print('and upload the code to your Arduino.')
            print('Exiting ...')

    print("\nTaking data ...")
    print("Press ctl+c to terminate process")

    if nDetectors>1:
        for i in range(nDetectors):
            string_of_names += detector_name_list[i].decode('utf-8') +', '
    else:
        string_of_names+=detector_name_list[0].decode('utf-8')

    print(string_of_names)
    file.write('Device ID(s): '+string_of_names)
    file.write('\n')
    file.flush()
    #detector_name = ComPort.readline()    # Wait and read data 
    #file.write("Device ID: "+str(detector_name))

    while True:
        for i in range(nDetectors):
            if globals()['Det%s' % str(i)].inWaiting():
                data = globals()['Det%s' % str(i)].readline().replace(b'\r\n',b'')    # Wait and read data
                data = data.decode('utf-8')
                datawrite = str(datetime.now())+" "+data+" "+detector_name_list[i].decode('utf-8')+'\n'
                file.write(datawrite)
                file.flush()
                print(data)
                print(datawrite)
                globals()['Det%s' % str(i)].write(b'got-it')
                pass
            pass
    for i in range(nDetectors):
        globals()['Det%s' % str(i)].close()     
    file.close()


