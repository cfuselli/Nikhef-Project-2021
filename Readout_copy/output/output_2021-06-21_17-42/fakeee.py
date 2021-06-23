import matplotlib.pyplot as plt
import serial
from datetime import datetime
import sys, os, shutil
import time
import configparser
import serial.tools.list_ports
import schedule
import random
import io

file = io.open('output_data1.txt', mode='w')

while True:
    s = """0 255 43.96 27.34 2.739193 2021-06-21 17:49:38.084558 16 326 Cecile 420.810413
1 124 23.92 27.34 0.033954 2021-06-21 17:49:38.118512 14 14 MattiaCosmicWatch 420.844367
2 88 20.96 26.05 0.006154 2021-06-21 17:49:38.124666 9 10 Niels 420.850521

"""
    file.write(s)
    file.flush()
    time.sleep(2)
