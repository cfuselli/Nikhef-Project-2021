import numpy as np
import matplotlib.pyplot as plt

#Define your parameters:

#Length of orthogonal scintillators
L=0.3

#This is the maximum detectable angle in degrees,leads to the height between scint. layers by h=L/tan(θ_max)
theta_max=60 

#Minimum and maximum detectable muons energy(in GeV):
E_min=1
E_max=50

#Number of possible energy values(this depends on SiPM's accuracy):
N_E=6

#For a random sample define 1,for a perfect CM distribution 0:
random=1

def MetropolisHastings(pdf, N, x_init, sigma):
    chain_points=np.zeros((N,x_init.shape[0]))
    stepsize=sigma
    x_old=x_init
    for i in range(N):
      x_new =np.random.uniform(low=x_old-(1/2)*stepsize,high=x_old+(1/2)*stepsize,size=x_old.shape)
      p_accept=min(1, pdf(x_new)/pdf(x_old))
      accept = (np.random.random()<p_accept)
      if accept:
        x_old=x_new
      chain_points[i,:]=x_old

    return chain_points
    
def pdf_theta(x,theta_max=theta_max*np.pi/180):
    if (x>theta_max) or (x<0):
        return 0
    return np.cos(x)**2

def norm(theta,E_min=E_min,E_max=E_max,N_E=N_E):
    dE=(E_max-E_min)/(N_E-1)
    e_k=115
    e_p=850
    E=E_min
    sum=0
    for i in range (N_E):
        sum+=0.14*dE*(E**(-2.7))*(((1/(1+1.1*E*np.cos(theta)/e_p))+(0.054/(1+1.1*E*np.cos(theta)/e_k))))
        E+=dE
    return sum


def pdf_e(E,theta=0,E_min=E_min,E_max=E_max,n=N_E):
    E_norm=norm(theta=theta)
    if (E<E_min) or (E>E_max):
        return 0
    dE=(E_max-E_min)/(n-1)
    e_k=115
    e_p=850
    p=0.14*dE*(E**(-2.7))*(((1/(1+1.1*E*np.cos(theta)/e_p))+(0.054/(1+1.1*E*np.cos(theta)/e_k))))
    return p/E_norm
    
    
def source(n_theta,n_phi,L,theta_max=60*np.pi/180,s_h=100):    
   h=L/np.tan(theta_max)
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
    
  
random=0
def simulation(time,N_theta,N_phi,random=random,L=L,theta_max=theta_max,N_E=N_E):
    N=int((L*L)*(2*(theta_max*(np.pi/180))/(np.pi))*time)*(E_max-E_min)
    x,y,z,directionx,directiony,directionz=source(N_theta,N_phi,L,theta_max*(180/np.pi)) 
    e=np.linspace(1,60,N_E)
    name =[]
    w=0
    if (random==1):
        x_init1=np.array([1])
        x_init2=np.array([10])
        bins=np.linspace(0,theta_max*(180/np.pi),N_theta+1)
        bins2=np.linspace(1,60,N_E+1)
        N_angles=plt.hist(MetropolisHastings(pdf_theta,N, x_init1, 0.1),bins=bins)
        n_phi=np.around(N_angles[0]/N_phi).astype(int)
    else:
        N_angles=np.zeros(N_theta)
        nor=0
        for i in range (N_theta):
            N_angles[i]=N*pdf_theta((i*theta_max*(np.pi/180))/(N_theta-1))
            nor+=N_angles[i]/N
        N_angles=N_angles/nor
        n_phi=np.around(N_angles/N_phi).astype(int)
    for i in range (N_theta):
        for j in range(N_phi):
            if (random==1):
                N_en=plt.hist(MetropolisHastings(pdf_e,n_phi[i] , x_init2,10 ),bins=bins2)
                N_events=N_en[0]
            else:
                N_events=np.zeros(N_E)
                for o in range (N_E):
                    N_events[o]=np.around((n_phi[i]*pdf_e(e[o])))
            n=0
            for k in N_events:
                if k>=1:
                    name.append("E_th_ph_"+str(int(e[n]))+"_"+str(int(60*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+".conf")
                    f = open(name[w], "w")
                    f.write(
'''[Allpix]
root_file = "E_th_ph_'''+str(int(e[n]))+"_"+str(int(60*(i/(N_theta-1))))+"_"+str(int(j*360/N_phi))+'''"
number_of_events = '''+str(int(k))+ '''
detectors_file = "scintillator_layer_2_detector.conf"
log_level= "Info"

[GeometryBuilderGeant4]
resolution_scale = 1

[DepositionGeant4]
optical_physics=true

scint_yield_factor = 1

source_position = '''+str(x[i,j])+"mm " +str(y[i,j])+"mm "+str(z[i,j])+'''mm
source_type = "beam"
particle_type = "mu-"
source_energy = '''+str(int(e[n]))+'''GeV
beam_direction = '''+str(directionx[i,j])+' '+str(directiony[i,j])+' '+str(directionz[i,j])+'''
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
                n+=1
                w+=1
    return name




def simulation_energy(N=10000,N_E=10,E_max=60,theta_max_energy=60):
    e=np.around(np.linspace(1,E_max,N_E))
    x,y,z,dx,dy,dz=source(2,1,0.3,theta_max=theta_max)
    name1 =[]
    name2 =[]
    n=-1
    for i in e:
        n+=1
        name1.append("sim_en_"+str(int(i))+"_0.conf")
        f = open(name1[n], "w")
        f.write(
'''[Allpix]
root_file = "sim_en_'''+str(int(i))+'''_0"
number_of_events = '''+str(N)+ '''
detectors_file = "scintillator_detector_1.conf"
log_level= "Info"

[GeometryBuilderGeant4]
resolution_scale = 1

[DepositionGeant4]
optical_physics=true

scint_yield_factor = 1

source_position = 0mm 0mm 100mm
source_type = "beam"
particle_type = "mu-"
source_energy = '''+str(i)+'''GeV
beam_direction = 0 0 -1 
physics_list = QGSP_BIC

output_plots=true
output_scale_hits = 50000
extra_scint_info = true


[ROOTObjectWriter]
include = "nothing"

[VisualizationGeant4]''')
	
        f.close()
        name2.append("sim_en_"+str(int(i))+"_60.conf")
        f = open(name2[n], "w")
        f.write(
'''[Allpix]
root_file = "sim_en_'''+str(int(i))+'''_60"
number_of_events = '''+str(N)+ '''
detectors_file = "scintillator_detector_1.conf"
log_level= "Info"

[GeometryBuilderGeant4]
resolution_scale = 1

[DepositionGeant4]
optical_physics=true

scint_yield_factor = 1

source_position = '''+str(x[1])+"mm " +str(y[1])+"mm "+str(z[1])+'''mm
source_type = "beam"
particle_type = "mu-"
source_energy = '''+str(i)+'''GeV
beam_direction =''' +str(dx[1])+' '+str(dy[1])+' '+str(dz[1])+'''
physics_list = QGSP_BIC

output_plots=true
output_scale_hits = 50000
extra_scint_info = true


[ROOTObjectWriter]
include = "nothing"

[VisualizationGeant4]''')
    return name1,name2
    
    
a,b=simulation_energy()
