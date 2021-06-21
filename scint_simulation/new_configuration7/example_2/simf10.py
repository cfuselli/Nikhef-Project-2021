import numpy as np
import matplotlib.pyplot as plt

#Define your parameters:

#Length of orthogonal scintillators
h_0=10
#This is the maximum detectable angle in degrees,leads to the height between scint. layers by h=L/tan(θ_max)
theta_max=45


def pdf_theta(x,theta_max=theta_max*np.pi/180):
    if (x>theta_max) or (x<0):
        return 0
    return np.cos(x)**2

def source(n_theta,n_phi,theta_max=theta_max*np.pi/180,h=h_0,s_h=1000):   
    z=np.ones((n_theta,n_phi))*(h/2+s_h)
    x=np.zeros((n_theta,n_phi))
    y=np.zeros((n_theta,n_phi))
    directionx=np.zeros((n_theta,n_phi))
    directiony=np.zeros((n_theta,n_phi))
    directionz=np.zeros((n_theta,n_phi))
    theta=np.linspace(0,theta_max,n_theta)
    phi=np.linspace(0,2*np.pi-2*np.pi/n_phi,n_phi)

    for i in range (n_theta):
        R=z[0,0]*np.tan(theta[i])
        for j in range (n_phi):
            x[i,j]=R*np.cos(phi[j])
            y[i,j]=R*np.sin(phi[j])
            directionx[i,j]=-np.sin(theta[i])*np.cos(phi[j])
            directiony[i,j]=-np.sin(theta[i])*np.sin(phi[j])
            directionz[i,j]=-np.cos(theta[i])

    return x,y,z,directionx,directiony,directionz
    
    
def simulation(N,N_theta,N_phi,theta_max=theta_max):
    x,y,z,directionx,directiony,directionz=source(N_theta,N_phi) 
    name =[]
    w=0
    N_angles=np.zeros(N_theta)
    nor=0
    for i in range (N_theta):
        N_angles[i]=N*pdf_theta((i*theta_max*(np.pi/180))/(N_theta-1))
        nor+=N_angles[i]/N
    N_angles=N_angles/nor
    n_phi=np.around(N_angles/N_phi).astype(int)
    for i in range (N_theta):
        for j in range(N_phi):
            N_events=n_phi[i]
            name.append("A10_th_ph_"+str(int(theta_max*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+".conf")
            f = open(name[w], "w")
            f.write(
'''[Allpix]
root_file = "A10_th_ph_'''+str(int(theta_max*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+'''"
number_of_events = '''+str(N_events)+ '''
detectors_file = "scintillator_layer_new_detector10.conf"
log_level= "Info"

[GeometryBuilderGeant4]
resolution_scale = 1

[DepositionGeant4]
optical_physics=true

scint_yield_factor = 1

source_position = '''+str(x[i,j])+"cm " +str(y[i,j])+"cm "+str(z[i,j])+'''cm
source_type = "beam"
particle_type = "mu-"
source_energy = 4GeV
beam_direction = '''+str(directionx[i,j])+' '+str(directiony[i,j])+' '+str(directionz[i,j])+'''
physics_list = QGSP_BIC

output_plots=true
output_scale_hits = 150000
extra_scint_info = true


[ROOTObjectWriter]
include = "nothing"

[Ignore]
#[VisualizationGeant4]''')
            w+=1
    return name  


a=simulation(2000,5,8)
