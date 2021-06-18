
import numpy as np
import matplotlib.pyplot as plt

def pdf_theta(x,theta=60):
    if (x>(np.pi*theta/180)) or (x<0):
        return 0
    return np.cos(x)**2
    
    
def source2(n_theta,n_phi,L=7.5,theta_max=10*np.pi/180):    
    s_h=200
    h=100
    z=np.ones((n_theta,n_phi,9))*(s_h+h+1)
    x=np.zeros((n_theta,n_phi,9))
    y=np.zeros((n_theta,n_phi,9))
    directionx=np.zeros((n_theta,n_phi,9))
    directiony=np.zeros((n_theta,n_phi,9))
    directionz=np.zeros((n_theta,n_phi,9))
    theta=np.linspace(0,theta_max,n_theta)
    phi=np.linspace(0,2*np.pi-2*np.pi/n_phi,n_phi)
    q1=np.array([0,0,0,1,1,1,-1,-1,-1])
    q2=np.array([0,-1,1,0,1,-1,0,1,-1])
    
    for i in range (n_theta):
        R=z[0,0,0]*np.tan(theta[i])
        for j in range (n_phi):
            for k in range (9):
                #print(q1[k],q2[k])
                x[i,j,k]=R*np.cos(phi[j])+q1[k]*(L/3)
                y[i,j,k]=R*np.sin(phi[j])+q2[k]*(L/3)
            
                dx=-np.sin(theta[i])*np.cos(phi[j])
                dy=-np.sin(theta[i])*np.sin(phi[j])
                dz=-np.cos(theta[i])
                
                directionx[i,j,k]=dx
                directiony[i,j,k]=dy
                directionz[i,j,k]=dz

    return 
    
    
random=0
L=7.5
def simulation_new(N,N_theta,N_phi):
    #N=int((L*L)*(2*(theta_max*(np.pi/180))/(np.pi))*time)*(E_max-E_min)
    x,y,z,directionx,directiony,directionz=source2(N_theta,N_phi,L,theta_max*(180/np.pi)) 
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
        for j in range (N_phi):
            N_events=(n_phi[i]/9).astype(int)
            for k in range(9):
                if N_events>=1:
                    name.append("N_th_ph_"+str(k)+"_"+str(int(10*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+".conf")
                    f = open(name[w], "w")
                    f.write(
'''[Allpix]
root_file = "N_th_ph_'''+str(k)+"_"+str(int(10*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+'''"
number_of_events = '''+str(int(N_events))+ '''
detectors_file = "scintillator_layer_2_detector.conf"
log_level= "Info"

[GeometryBuilderGeant4]
resolution_scale = 1

[DepositionGeant4]
optical_physics=true

scint_yield_factor = 1

source_position = '''+str(x[i,j,k])+"cm " +str(y[i,j,k])+"cm "+str(z[i,j,k])+'''cm
source_type = "beam"
particle_type = "mu-"
source_energy = 4GeV
beam_direction = '''+str(directionx[i,j,k])+' '+str(directiony[i,j,k])+' '+str(directionz[i,j,k])+'''
physics_list = QGSP_BIC

output_plots=true
output_scale_hits = 50000
extra_scint_info = true


[ROOTObjectWriter]
include = "nothing"

[Ignore]
#[VisualizationGeant4]''')
                else:
                    name.append("None")
                w+=1
    return name
    
simulation_new(10000,5,8) 

