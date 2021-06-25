import argparse
import numpy as np
import txt_to_root_matching_withbg as txthelper
import converter
import io
import matplotlib.pyplot as plt

    
    # parse path
parser = argparse.ArgumentParser(description='convert all .txt in folder to single root file')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+',default = ['setup','master'], help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
parser.add_argument('-header', type=int, default = 1, help='header')
#parser.add_argument('-cw', type=float, default = 0.1, help='acceptance time window for two consecutive readings')
#parser.add_argument('-tw', type=float, default = 0.4, help='total acceptance for a muon')


def makeHist(data_list,labels,bins=32,binrange=(0,1024),xlabel="ADC",ylabel="Entries / 32 ADC",normalize=False):
    print(data_list)
    plt.figure()
    for i,data in enumerate(data_list):
        plt.hist(data,bins=bins,range=binrange,label=labels[i],density=normalize,histtype='step')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

args = parser.parse_args()
path = args.path
if path[-1]!='/': path+='/'

files = txthelper.getFileNames(path, args.ignore, args.filetype)
setup = txthelper.getSetup(path)

setup = [detector.split('_')[0] for detector in setup]
print(setup,files)


adcs = {detector : [] for detector in setup}
time = {detector : [] for detector in setup}
mV = {detector : [] for detector in setup}
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
            print(conv.adc2mv(detector,adc))
            #mV[detector].append(float(line[4]))
            time[detector].append(float(line[4]))
            
#print(len(adcs[setup[0]]),len(time))


makeHist([adc for adc in adcs.values()],[det for det in adcs.keys()],
         bins=32,binrange=(0,1024),xlabel="ADC",ylabel="Entries / 32 ADC",normalize=False)
    
# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')



print('goodbye')