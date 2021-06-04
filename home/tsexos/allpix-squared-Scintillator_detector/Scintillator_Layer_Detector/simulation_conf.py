import numpy as np
import matplotlib.pyplot as plt

#Generating the configuration files for the allpix simulation.
#You only call the simulation function.


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
    
def pdf_theta(x,theta_max=60):
    if (x>(np.pi*theta_max/180)) or (x<0):
        return 0
    return np.cos(x)**2

def norm(E_min,E_max,n,theta):
    dE=(E_max-E_min)/(n-1)
    e_k=115
    e_p=850
    E=E_min
    sum=0
    for i in range (n):
        sum+=0.14*dE*(E**(-2.7))*(((1/(1+1.1*E*np.cos(theta)/e_p))+(0.054/(1+1.1*E*np.cos(theta)/e_k))))
        E+=dE
    return sum


def pdf_e(E,E_min=1,E_max=60,theta=0,n=6):
    E_norm=norm(E_min,E_max,n,theta)
    if (E<E_min) or (E>E_max):
        return 0
    dE=(E_max-E_min)/(n-1)
    e_k=115
    e_p=850
    p=0.14*dE*(E**(-2.7))*(((1/(1+1.1*E*np.cos(theta)/e_p))+(0.054/(1+1.1*E*np.cos(theta)/e_k))))
    return p/E_norm
    
    
def source(n_theta,n_phi,L,theta_max=60*np.pi/180,s_h=1):    
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
    

def simulation(time,N_theta,N_phi,L,theta_max=60):
    N=int((L*L)*(2*(theta_max*(np.pi/180))/(np.pi))*time)
    x_init1=np.array([1])
    x_init2=np.array([10])
    x,y,z,directionx,directiony,directionz=source(N_theta,N_phi,L,theta_max*(180/np.pi)) 
    bins=np.linspace(0,theta_max*(180/np.pi),N_theta+1)
    bins2=np.linspace(1,60,5)
    e=np.linspace(1,60,5)
    N_angles=plt.hist(MetropolisHastings(pdf_theta,N, x_init1, 0.1),bins=bins)
    n_phi=np.around(N_angles[0]/N_phi).astype(int)
    for i in range (N_theta):
        for j in range(N_phi):
            N_events=plt.hist(MetropolisHastings(pdf_e,n_phi[i] , x_init2,10 ),bins=bins2)
            n=0
            for k in N_events[0]:
                f = open("par_(E,theta,phi)=("+str(int(e[n]))+","+str(int(60*(i/(N_theta-1))))+","+str(int(j*360/N_phi))+").conf", "w")
                f.write(''' 
                [Allpix] \n
                number_of_events = '''+str(k)+ ''' \n
                detectors_file = "scintillator_detector.conf" \n 
                log_level= "Info" \n

                [GeometryBuilderGeant4] \n
                resolution_scale = 1 \n

                [DepositionGeant4] \n
                optical_physics=true \n

                scint_yield_factor = 1 \n

                source_position = '''+str(x[i,j])+"mm " +str(y[i,j])+"mm "+str(z[i,j])+'''mm \n
                source_type = "beam" \n
                particle_type = "mu-" \n
                beam_energy = '''+str(e[n])+'''MeV \n
                beam_direction = '''+str(directionx[i,j])+' '+str(directiony[i,j])+' '+str(directionz[i,j])+''' \n 
                physics_list = QGSP_BIC \n

                output_plots=true \n
                output_scale_hits = 50000
                extra_scint_info = true

            
                [ROOTObjectWriter]
                include = "nothing"

                [VisualizationGeant4] ''')
                n+=1 
    
    
    

