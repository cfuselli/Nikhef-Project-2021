# Instructions Nikhef Project 2021 Detector

The limitation of this setup (0 detector, one USB hub + screen, keyboard and mouse) seems to overload the raspberry's IO once the scripts are running. Meaning: Once the detectors are read out, one cannot use the keyboard. Fix? Restart the raspberry by power-cycling.
This also means, that the plotting script. ```live_plot.py``` has to run before the readout script ```record_data.py``` is started. The plotting script has an 60s delay, which works but has not yet been pushed to git as the raspberry has not been connected to the internet since.

In general, make sure that the USB hub has AC power from the plug. And that the raspberry has enough disk space (```df -h <home_dir>```). Last time I checked, there was still several GB free and only 20GB used.
Also, the code works. So if one sees any errors appearing after weeks of running, the best is to power-cycle and restart. (Or to take the time automate this.) 

To (re)start the setup in the presentation mode:

1. Restart raspberrypi (unplug power cord).

2. Open two terminals (it looks nicer if you open both to fill each half the screen). In each setup the correct python path:

```
cd Nikhef-Project-2021/Readout_copy/
. setup.sh
```

3. Then, in the one terminal (use the right one), one starts the plotting script.

```
python3 live_plot.py
````

4. One now have 60s to start the date takings script in the left terminal and to enter the digits corresponding to the detectors (ttyUSB*).

```
python3 record_data.py
```

5. From now one, if one need to restart / stop / ..., one needs to start at 1.

###Bug fixes:

- one (or more) detector(s) does not connect:
* Restart the process at 1.. While the detectors are connecting, keep the reset button pushed at the back of the corresponding detector and let go circa 2s before the script tries to connect to this detecotr.

- the screen of a detector is not working
* power-cycle the detectors by turning off the USB hub and restart the Raspberry Pi. Note, for the upper row, the screens do not work anyways.