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
import matplotlib.animation as animation


from Readout.cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
from Readout.cosmic_watch.class_module import serial_ports

folder_name = 'output_2021-06-16_15-30'
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
        pos = [float(line[2]), float(line[3]), float(line[4])]
        dim = [float(line[5]), float(line[6]), float(line[7])]
        d.pos = pos
        d.dimensions = dim
        d.name = line[9]
        d.type = line[1]
        d.layer = int(line[0])
        grid.detectors.append(d)

print(grid.info())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ln, = plt.plot([], [], [])

def init():
    grid.plot(ax, show=False)

file.close()



muon = Muon()

def update(i):
    file_number = 0
    file = open(folder_name + '/output_data%i.txt' % file_number, "r")
    header = file.readline()
    print(header)
    if os.path.exists(folder_name + '/output_data%i.txt' % (file_number + 1)):
        file.close()
        file_number += 1
        file = open(folder_name + '/output_data%i.txt' % file_number, "r")
        header = file.readline()
        print('Reading file ' + folder_name + '/output_data%i.txt' % file_number)
        print(header)

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
                strin = 'Unknown detector found ' + lsplit[-1]
                exit(strin)

            signal = Signal(det)
            try:
                signal.adc = int(lsplit[1])
                signal.volt = float(lsplit[2])
                signal.temp = float(lsplit[3])
                datetime_object = datetime.strptime(lsplit[5] + ' ' + lsplit[6], '%Y-%m-%d %H:%M:%S.%f')
                signal.time = datetime_object
                signal.timediff = float(lsplit[4])
            except:
                print('')
            muon.add_signal(signal)
            line = file.readline()

        print(' ----> Muon')
        muon.print()
        muon.plot(ax)
        if muon.signals[1].detector.dimensions[0] > muon.signals[1].detector.dimensions[1]:
            fx = muon.signals[1].detector.pos[0]
            fy = muon.signals[2].detector.pos[1]
        else:
            fx = muon.signals[2].detector.pos[0]
            fy = muon.signals[1].detector.pos[1]
        print(muon.signals[1].detector.pos, muon.signals[2].detector.pos)
        print(muon.signals[1].detector.dimensions, muon.signals[2].detector.dimensions)
        print(fx, fy)

        muon.reset()


ani = animation.FuncAnimation(fig, update, interval=1000)
plt.show()


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