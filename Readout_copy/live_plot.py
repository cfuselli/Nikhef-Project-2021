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
import io

from class_module import *

numbers = re.compile(r'(\d+)')

def numericalSort(value): # this can be done without regex...
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# Pick the last folder of data in the output folder
folder_name = sorted(glob.glob('output/output_*'), key=numericalSort)[-1]
print('Reading folder: ', folder_name)

# Open grid_setup file and start building the grid
file = io.open(folder_name + '/grid_setup.txt', 'r', encoding = 'utf-8')
grid = Grid()

# read and build the grid and the detectors
for i, line in enumerate(file.readlines()):
    if i == 0:
        print('Data from: ', line)
    else:
        if len(line) < 3:
            # when we find a blank line, we stop reading the grid
            break

        # create a detector !
        d = Detector()
        line = line.replace('[', ' ')
        line = line.replace(']', ' ')
        line = line.replace('\n', ' ')
        line = line.replace(',', ' ')
        line = line.replace("'", ' ')
        #line = line.replace(']', '').split(' ')
        line = line.split(' ')
        line = [val for val in line if val != '']
        print(line)
        
        print(line)
        pos = [float(line[2]), float(line[3]), float(line[4])]
        dim = [float(line[5]), float(line[6]), float(line[7])]
        d.pos = pos
        d.dimensions = dim
        d.name = line[9]
        d.type = line[1]
        d.layer = int(line[0])
        grid.detectors.append(d)

print(grid.info())
file.close()

# create fig and plot the grid
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
grid.plot(ax, show=False)

# initialize some variables
oldname = None
file_number = 0
muon = Muon()
alpha_factor = 1.1


def update():
    '''
    This function is called continuously based on the interval of the timer
    '''

    global folder_name
    global filename
    global oldname
    global file
    global where
    global new_where

    # change the alpha of every plotted line (line == muon)
    # changing the alpha factor makes lines disappear quicker or slower
    for mline in fig.gca().lines:
        try:
            mline.set_alpha(plt.getp(mline, 'alpha')/alpha_factor)
            if plt.getp(mline, 'alpha') < 0.01:
                mline.remove()
        except:
            pass

    # find the last file in the folder that we are reading
    filename = sorted(glob.glob(folder_name + '/output_data*'), key=numericalSort)[-1]
    if filename != oldname:
        # if there is a new file
        print('Changing file ', oldname, filename)
        file.close()
        file = io.open(filename, "r", encoding='utf-8')
        file.seek(0, 0)
        header = file.readline()
        if oldname is None:
            # if this is the first file that we are reading
            # let's go to the end of it
            while True:
                line = file.readline()
                if not line:
                    break
        oldname = filename

    # try to read a line. if empty, come back with the cursor
    where = file.tell()
    line = file.readline()
    if not line:
        file.seek(where)
    new_where = file.tell()

    # if there was a new line, it's a muon !
    # let's read the lines until the next blank line
    if where != new_where:
        while line != '\n':
            line = line.replace('\n', '')
            lsplit = line.split(' ')
            print(lsplit)
            det = 0
            # find the right detector to assign
            for d in grid.detectors:
                if d.name == lsplit[9]:
                    det = d
                    break
            if det == 0:
                strin = 'Unknown detector found ' + lsplit[9]
                exit(strin)

            # add the data to each signal
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
        muon.print()
        muon.reset()
        fig.canvas.draw_idle()


timer = fig.canvas.new_timer(interval=200)
timer.add_callback(update)
timer.start()

plt.show()
