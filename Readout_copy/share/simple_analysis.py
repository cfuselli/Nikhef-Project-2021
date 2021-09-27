# adc histograms
# @haslbeck
# 25th June deep at night...

import argparse
import numpy as np
import txt_to_root_matching_withbg as txthelper
import converter
import io
import matplotlib.pyplot as plt

    
# parse path
parser = argparse.ArgumentParser(description='read in txt files to make adc plots')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+',default = ['setup','master'], help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
parser.add_argument('-header', type=int, default = 1, help='header')
parser.add_argument('-title', type=str, default = '', help='title')
parser.add_argument('-bg', action='store_true', help='background?')



args = parser.parse_args()
path = args.path
if path[-1]!='/': path+='/'

files = txthelper.getFileNames(path, args.ignore, args.filetype)
setup_layer = txthelper.getSetup(path)

setup = [detector.split('_')[0] for detector in setup_layer]
print(setup,files)


adcs = {detector : [] for detector in setup}
time = [] #{detector : [] for detector in setup}
mVs = {detector : [] for detector in setup}
print(adcs,time)
    

conv = converter.Converter()

for f in files: 
    
    if '.txt' in f: f = f[:-4]
    

    rf = io.open('%s/%s.txt'%(args.path,f),encoding='utf-8')
     
        
    for i, line in enumerate(rf.readlines()):
            # skip header
            line = line.split(' ')
            if i < args.header : continue
            if len(line) == 1: continue
            # read in data
            
            detector = line[-2]
            adc = int(line[1])
            adcs[detector].append(adc)
            mVs[detector].append(conv.adc2mv(detector,adc))
            time.append(float(line[-1]))
  

if not args.bg: time = [0.5*(abs(time[i+1]-time[i])+abs(time[i+2]-time[i+1])) for i in range(0,len(time)-1,3)]
    


def makeHist(data_list,labels,name='',bins=32,binrange=(0,1024),\
                xlabel="ADC",ylabel="Entries / 32 ADC",title=args.title,
                normalize=True,path=args.path):
    plt.figure()
    
    for i,data in enumerate(data_list): 
        labels[i]+=' median %.2f'%(np.median(data))
        plt.hist(data,bins=bins,range=binrange,label=labels[i],density=True,histtype='step')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig("%s/%s.png"%(path,name), dpi=300)
    print("%s/%s.png"%(path,name))


# adc plots
nameadc = 'adc_bg_%s'%args.title.replace(' ','_') if args.bg else 'adc_%s'%args.title.replace(' ','_')
makeHist([adc for adc in adcs.values()],[det for det in setup_layer],name=nameadc,
         bins=16,binrange=(0,1024),xlabel="ADC",ylabel="Entries / 64 ADC",normalize=True)
#makeHist([mv for mv in mVs.values()],[det for det in setup_layer],name="mv",
#         bins=None,binrange=(0,1000),xlabel="mV (from calibration)",ylabel="Entries",normalize=False)
#makeHist([mVs[setup[2]]],[setup_layer[2]],name="mv",
#         bins=100,binrange=(0,1000),xlabel="mV (from calibration)",ylabel="Entries",normalize=False)

if not args.bg:
    makeHist([time],["avg. time difference"],name="timediff",\
             bins=10,binrange=(0,0.2),xlabel="average relative time difference between serial readings for muon-like event [s]",\
             ylabel="Entries / 0.02s")
    
# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')



print('goodbye')