#!/usr/bin/env python3
# adc histograms per detector 
# @haslbeck
# 4th July 2021 - happy Higgs day


import argparse
import numpy as np
import txt_to_root_matching_withbg as txthelper
import converter
import io
import matplotlib.pyplot as plt

conv = converter.Converter()
  
# parse path
parser = argparse.ArgumentParser(description='parse the folders containing the different files')
parser.add_argument('-path', nargs='+', default = ['../output/output_2021-06-24_16-30/','../output/output_2021-06-24_15-56/',\
                                                 '../output/output_2021-06-24_15-11'], help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+',default = ['setup','master'], help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
parser.add_argument('-header', type=int, default = 1, help='header')
parser.add_argument('-title', type=str, default = 'Lead', help='title')
parser.add_argument('-labels', nargs='+', default = ['0mm', '40mm', '86mm'], help='labels per path.')
parser.add_argument('-bg', action='store_true', help='background?')


args = parser.parse_args()
paths = args.path
paths = [p+'/' if p[-1]!='/' else p for p in paths ]
print(paths)

files = [txthelper.getFileNames(path, args.ignore, args.filetype) for path in paths]

# get setup from first folder
setup_layer = txthelper.getSetup(paths[0])
setup = [detector.split('_')[0] for detector in setup_layer]



adcs = {detector : [[] for i in range(len(paths))] for detector in setup}
#time = [] #{detector : [] for detector in setup}
#mVs = {detector : [] for detector in setup}
#print(adcs,time)
    

# read in data
for j, path in enumerate(paths):
    for f in files[j]: 

        if '.txt' in f: f = f[:-4]
        rf = io.open('%s/%s.txt'%(path,f),encoding='utf-8')

        for i, line in enumerate(rf.readlines()):
                # skip header
                line = line.split(' ')
                if i < args.header : continue
                if len(line) == 1: continue
                # read in data
            
                detector = line[-2]
                adc = int(line[1])
                adcs[detector][j].append(adc)
                #mVs[detector].append(conv.adc2mv(detector,adc))
                #time.append(float(line[-1]))
  

#if not args.bg: time = [0.5*(abs(time[i+1]-time[i])+abs(time[i+2]-time[i+1])) for i in range(0,len(time)-1,3)]
    


def makeHist(data_list,labels,name='',bins=22,binrange=(50,600),\
                xlabel="ADC",ylabel="Entries / 25 ADC",title=args.title,
                normalize=True,path=args.path):
    """ seperate hists for listed data entries in one single figure """
    plt.figure()
    
    for i, data in enumerate(data_list): 
        labels[i]+=' median %.1f'%(np.median(data))
        plt.hist(data,bins=bins,range=binrange,label=labels[i],density=True,histtype='step')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig("%s/%s.png"%(path,name), dpi=300, bbox_inches='tight')
    print("%s/%s.png"%(path,name))


# separate ADC hists per detectors
for detector , adc_det in zip(setup_layer,adcs.values()):
    
    makeHist(data_list = adc_det,
    title = '%s %s'%(args.title,detector),
    labels = args.labels.copy(),
    name="%s_%s"%(detector,args.title), path = './')



# close the plot when pressing a key
plt.draw()
plt.pause(1)
input('press any key to close')
plt.close('all')



print('goodbye')