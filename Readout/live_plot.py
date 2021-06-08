# from .live_multiple_class import Grid, Detector, Layer, Signal
import serial
import argparse
# import TTi_TG5011
import datetime
from datetime import datetime
import sys, glob
import time
import configparser
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation
import os
import numpy as np

from Readout.cosmic_watch.class_module import Grid, Detector, Signal, Layer, Stack
from Readout.cosmic_watch.class_module import serial_ports

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

file = open('output_data.txt', 'r')

muons = []
muon = []
for line in file.readlines():
    line = line.lstrip()
    if line.startswith('#'):
        continue
    elif line.startswith('>>>>'):
        muons.append(muon)
        muon = []
    else:
        line = line.split(' ')
        muon.append(line)

muons.remove(muons[0])
muons.append(muon)

print('\n\n')
for m in muons:
    print('-- Muon --')
    for s in m:
        print('  ', s[0])