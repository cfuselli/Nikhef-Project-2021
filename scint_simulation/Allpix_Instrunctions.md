##Allpix_scintillator_instructions:

#Commands at pc with CVMFS:

source /cvmfs/clicdp.cern.ch/software/allpix-squared/1.6.2/x86_64-centos7-gcc10-opt/setup.sh
git clone https://gitlab.cern.ch/kvandenb/allpix-squared.git -b Scintillator_detector
cd Scintillator_detector
mkdir build
cd build
cmake ..
make install
cd ..
#If you want to execute the simulation: (but better check first the rest of this to change the parameters)
bin/allpix -c examples/scintillator_tutorial_config.conf

#Some change for our case: 
Go to folder "examples" to file "scintillator_tutorial_detector.conf",delete everything before [scintillator_box].
Change this "type = "scintillator_tutorial_model_box" " to " type = "scintillator_box" ".
Choose size and orientation of scintillator.

#Change source parameters:
In the folder "examples" in the file "scintillator_tutorial_config.conf" you can change:particle,energy,source's position+direction,number 
of events.

#Change scintillator parameters:
Open the file "scintillator_box.conf" in the folder "model".The size and shape parameters can be changed to the values you prefer.If you 
want to deactivate housing chane the housing_thickness to 0. 

#Deactivate visualization:
In the folder "examples" in the file "scintillator_tutorial_config.conf" in the end delete [VisualizationGeant4] (or just write # in front) 
and write [Ignore] 
 

