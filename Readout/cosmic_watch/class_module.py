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
        self.name = 'Name not initialized'
        self.type = 'Master or Slave?'
        self.pos = [-999, -999, -999]
        self.count = 0
        self.muon_count = 0

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
        res = '{} {} {} {} {}'.format(self.layer,
                                      self.type,
                                      self.pos,
                                      self.port_name,
                                      self.name)
        return res


class Grid:
    def __init__(self):
        self.detectors = []

    def info(self):
        s = ''
        for d in self.detectors:
            s += d.info() + '\n'
        return s

    def plot(self, show=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = ["orange", "blue", "red", "yellow"]
        for d in self.detectors:
            ax.plot([d.pos[0]], [d.pos[1]], [d.pos[2]], markerfacecolor=colors[d.layer],
                    markeredgecolor=colors[d.layer], marker='o', markersize=8, alpha=0.8)
            ax.text(d.pos[0], d.pos[1], d.pos[2], d.name, size=10, color='k')
        ax.invert_zaxis()
        if show:
            plt.show()
        return ax

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

    def set_muon(self):
        self.muon = True

    def info(self):
        string = '{} {} {} {} {} {} {} {} {}'.format(self.detector.layer,
                                                     self.adc,
                                                     self.volt,
                                                     self.temp,
                                                     self.timediff,
                                                     self.time,
                                                     self.detector.muon_count,
                                                     self.detector.count,
                                                     self.detector.name)
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
            f.write(s.info() + '\n')
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
