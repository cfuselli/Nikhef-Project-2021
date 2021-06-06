##Layer Scintillator Detector Simulation:The goal is to simulate our two layer detector.

#Process:
1)Create a new folder and create a read.me file defining the used parameters.

2)Copy the simulation_conf.py and scintillator_detector.conf in there.If you want to change the scintillator shape change the 
appropriate values in scintillator_detector.conf file.

3)Change the initial parameters at the start of the simulation_conf.py with the values you prefer.
Parameters:
L:Length of orthogonal scintillators

theta_max:maximum detectable angle in degrees,leads to the height between scint. layers by h=L/tan(θ_max)

Minimum and maximum detectable muons energy(in GeV):
E_min
E_max

N_E:Number of possible energy values(this depends on SiPM's accuracy)

random:For a random sample define 1,for a perfect CM distribution 0

4)In the end of the new python file call simulation(n_theta,n_phi) in order to create all the allpix configure files,where n_theta is the number of theta values in [0,theta_max] and n_phi the number of phi values in [0,2π].

5)In the name of each conf file there are the proper (Ε,φ,θ) values.You have to execute each one at a time
(after you sourced the allpix code) by:  allpix -c <name_of_conf>
