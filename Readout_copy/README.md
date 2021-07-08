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

The output of the script is saved into one folder named with the date and time of the measurement. There are three different kind of files in this folder.

The first one is just a modified copy of the configuration file used to run the program: as the configuration changed a lot from one measurement to the other, it has been very important to always have file in the folder where the setup of the detectors is automatically stored. 

There is then another text file where the main results are stored: this is just a list of the muons that were detected during the measurement. Every muon event consists of three lines (one line per every signal, where each signal belongs to detectors of the three different layers), followed by a blank line. The signals of a single event are not ordered in time, but they are sorted by their layer from top to bottom. The script automatically divides these results in different files when the maximum number of events per file is reached (this can be set through the configuration file) to avoid having very large text files that can be difficult to work with.

The last kind of file (again a text file), is where every signal recorded by every detector is stored. Here it is possible to do some non-live software analysis and to study the background measured by the single detectors. Also these files are separated in multiple ones when they reach a certain amount of lines.
