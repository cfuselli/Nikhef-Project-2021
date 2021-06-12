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

In general you run from Scintillator_detector folder the command:bin/allpix -c path/to/conf

#Some change for our case: 
Go to folder "examples" to file "scintillator_tutorial_detector.conf",delete everything before [scintillator_box].
Change this "type = "scintillator_tutorial_model_box" " to " type = "scintillator_box" ".
Choose position and orientation of scintillator or add additional scintillators by following the same formalism.

#Change source parameters:
In the folder "examples" in the file "scintillator_tutorial_config.conf" you can change:particle,energy,source's position+direction,number 
of events.

#Change scintillator parameters:
Open the file "scintillator_box.conf" in the folder "model".The size and shape parameters can be changed to the values you prefer.If you 
want to deactivate housing chane the housing_thickness to 0.You can also change the material with the possible choices to be:
cebr3 :Cerium Bromide
Labr3 :Lanthandium Bromide
nai :Sodium Iodide
bgo :Bismuth Germenate
Other possible scintillator shape is "cylinder" but we do not use this in our detector.
If additional scintillators with different shapes are needed,go to folder "models" and copy the file "scintillator_box.conf" and rename it 
with similar name,example:"scintillator_box1.conf".You choose the characteristics of each scintillator in each file like the previous one 
and when you want to simulate them in the "detector.conf" file chose them as "type",example:type="scintillator_box1.conf"
 
#Deactivate visualization:
In the folder "examples" in the file "scintillator_tutorial_config.conf" in the end delete [VisualizationGeant4] (or just write # in 
front) and write [Ignore]. 
 
#Output data:
After running one simulation a folder "output" is created.You can access the output data by:

cd output
root -l modules.root 
TBrowser t;

The ouput data can be found in the form of histograms at the output/data.root/DepositionGeant4 folder.The classes of data for each 
detector are:

Photons hits
Energy of photon
Wavelength of photon
Detection time of photon
Emission time of photon
Travel time of photon
