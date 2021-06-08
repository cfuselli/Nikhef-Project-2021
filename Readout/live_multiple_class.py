import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, glob
import time
import configparser
import serial.tools.list_ports

from Readout.cosmic_watch.class_module import Grid, Detector, Signal, Layer, Stack
from Readout.cosmic_watch.class_module import serial_ports

print(" ")

stack = Stack(2)

# read config from setup.ini (READ README.md)
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read('setup.ini')
config_detectors = list(config.items(section='DETECTORS'))
nLayers = int(config['INFO']['nLayers'])

# creating a grid, adding the layers (probably 3)
grid = Grid()
for i in range(nLayers):
    layer = Layer(i)
    grid.add_layer(layer)

# creating the detectors (but still not connected to ports)
for el in config_detectors:
    d = Detector()
    pos = el[1].split(',')
    pos = [float(item) for item in pos]
    d.set_pos(pos)
    d.set_name(el[0])
    grid.layers[d.get_layer()].add_detector(d)
grid.info()


# connect detectors and ports based on name
port_name_list = serial_ports()
for port_name in port_name_list:
    conn = serial.Serial(port=port_name, baudrate=9600, timeout=None)
    while True:
        if conn.inWaiting():
            data = conn.readline().replace(b'\r\n', b'').decode('utf-8').split(',')
            for d in grid.get_detector_list():
                if d.name == data[0].lstrip():
                    d.set_port(port_name, conn)
                    d.set_type(data[1].lstrip())
                    print('Connected to detector: ', d.name)
                    break
            break


# remove detectors for which we did not find a port
grid.remove_undefined_detectors()

grid.info()
ax = grid.plot(show=True)


file = open('output_data.txt', "w")
file.write('# count detector.name time adc volt timediff\n')

print("\nStart reading data\n")


# Don't consider the first two seconds of data
# Not sure this is smart but made sense at some point
t_end = time.time() + 2
while time.time() < t_end:
    for detector in grid.get_detector_list():
        if detector.port.inWaiting():
            data = detector.readline()

# Start loop of data taking
while True:
    for detector in grid.get_detector_list():
        if detector.port.inWaiting():
            now = datetime.now()
            data = detector.readline()

            # how much time from the last signal?
            try:
                timediff = now - stack.peek().time
                timediff = timediff.total_seconds()
            except:
                # if stack is empty...
                timediff = 10

            # create a signal
            signal = Signal(data, detector, now, timediff)
            stack.push(signal)

            # if last signal is close in time, then maybe it's a muon
            # we also do not want a muon to pass two times in the same detector
            if timediff < 0.05 and stack.isEmpty() is False and detector is not stack.peek(1).detector:

                # if the signal before was targeted as muon, then this is still part of the same muon
                if stack.peek(1).muon:
                    if detector is not stack.detectors:
                        signal.set_muon()
                        signal.write(file)
                        print(signal.info())

                # if not, we create a 'new muon signal'
                else:
                    file.write('>>>> Start muon\n')
                    print('>>>> Start muon')
                    stack.peek(1).set_muon()
                    signal.set_muon()

                    stack.peek(1).write(file)
                    signal.write(file)

                    print(signal.info())
                    print(stack.peek(1).info())
