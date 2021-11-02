##Layer Scintillator Detector Simulation:The goal is to simulate our two layer detector.

#Process:
1)Create a new folder and create a read.me file defining the used parameters.

2)Copy the simulation_conf.py and scintillator_detector.conf in there.If you want to change the scintillator shape change the 
appropriate values in scintillator_detector.conf file and scintillator_box1.conf file.For details see at the last part of this file.Then 
copy scintillator_box1.conf in "model" folder of the allpix-squared folder.

3)Change the initial parameters at the start of the simulation_conf.py with the values you prefer.
Parameters:
L:Length of orthogonal scintillators

theta_max:maximum detectable angle in degrees,leads to the height between scint. layers by h=L/tan(θ_max)

Minimum and maximum detectable muons energy(in GeV):
E_min
E_max

N_E:Number of possible energy values(this depends on SiPM's accuracy)

random:For a random sample define 1,for a perfect CM distribution 0

4)In the end of the new python file call a=simulation(n_theta,n_phi) in order to create all the allpix configure files,where n_theta is 
the number of theta values in [0,theta_max] and n_phi the number of phi values in [0,2π].

5)In the name of each conf file there are the proper (Ε,φ,θ) values.You have to execute each one at a time
(after you sourced the allpix code,see instrunctions) inside the main folder (Scintillator_detector) by:  bin/allpix -c path/
<name_of_conf>

#General detector configuration template (don't change orientation!!!):

*Model file:
__________________________________________________________________________________________________________________________________________
type = "scintillator"
sensor_size = S1mm S2mm S3mm
sensor_material = silicon
scintillator_shape= box
scintillator_size= L1mm L2mm L3mm
scintillator_material= cebr3
housing_thickness = Tmm
housing_reflectivity = 1.0 #This value describes the perfect reflectivity case,in real measumeremets always smaller than 1.
__________________________________________________________________________________________________________________________________________

*Detector conf file:
__________________________________________________________________________________________________________________________________________
[detector1]
type = "scintillator_box"
position = 0mm 0mm 0mm
orientation = 0deg 0deg 90deg

[detector2]
type = "scintillator_box"
position = L2mm 0mm 0mm
orientation = 0deg 0deg 90deg

[detector3]
type = "scintillator_box"
position = -L2mm 0mm 0mm
orientation = 0deg 0deg 90deg

[detector4]
type = "scintillator_box"
position = 0mm 0mm h1mm
orientation = 0deg 0 0deg

[detector5]
type = "scintillator_box"
position = 0mm L2mm h1mm
orientation = 0deg 0 0deg

[detector6]
type = "scintillator_box"
position = 0mm -L2mm h1mm
orientation = 0deg 0 0deg

[detector7]
type = "scintillator_box"
position = 0mm 0mm Hmm
orientation = 0deg 0deg 90deg

[detector8]
type = "scintillator_box"
position = L2mm 0mm Hmm
orientation = 0deg 0deg 90deg

[detector9]
type = "scintillator_box"
position = -L2mm 0mm Hmm
orientation = 0deg 0deg 90deg

[detector10]
type = "scintillator_box"
position = 0mm 0mm H+h2mm
orientation = 0deg 0 0deg

[detector11]
type = "scintillator_box"
position = 0mm L2mm H+h2mm
orientation = 0deg 0 0deg

[detector12]
type = "scintillator_box"
position = 0mm -L2mm H+h2mm
orientation = 0deg 0 0deg

__________________________________________________________________________________________________________________________________________

**S1xS2xS3:sensor dimensions
**L1:scintillator length
**L2:scintillator width.For the case of housing with thickness T we have: L2->L2+2*T
**L3:Scintillator thickness
**T:housing thickness
**h1:height between "ground" and next layer.
**H:height between 2nd and 3rd layer (has the highest value).
**h2:height between the two upper layers.


