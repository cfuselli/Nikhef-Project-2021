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

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read('setup.ini')
config_detectors = list(config.items(section='DETECTORS'))
nLayers = int(config['INFO']['nLayers'])

grid = Grid()
for i in range(nLayers):
    layer = Layer(i)
    grid.add_layer(layer)

for el in config_detectors:
    d = Detector()
    pos = el[1].split(',')
    pos = [float(item) for item in pos]
    d.set_pos(pos)
    d.set_name(el[0])
    grid.layers[d.get_layer()].add_detector(d)
grid.info()


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

grid.remove_undefined_detectors()
grid.info()
ax = grid.plot(show=True)


file = open('output_data.txt', "w")
file.write('# count detector.name time adc volt timediff\n')

print("\nStart reading data\n")


# Don't consider the first two seconds of data
t_end = time.time() + 2
while time.time() < t_end:
    for detector in grid.get_detector_list():
        if detector.port.inWaiting():
            data = detector.readline()

while True:
    for detector in grid.get_detector_list():
        if detector.port.inWaiting():
            now = datetime.now()
            data = detector.readline()

            try:
                timediff = now - stack.peek().time
                timediff = timediff.total_seconds()
            except:
                timediff = 10

            signal = Signal(data, detector, now, timediff)
            stack.push(signal)

            if timediff < 0.05 and stack.isEmpty() is False and detector is not stack.peek(1).detector:
                if stack.peek(1).muon:
                    if detector is not stack.detectors:
                        signal.set_muon()
                        signal.write(file)
                        print(signal.info())


                else:
                    file.write('>>>> Start muon\n')
                    print('>>>> Start muon')
                    stack.peek(1).set_muon()
                    signal.set_muon()

                    stack.peek(1).write(file)
                    signal.write(file)

                    print(signal.info())
                    print(stack.peek(1).info())
