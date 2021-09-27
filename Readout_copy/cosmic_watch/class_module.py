import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, glob
import time
import configparser
import serial.tools.list_ports
import numpy as np
import random

global text


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print(" ")
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

    print('Available serial ports:')
    for i in range(len(result)):
        print('[' + str(i + 1) + '] ' + str(result[i]))

    port_name_list = []

    ArduinoPort = input("Select Arduino port (comma separated): ")
    ArduinoPort = ArduinoPort.split(',')
    # nDetectors = len(ArduinoPort)
    for i in range(len(ArduinoPort)):
        port_name_list.append(str(result[int(ArduinoPort[i]) - 1]))

    print(" ")

    return port_name_list


class Detector:
    def __init__(self):
        self.port_name = None
        self.port = None
        self.layer = -1
        self.name = 'Name_not_initialized'
        self.type = 'Master_or_Slave?'
        self.pos = [-999, -999, -999]
        self.dimensions = [-999, -999, -999]
        self.count = 0
        self.muon_count = 0

    def set_port(self, name, serialport):
        self.port_name = name
        self.port = serialport

    def readline(self):
        return self.port.readline().replace(b'\r\n', b'').decode('utf-8')

    def info(self, counts=False):
        res = '{} {} {} {} {} {}'.format(self.layer,
                                         self.type,
                                         self.pos,
                                         self.dimensions,
                                         self.port_name,
                                         self.name)
        if counts:
            res = '{} {} {} {} {} {} {} {}'.format(self.layer,
                                                   self.type,
                                                   self.pos,
                                                   self.dimensions,
                                                   self.port_name,
                                                   self.name,
                                                   self.count,
                                                   self.muon_count)

        return res


class Grid:
    def __init__(self):
        self.detectors = []

    def info(self):
        s = ''
        for d in self.detectors:
            s += d.info() + '\n'
        return s

    def plot(self, ax, show=True):
        colors = ["orange", "blue", "red", "yellow"]
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')

        def get_cube(center, dist):
            cx, cy, cz = center[0], center[1], center[2]
            dx, dy, dz = dist[0], dist[1], dist[2]

            phi = np.arange(1, 10, 2) * np.pi / 4
            Phi, Theta = np.meshgrid(phi, phi)

            x = cx + np.cos(Phi) * np.sin(Theta) * dx
            y = cy + np.sin(Phi) * np.sin(Theta) * dy
            z = cz + np.cos(Theta) / np.sqrt(2) * dz
            return x, y, z

        for d in self.detectors:
            ax.plot([d.pos[0]], [d.pos[1]], [d.pos[2]], markerfacecolor=colors[d.layer],
                    markeredgecolor=colors[d.layer], marker='o', markersize=8, alpha=0.8)
            ax.text(d.pos[0], d.pos[1], d.pos[2], d.name, size=10, color='k')
            x, y, z = get_cube(d.pos, d.dimensions)
            ax.plot_surface(x, y, z, color=colors[d.layer], alpha=0.1)
        ax.invert_zaxis()

        if show:
            plt.show()

    def remove_undefined_detectors(self):
        to_remove = []
        print('\nChecking detectors that are not connected...')
        for d in self.detectors:
            if d.port_name is None:
                to_remove.append(d)

        for d in to_remove:
            print('Removed ', d.name)
            self.detectors.remove(d)


class Stack:
    def __init__(self, maxitems):
        self.items = []
        self.maxitems = maxitems

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        if self.size() > self.maxitems:
            self.pop()

    def pop(self):
        return self.items.pop(0)

    def peek(self, i=0):
        return self.items[len(self.items) - i - 1]

    def size(self):
        return len(self.items)

    def detectors(self):
        result = []
        for it in self.items:
            result.append(it.detector)
        return result


class Signal:
    def __init__(self, detector):
        self.detector = detector
        self.time = 0
        self.timediff = 0
        self.uptime = 0
        self.adc = 0
        self.volt = 0
        self.temp = 0
        self.count = 0
        detector.count += 1

    def set_data(self, data):
        #   0               1                   2
        # count + " [" + countslave + "] " + time_stamp + " " +
        #  3            4                       5
        # adc+ " " + sipm_voltage + " " + measurement_deadtime+ " " +
        #   6                       7                   8                   9
        # temperatureC + " " + MASTER_SLAVE + " " + keep_pulse + " " + detector_name);
        data = data.split(' ')
        self.adc = data[3]
        self.volt = data[4]
        self.temp = data[6]
        self.count = int(data[0])

    def info(self):
        string = '{} {} {} {} {} {} {} {} {} {}'.format(self.detector.layer,
                                                        self.adc,
                                                        self.volt,
                                                        self.temp,
                                                        self.timediff,
                                                        self.time,
                                                        self.detector.muon_count,
                                                        self.detector.count,
                                                        self.detector.name,
                                                        self.uptime)
        return string

    def write(self, f):
        f.write(self.info() + '\n')
        f.flush()


class Muon:
    def __init__(self):
        self.signals = []
        self.layers = []
        self.detectors = []

    def add_signal(self, sig):
        self.signals.append(sig)

        def sortkey(s):
            return s.detector.layer

        self.signals.sort(key=sortkey)
        self.layers.append(sig.detector.layer)
        self.detectors.append(sig.detector)
        sig.detector.muon_count += 1

    def peek(self, i=0):
        return self.signals[len(self.signals) - i - 1]

    def write(self, f):
        for s in self.signals:
            s.write(f)
        f.write('\n')
        f.flush()

    def print(self):
        for s in self.signals:
            print(s.info())

    def not_empty(self):
        if len(self.signals) == 0:
            return False
        else:
            return True

    def reset(self):
        self.signals = []
        self.layers = []
        self.detectors = []

    def plot(self, ax, text=None):

        r = min(self.signals[1].detector.pos[0], self.signals[1].detector.pos[1]) / 2
        rx = random.uniform(-r, r)
        ry = random.uniform(-r, r)
        x = [self.signals[0].detector.pos[0] + rx, self.signals[1].detector.pos[0] + ry]
        rx = random.uniform(-r, r)
        ry = random.uniform(-r, r)
        y = [self.signals[0].detector.pos[1] + rx, self.signals[2].detector.pos[1] + ry]
        z = [self.signals[0].detector.pos[2], self.signals[2].detector.pos[2]]

        adc = max(self.signals[0].adc,
                  self.signals[1].adc,
                  self.signals[2].adc)

        adc_linew = int(adc/1023) + 1

        # Connect the first two points in the array
        line = ax.plot(x, y, z, alpha=0.98, linewidth=adc_linew)
        stringg = 'ADC: ' + str(adc)
        text.set_text(stringg)

        return line
