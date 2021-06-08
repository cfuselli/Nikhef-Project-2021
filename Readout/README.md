## Readout

Hello,

Carlo here.
Enjoy going throug the files in this directory. 

This is how we are going to read from the detectors. 

You need to plug in the detectors, connecting everyone both to the power and the jack. 

You need to use the latest version of OLED_M_S.ino in your detectors. 

### What do i find? 

- cosmic_watch: it's the package folder, it contains the empty __init__.py file (important!) and the class_module.py where all the classes that I created are defined.

- live_multiple_class.py: this is the main code to read the data from the detectors in coincidence mode. You have to manually add the configuration of the detectors in the setup.ini file. This scripts connects automatically the detectors and the ports based on the names of the detectors (that you can change with naming.ino).

- live_plot.py: a script to do live plotting (work in progress)

- setup.ini: file where you define the layout of the detectors. You can add the name of the detector and then its position.
For example "CarloCosmicWatch = 0, 0, 0". The z part of the position must be an integer and represents the layer (top layer is layer 0). 

- output_data.txt: is where the data is saved.