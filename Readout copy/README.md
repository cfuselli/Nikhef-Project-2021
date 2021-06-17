## Readout

Hello,

Carlo here.
Enjoy going throug the files in this directory. 

This is how we are going to read from the detectors. 

You need to plug in the detectors, connecting everyone both to the power and the jack (use usb hub). 

You need to use the latest version of OLED_M_S.ino in your detectors. 
----
### What do I find? 

- cosmic_watch: it's the package folder, it contains the empty __init__.py file (important!) and the class_module.py where all the classes that I created are defined.

- record_data.py: this is the main code to read the data from the detectors in coincidence mode. You have to manually add the configuration of the detectors in the setup.ini file. This scripts connects automatically the detectors and the ports based on the names of the detectors (that you can change with naming.ino).

- mock_data.py: just to fake some data from random detectors to easily test live plotting

- live_plot.py: a script to do live plotting

- setup.ini: file where you define the layout of the detectors. You can add the name of the detector and then its position.
For example "CarloCosmicWatch = 1, 0, 0, 0, 2, 2, 1".
They represent: layer, center_x, center_y, center_z, dimension_x, dimension_y, dimension_z  
Here you also need to specify how many events you want per file and controlfile.

----
### What is the output? 

- grid_setup.txt: the setup 

- output_data*.txt: list of muons, line separated

- output_master_control*.txt: raw signals from master(s), plus slaves in coincidence

You can decide how many events you want to record per file. They will be automatically splitted.

