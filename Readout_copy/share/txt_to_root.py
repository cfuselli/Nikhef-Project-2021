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
        
#Text_t



def readFiles(files, setup, path=args.path, verbose = True):
    """ read in txt files and fill ROOT tree """
    
    
    # create ROOT file
    root_file = ROOT.TFile("%s/output.root"%path, 'RECREATE' )
    
    # create tree
    tree = ROOT.TTree('output', 'output for folder %s'%path)
    
    # pointers
    number, time, timediff, temp = array('i', [0]), array('f', [0.]), array('f', [0.]), array('f', [0.])
    adcs = {detector: array('f', [0.]) for detector in setup}
    
    # create branches 
    
    tree.Branch( 'number', number, 'number/I')
    tree.Branch( 'timediff', timediff, 'timediff/F')
    tree.Branch( 'time', time, 'time/F')
    tree.Branch( 'temp', temp, 'temp/F')

    for (detector, pointer) in adcs.items():
        print("%s/F"%detector)
        tree.Branch(detector, pointer, "%s/F"%detector)
    print("Created branches...")
    
    
    # iterate over all files
    for nf, f in enumerate(files):

        # open file
        print('Processing %s (%i/%i)'%(f,nf+1,len(files)))
        f_in = open('%s%s'%(path,f))
        f_in.readline()  # skip header

        # read data
        i = 1
        for line in f_readlines():
            line  = line.split(' ')
            print(line)

            # fill tree for each event
            if len(line) == 1:
                number[0] = i
                tree.Fill()
                for detector in adcs: adcs[detector][0] = 0.
                i += 1    
            
            layer, name = line[0], line[-1]
            
            # assign to pointers
            temp[0], timediff[0], time[0] = line[3], line[4], line[5]
            # # # # # # 
            # FIXME adc to mV and energy conversion....
            # # # # # #
            adcs["%s_%s"%(name,layer)][0] = adc

        f.close()    
        tree.Print()
        tree.Write()
    
    

if __name__ == '__main__':
    files = getFileNames(path, args.ignore, args.filetype)
    setup = getSetup(path)
    readFiles(files, setup, path)
    
