import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, os, shutil
import time
import configparser
import serial.tools.list_ports
import schedule

# I don't know why this works on the computer of the lab but not on my MacBook (Carlo)
# from cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
# from cosmic_watch.class_module import serial_ports

from cosmic_watch.class_module import Grid, Detector, Signal, Stack, Muon
from cosmic_watch.class_module import serial_ports

print(" ")

stack = Stack(2)

# read config from setup.ini (READ README.md)
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read('setup.ini')
config_detectors = list(config.items(section='DETECTORS'))


grid = Grid()

# creating the detectors (but still not connected to ports)
for el in config_detectors:
    d = Detector()
    p = el[1].split(',')
    lay = int(p[0])
    pos = [p[1], p[2], p[3]]
    dim = [p[4], p[5], p[6]]
    d.pos = pos
    d.dimensions = dim
    d.layer = lay
    d.name = el[0]
    grid.detectors.append(d)
print(grid.info())


# connect detectors and ports based on name
port_name_list = serial_ports()
noname = True
for port_name in port_name_list:
    conn = serial.Serial(port=port_name, baudrate=9600, timeout=None)
    while True:
        if conn.inWaiting():
            data = conn.readline().replace(b'\r\n', b'').decode('utf-8').split(',')
            if data[0].lstrip() != 'OLED_M_S':
                print('Detector in port ', port_name, ' does not have OLED_M_S.ino installed!')
                break
            for d in grid.detectors:
                noname = True
                if d.name == data[1].lstrip():
                    d.set_port(port_name, conn)
                    d.type = data[2].lstrip()
                    print('Connected to detector: ', d.name, port_name)
                    noname = False
                    break
            if noname:
                print('No detector name found for this port ', port_name, data)
            break


# remove detectors for which we did not find a port
grid.remove_undefined_detectors()
if len(grid.detectors) == 0:
    sys.exit('No detectors correctly connected, program ended')

print('\nGrid configuration:\n')


def sortkey(dd):
    return dd.layer


grid.detectors.sort(key=sortkey)
print(grid.info())
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
grid.plot(ax, show=False)


signals_per_file = int(config['INFO']['signals_per_file'])
signals_per_control_file = int(config['INFO']['signals_per_control_file'])

file_number = 0
control_file_number = 0

today = datetime.today()
strx = today.strftime("%Y-%m-%d_%H-%M")

folder_name = 'output/output_' + strx + '/'
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


# Don't consider the first two seconds of data
# Not sure this is smart but made sense at some point
t_end = time.time() + 2
while time.time() < t_end:
    for detector in grid.detectors:
        if detector.port.inWaiting():
            data = detector.readline()

print("\nStart reading data\n")
start = datetime.now()

# Start loop of data taking
muon = Muon()
while True:
    for detector in grid.detectors:
        if detector.port.inWaiting():
            now = datetime.now()
            data = detector.readline()

            # how much time from the last signal?
            try:
                timediff = now - stack.peek().time
                timediff = timediff.total_seconds()
            except:
                # if stack is empty...
                timediff = 10

            # create a signal
            signal = Signal(detector)
            signal.time = now
            signal.timediff = timediff
            signal.set_data(data)
            upt = now - start
            signal.uptime = upt.total_seconds()

            stack.push(signal)

            signal.write(control_file)
            signal_control_count += 1

            if signal_control_count % signals_per_control_file == 0:
                control_file_number += 1
                control_file = open(folder_name + '/output_master_control%i.txt' % control_file_number, "w")
                control_file.write(header)

            # if last signal is close in time, then maybe it's a muon
            # we do not want a muon to pass two times in the same layer
            if timediff < 0.05 and stack.isEmpty() is False:
                if detector.layer not in muon.layers and detector.layer != stack.peek(1).detector.layer:
                    # if the signal before was targeted as muon, then this is still part of the same muon
                    if muon.not_empty():
                        muon.add_signal(signal)

                    # if not, we create a 'new muon'
                    else:
                        muon.add_signal(signal)
                        muon.add_signal(stack.peek(1))

            else:
                if muon.not_empty() and len(muon.signals) == 3:
                    muon_count += 1
                    print('-- %i Muon(s) detected --' % muon_count)
                    muon.print()
                    muon.write(file)

                    if muon_count % signals_per_file == 0:
                        file_number += 1
                        file.close()
                        file = open(folder_name + '/output_data%i.txt' % file_number, "w")
                        file.write(header)
                        file.flush()

                        tnow = datetime.now()
                        tdelta = datetime.now() - start
                        grid_file.write('\n' + tnow.ctime() + '(' + str(tdelta) + ')\n')
                        grid_file.write(grid.info() + '\n')
                        grid_file.flush()

                muon.reset()
