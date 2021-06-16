import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, os, shutil
import time
import configparser
import serial.tools.list_ports
import schedule
import random

# I don't know why this works on the computer of the lab but not on my MacBook (Carlo)
# from cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
# from cosmic_watch.class_module import serial_ports

from Readout.cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
from Readout.cosmic_watch.class_module import serial_ports

print(" ")

stack = Stack(2)

# read config from setup.ini (READ README.md)
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read('setup_fake.ini')
config_detectors = list(config.items(section='DETECTORS'))


grid = Grid()

# creating the detectors (but still not connected to ports)
for el in config_detectors:
    d = Detector()
    p = el[1].split(',')
    lay = int(p[0])
    pos = [float(p[1].lstrip()), float(p[2].lstrip()), float(p[3].lstrip())]
    dim = [float(p[4].lstrip()), float(p[5].lstrip()), float(p[6].lstrip())]
    d.pos = pos
    d.dimensions = dim
    d.layer = lay
    d.name = el[0]
    grid.detectors.append(d)
print(grid.info())

# connect detectors and ports based on name

print('\nGrid configuration:\n')

def sortkey(dd):
    return dd.layer


grid.detectors.sort(key=sortkey)
print(grid.info())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax = grid.plot(ax, show=False)

signals_per_file = int(config['INFO']['signals_per_file'])
signals_per_control_file = int(config['INFO']['signals_per_control_file'])

file_number = 0
control_file_number = 0

today = datetime.today()
strx = today.strftime("%Y-%m-%d_%H-%M")

folder_name = 'output_' + strx
try:
    shutil.rmtree(folder_name)
except:
    print('New folder ', folder_name, ' created')
os.makedirs(folder_name)


grid_file = open(folder_name + '/grid_setup.txt', "w")
file = open(folder_name + '/output_data%i.txt' % file_number, "w")
control_file = open(folder_name + '/output_master_control%i.txt' % file_number, "w")

grid_file.write(datetime.today().ctime() + '\n')
grid_file.write(grid.info())
grid_file.flush()

header = '# layer adc volt temp timediff time detector_muon_count detector_count detector_name\n'

file.write(header)
control_file.write(header)

muon_count = 0
signal_control_count = 0

print("\nStart reading data\n")
start = datetime.now()

# Don't consider the first two seconds of data
# Not sure this is smart but made sense at some point


layer0 = []
layer1 = []
layer2 = []

for detector in grid.detectors:
    if detector.layer == 0:
        layer0.append(detector)
    if detector.layer == 1:
        layer1.append(detector)
    elif detector.layer == 2:
        layer2.append(detector)

muon = Muon()
while True:

    signal = Signal(random.choice(layer0))
    muon.add_signal(signal)

    signal = Signal(random.choice(layer1))
    muon.add_signal(signal)

    signal = Signal(random.choice(layer2))
    muon.add_signal(signal)

    muon_count += 1
    print('-- %i Muon(s) detected --' % muon_count)
    muon.print()
    muon.write(file)

    if muon_count % signals_per_file == 0:
        file_number += 1
        file = open(folder_name + '/output_data%i.txt' % file_number, "w")
        file.write(header)
        file.flush()
        tnow = datetime.now()
        tdelta = datetime.now() - start
        grid_file.write('\n' + tnow.ctime() + '(' + str(tdelta) + ')\n')
        grid_file.write(grid.info() + '\n')
        grid_file.flush()

    muon.reset()
    time.sleep(5)