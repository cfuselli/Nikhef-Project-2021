# convert all .txt in folder to single root file
# based on https://root.cern.ch/doc/v612/staff_8py.html by Wim Lavrijsen
# and https://gist.github.com/raggleton/0686060ed1e94894c9cf
#
# @haslbeck
# 18 June 2021 

#import re, array, os
import os

import ROOT
#from ROOT import TFile, TTree, gROOT, AddressOf
import argparse
from array import array
from natsort import natsorted # for file name sorting
from sys import exit
import io

# parse path
parser = argparse.ArgumentParser(description='convert all .txt in folder to single root file')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+',default = ['setup'], help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
parser.add_argument('-cw', type=float, default = 0.5, help='acceptance time window for two consecutive readings')
parser.add_argument('-tw', type=float, default = 1.5, help='total acceptance for a muon')

args = parser.parse_args()
path = args.path



def getFileNames(path, ignore=args.ignore,filetype=args.filetype):
    """ get all file names in given path according to some criteria, requires feeback by user """
    
    files = os.listdir(path) # get file names
    files = [f for f in files if filetype in f] # only consider files of corect type
    for ign in ignore: files = [f for f in files if ign not in f] # remove files with ignore key
    files = natsorted(files, key=lambda y: y.lower()) # natural sort of file names

    print("read in files at %s ... ?"%path)
    for f in files: print("%s"%f)
    
    # give feedback what files have been read
    while True:
        usr = input('continue y/N:\n')
        if 'N' in usr: exit()
        elif 'y' in usr: break
        else: continue
        
    return files

def getSetup(path, filetye=args.filetype, name = 'grid_setup'):
    """ extract the used detectors from grid_setup.txt file """
    setup = []
    f = io.open("%s%s.txt"%(path,name), encoding = 'utf-8')
    for line in f.readlines():
        line = line.split(' ')
        if len(line) <= 1 : break
        # store layer
        layer , name = line[0], line[-1][:-1]  # dont store '\n'
        setup.append("%s_%s"%(name,layer))
    f.close()
    # remove date
    setup = setup[1:]
    return setup



def readFiles(files, setup, path=args.path, verbose = True):
    """ read in txt files and fill ROOT tree """

    # create ROOT file
    root_file = ROOT.TFile("%s/output.root"%path, 'RECREATE' )
    
    # create tree
    tree = ROOT.TTree('output', 'output for folder %s'%path)
    
    # pointers
    number, time = array('i', [0]), array('s', [0.])
    timediff_cons1, timediff_cons2, timediff_total = array('f', [0.]), array('f', [0.]), array('f', [0.])
    temp =  array('f', [0.])
    # dict of pointer, each detector has own key
    adcs = {detector: array('f', [0.]) for detector in setup}
    
    # create branches 
    tree.Branch( 'number', number, 'number/I')
    tree.Branch( 'time', time, 'time/S')
    tree.Branch( 'timediff_cons1', timediff, 'timediff_cons1/F')
    tree.Branch( 'timediff_cons2', timediff, 'timediff_cons2/F')
    tree.Branch( 'timediff_total', timediff, 'timediff_total/F')
    tree.Branch( 'temp', temp, 'temp/F')

    for (detector, pointer) in adcs.items():
        print("%s/F"%detector)
        tree.Branch(detector, pointer, "%s/F"%detector)
    print("Created branches...")
    
    
    # iterate over all files
    for nf, f in enumerate(files):

        # open file
        print('Processing %s (%i/%i)'%(f,nf+1,len(files)))
        f_in = io.open('%s%s'%(path,f), encoding='utf-8')
        f_in.readline()  # skip header

        # read data
        
        # # # # # # 
        # FIXME adc to mV and energy conversion....
        # # # # # #
        
        # new event 
        layer_1before, detector_1before = None, None
        layer_2before, detector_2before = None, None
        timediff_now , timediff_before = None, None
        
        event = 0
        for l_id, line in enumerate(f_in.readlines()):
            line  = line.split(' ')
            print(line)
            
            # define new event
            # fill tree for each event
            
            # could this be a muon? 
            layer, detector , timediff_now = int(line[0]), line[-2], float(line[4])
            
            # save the adc to the corresponding branch
            adcs["%s_%s"%(detector,layer)][0] = int(line[1])
            
            # check layers and detectors
            if (detector_1before != detector_2before): # remove 2 consecutive detector readings
                if (detector != detector_1before) and (detector != detector_2before): # 3 different detectors ...
                    if (layer_1before != layer_2before) and (layer != layer_1before) and (layer != layer_2before): # .. in 3 different layers
                    # check the time difference
                        _tot_time = timediff_now + timediff_before
                        if timediff_now <= args.cw and _tot_time <= args.tw:
                            # if we are here we have three ... save the event
                            event += 1
                        
                            number[0] = event
                            timediff_cons[0]  = timediff_now
                            timediff_total[0] = _tot_time
                            temp[0] = float(line[3])
                            tree.Fill()
            
            # assign to pointers
            #temp[0], timediff[0] = float(line[3]), float(line[4])
            #adcs["%s_%s"%(detector,layer)][0] = int(line[1])
            
            
            #temp[0], timediff[0], time[0] = float(line[3]), float(line[4]), float(line[5])
            
            
            
            
            layer_2before, detector_2before = layer_1before, detector_1before
            layer_1before, detector_1before = layer, detector
            timediff_before = timediff_now 
            '''
            if len(line) == 1:
                number[0] = i
                tree.Fill()
                for detector in adcs: adcs[detector][0] = 0.
                i += 1
                continue
            '''

        f_in.close()    
        tree.Print()
        tree.Write()
    
    

if __name__ == '__main__':
    files = getFileNames(path, args.ignore, args.filetype)
    setup = getSetup(path)
    readFiles(files, setup, path)
    
