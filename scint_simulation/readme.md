##Allpix-Squared Simulation Project:

The goal is to simulate the cosmic muons as sources and to test the detectable events of scintillator detectors for varius shapes and 
combinations.Because Allpix doesn't allow more than sources in each simulation,we create a grid of possible directions (θ,φ) and energy 
values and we calculate the expected number of events for each combination of them by the known angular and energy distributions.Then we 
simulate each parameters combination one at the time.The following folders contain the codes and instructions on how to create the 
necessary config files for the allpix simulations we aim.

#Scintillator_Layer_Detector:
Simulation of two layers of scintillator detectors for an isotropic cosmic muons source.We create the position and the direction of each 
(θ,φ) case for a variety of energy values.We aim to observe the ratio of detectable events from the total events for each (Ε,θ,φ) case and 
also to recreate the observed pulse's peak value from the detector.A general expectation is to observe that the detectable events also 
follows the theretical angular and energy distributions.

#Scintillator_Energy:
Simulation of the initial cosmic watch scintillator detector and one of the orthogonal scintillators of the two layers case.Then we test 
their measurements (each one at a time) for theta=0 and theta=theta_max while we change the muons energy.By the detectable events we aim to 
define the detectable energy range of muons,this is necessary for the Scintillator_Layer_Detector case and also for the expectable events 
in any case (check cosmic muons intensity formula).By the theta=0 we expect to find the minimum energy value and in the other case the 
maximum,considering the travelled distance inside the scintillator.

#Scintillator_shape:
We test how the different dimensions of the scintillator effect the measureble events.

#Planb and Planc:
Different final detector configurations for the case of 8 working detectors.

