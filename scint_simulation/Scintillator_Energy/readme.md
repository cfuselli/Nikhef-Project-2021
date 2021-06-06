##E_min and E_max Simulation:

The goal is to find the minimum energy and maximum energy for one detector.By the 0 theta muons we expect to 
find the energy minimum and by the maximum angle the energy minimum,considering the travelled distance of muons inside the scintillator.  

#Process

1)Create a new folder and create a read.me file defining the used parameters.

2)Copy the simulation_conf.py and scintillator_detector_orth.conf(one detector from the complex grid) and
scintillator_detector_square.conf(initial CW shape) in there.

3)Change one of the N,N_E,E_max,theta_max_energy parameter at the simulation_energy() definition with the values you prefer.

N:number of events for each simulation
N_E:number of possible energy values
E_max:maximum energy value
theta_max_energy:maximum angle value

4)In the end of the new python file call simulation_energy() in order to create all the allpix configure files.

5)Rename the detector_conf file,depending on the detector shape you want to test,as "scintillator_detector_1.conf".

6)In the name of each conf file there are the proper (Ε,θ) values.You have to execute each one at a time
(after you sourced the allpix code) by:  allpix -c <name_of_conf>
