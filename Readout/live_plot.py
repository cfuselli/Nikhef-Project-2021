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

folder_name = 'output_2021-06-16_16-31'
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

#def init():
grid.plot(ax, show=False)

file.close()

oldname = 'ciao'


muon = Muon()

file_number = 0

numbers = re.compile(r'(\d+)')

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def get_file():

    filename = sorted(glob.glob(folder_name + '/output_data*'), key=numericalSort)[-1]
    f = open(filename, "r")
    header = f.readline()
    print(filename)

    '''
    file_number = 0
    print(i)
    header = file.readline()
    print(header)
    if os.path.exists(folder_name + '/output_data%i.txt' % (file_number + 1)):
        file.close()
        file_number += 1
        file = open(folder_name + '/output_data%i.txt' % file_number, "r")
        header = file.readline()
        print('Reading file ' + folder_name + '/output_data%i.txt' % file_number)
        print(header)
    '''
    return f

def update():
    global folder_name
    global filename
    global oldname
    global file
    global where
    global new_where

    filename = sorted(glob.glob(folder_name + '/output_data*'), key=numericalSort)[-1]
    if filename != oldname:
        print('Changing file ', oldname, filename)
        file = open(filename, "r")
        file.seek(0, 0)
        header = file.readline()
        if oldname == 'ciao':
            while True:
                line = file.readline()
                if not line:
                    break
        oldname = filename

    where = file.tell()
    line = file.readline()
    if not line:
        file.seek(where)
    new_where = file.tell()

    if where != new_where:
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
                pass
            muon.add_signal(signal)
            line = file.readline()

        print(' ----> Muon', filename, datetime.today().time())
        muon.plot(ax)
        # muon.print()
        muon.reset()
        fig.canvas.draw_idle()



# ani = animation.FuncAnimation(fig, update, interval=1000)
timer = fig.canvas.new_timer(interval=200)
timer.add_callback(update)
timer.start()

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