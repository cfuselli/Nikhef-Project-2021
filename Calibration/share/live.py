import serial
import argparse
import TTi_TG5011
import time

# open connection to detector
d = serial.Serial(port='/dev/ttyUSB0',baudrate=9600, timeout = None)


while True:
    try:

        # trigger
        # read the data (byte) as utf8
        data = d.readline().replace(b'\r\n',b'').decode('utf-8')
        print(data)
        
    # halfly graceful exit... 
    except KeyboardInterrupt:
        break

