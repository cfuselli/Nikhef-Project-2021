import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, glob
import time
import configparser
import serial.tools.list_ports


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
        print('['+str(i+1)+'] ' + str(result[i]))

    port_name_list = []

    ArduinoPort = input("Select Arduino port (comma separated): ")
    ArduinoPort = ArduinoPort.split(',')
    # nDetectors = len(ArduinoPort)
    for i in range(len(ArduinoPort)):
        port_name_list.append(str(result[int(ArduinoPort[i])-1]))

    print(" ")

    return port_name_list


class Detector:
    def __init__(self):
        self.port_name = 'Port undefined'
        self.port = None
        self.layer = -1
        self.name = 'Name not initialized'
        self.type = 'Master or Slave?'
        self.pos = [-999, -999, -999]

    def set_port(self, name, serialport):
        self.port_name = name
        self.port = serialport

    def set_layer(self, layer_num):
        self.layer = int(layer_num)

    def set_name(self, dname):
        self.name = dname

    def set_type(self, t):
        self.type = t

    def set_pos(self, _pos):
        self.pos = _pos
        self.layer = int(_pos[2])

    def readline(self):
        return self.port.readline().replace(b'\r\n', b'').decode('utf-8')

    def info(self):
        print('--', self.name, self.type, self.pos, self.layer, self.port_name)

    def get_layer(self):
        return int(self.layer)

    def get_pos(self):
        return self.pos


class Layer:
    def __init__(self, index):
        self.detectors = []
        self.index = index

    def add_detector(self, det):
        self.detectors.append(det)

    def remove_detector(self, det):
        self.detectors.remove(det)


class Grid:
    def __init__(self):
        self.layers = []
        self.nLayers = 0

    def add_layer(self, lay):
        self.layers.append(lay)
        self.nLayers += 1

    def info(self):
        for l in self.layers:
            print("Layer ", l.index)
            for d in l.detectors:
                d.info()

    def get_layer(self, index):
        return self.layers[index]

    def get_detector_list(self):
        result = []
        for lay in self.layers:
            for det in lay.detectors:
                result.append(det)
        return result


    def plot(self, show=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = ["orange", "blue", "red", "yellow"]
        for d in self.get_detector_list():
            ax.plot([d.pos[0]], [d.pos[1]], [d.pos[2]], markerfacecolor=colors[d.get_layer()], markeredgecolor=colors[d.get_layer()], marker='o', markersize=8, alpha=0.8)
            ax.text(d.pos[0], d.pos[1], d.pos[2], d.name, size=10, color='k')
        ax.invert_zaxis()
        if show:
            plt.show()
        return ax

    def remove_undefined_detectors(self):
        for lay in self.layers:
            for d in lay.detectors:
                if d.port_name == 'Port undefined':
                    print('\nRemoved this detector, port undefined!')
                    d.info()
                    print(' ')
                    lay.remove_detector(d)


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
    def __init__(self, data, detector, time, timediff):
        data = data.split(' ')
        self.detector = detector
        self.time = time
        self.timediff = timediff
        self.adc = data[3]
        self.volt = data[4]
        self.muon = False
        self.count = int(data[0])

    def set_muon(self):
        self.muon = True

        # count + " [" + countslave + "] " + time_stamp + " " + adc +
        # " " + sipm_voltage + " " + measurement_deadtime + " " + temperatureC + " " + MASTER_SLAVE + " " + keep_pulse + " " + detector_name

    def info(self):
        s = '   ' + str(self.count) + ' ' + self.detector.name + ' ' + str(self.time) + ' ' + str(self.adc) + ' ' + str(self.volt) + ' ' + str(self.timediff)
        return s

    def write(self, f):
        f.write(self.info() + '\n')
        f.flush()

