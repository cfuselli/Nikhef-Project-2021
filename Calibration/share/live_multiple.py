import serial
import argparse
# import TTi_TG5011
import datetime
from datetime import datetime
import sys, glob


class Detector:
    def __init__(self, serialport):
        self.port = serial.Serial(port=serialport,baudrate=9600, timeout = None)

    def set_layer(self, layer_num):
        self.layer = layer_num



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
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


port_list = serial_ports()

print('Available serial ports:')
for i in range(len(port_list)):
    print('['+str(i+1)+'] ' + str(port_list[i]))

ArduinoPort = input("Select Arduino port (comma separated): ")
ArduinoPort = ArduinoPort.split(',')
nDetectors = len(ArduinoPort)
port_name_list = []
for i in range(len(ArduinoPort)):
    port_name_list.append(str(port_list[int(ArduinoPort[i])-1]))

print("The selected port(s) is(are): ")
for i in range(nDetectors):
    print('\t['+str(ArduinoPort[i])+']' +port_name_list[i])
print(" ")

ports = []
for port_name in port_name_list:
# open connection to detector
    ports.append(serial.Serial(port=port_name,baudrate=9600, timeout = None))

for i, port in enumerate(ports):
    print("\n", port_name_list[i])
    headcount = 0
    while headcount < 6:
        if port.inWaiting():
            headcount += 1
            data = port.readline().replace(b'\r\n', b'').decode('utf-8')
            print(data)

print("\nStart reading data\n")

a = datetime.now()
while True:
    for port in ports:
        if port.inWaiting():
            # trigger
            # read the data (byte) as utf8
            data = port.readline().replace(b'\r\n',b'').decode('utf-8')
            b = datetime.now()
            timediff = b - a
            a = datetime.now()
            together = ""
            if timediff.total_seconds() < 0.05:
                together = " --- With the previous one --- "
            print(data, a.strftime('%Y-%m-%d %H:%M:%S.%f'), timediff.total_seconds(), together)
