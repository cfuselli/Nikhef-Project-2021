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
import regex as re

from Readout.cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
from Readout.cosmic_watch.class_module import serial_ports

folder_name = 'output_2021-06-14_18-01'
file = open(folder_name + '/grid_setup.txt', 'r')

grid = Grid()

for i, line in enumerate(file.readlines()):
    if i == 0:
        print('Data from: ', line)
    else:
        if len(line) < 3: # there should be one blank line
            break
        d = Detector()
        line = line.replace('[', '')
        line = line.replace('\n', '')
        line = line.replace(',', '')
        line = line.replace(']', '').split(' ')
        pos = [float(line[2]), float(line[3]), int(float(line[4]))]
        d.set_pos(pos)
        d.set_name(line[6])
        d.set_type(line[1])
        grid.detectors.append(d)

print(grid.info())
grid.plot(show=False)

file.close()

file_number = 0
file = open(folder_name + '/output_data%i.txt' % file_number, "r")
header = file.readline()
print(header)

muon = Muon()

while True:
    if os.path.exists(folder_name + '/output_data%i.txt' % (file_number + 1)):
        file.close()
        file_number += 1
        file = open(folder_name + '/output_data%i.txt' % file_number, "r")
        header = file.readline()
        print('Reading file ' + folder_name + '/output_data%i.txt' % file_number)
        continue

    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        while line != '\n':
            line = line.replace('\n', '')
            lsplit = line.split(' ')
            det = 0
            for d in grid.detectors:
                if d.name == lsplit[-1]:
                    det = d
                    break
            if det == 0:
                exit('Unknown detector found')

            signal = Signal(det)
            signal.adc = int(lsplit[1])
            signal.volt = float(lsplit[2])
            signal.temp = float(lsplit[3])
            datetime_object = datetime.strptime(lsplit[5] + ' ' + lsplit[6], '%Y-%m-%d %H:%M:%S.%f')
            signal.time = datetime_object
            signal.timediff = float(lsplit[4])
            muon.add_signal(signal)
            line = file.readline()

        print(' ----> Muon')
        muon.print()
        muon.reset()




'''

            def __init__(self, data, detector, time, timediff):
                data = data.split(' ')
                #   0               1                   2
                # count + " [" + countslave + "] " + time_stamp + " " +
                #  3            4                       5
                # adc+ " " + sipm_voltage + " " + measurement_deadtime+ " " +
                #   6                       7                   8                   9
                # temperatureC + " " + MASTER_SLAVE + " " + keep_pulse + " " + detector_name);
                self.detector = detector
                self.time = time
                self.timediff = timediff
                self.adc = data[3]
                self.volt = data[4]
                self.temp = data[6]
                self.muon = False
                self.count = int(data[0])
                detector.count += 1

'''