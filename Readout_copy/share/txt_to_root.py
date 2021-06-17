# convert all .txt in folder to single root file
# based on https://root.cern.ch/doc/v612/staff_8py.html by Wim Lavrijsen
# and https://gist.github.com/raggleton/0686060ed1e94894c9cf

#import re, array, os
import os

#import ROOT
#from ROOT import TFile, TTree, gROOT, AddressOf
import argparse
import array
from natsort import natsorted # for file name sorting
from sys import exit

# parse path
parser = argparse.ArgumentParser(description='convert all .txt in folder to single root file')
parser.add_argument('-path', type=str, required = True,
                    help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+', default = 'setup',
                    help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt',
                    help='Filetype to read in.')

args = parser.parse_args()
path = args.path



def getFileNames(path, ignore=args.ignore,filetype=args.filetype, verbose=True):
    
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
   
    
#print(files)

## A C/C++ structure is required, to allow memory based access
'''
gROOT.ProcessLine(
"struct staff_t {\
   Int_t      layer;\
   Int_t      adc;\
   Float_t    volt;\
   Float_t    temp;\
   Float_t    timediff;\
   Float_t    time;\
   Int_t      detector_muon_count;\
   Int_t      detector_count;\
   String     detector_name;\
};" );
'''
# Text_t ?



def readFiles(files, path=args.path):
    """ read in txt files and fill ROOT tree """
    
    
    # create ROOT file
    root_file = TFile("%s/output.root"%path, 'RECREATE' )
    
    # create tree
    tree = TTree('output', 'output for folder %s'%path)
    
    # pointers
    layer, adc = array('i', [0.]), array('i', [0.])
    volt, temp, timediff, time = array('f', [0.]), array('f', [0.]), array('f', [0.]), array('f', [0.])
    detector_muon_count, detector_count = array('i', [0.]), array('i', [0.])
    detector_name = array('s', [0.])
    
    # create branches FIXME
    
    tree.Branch( 'layers', layer, 'layer/I')
    tree.Branch( 'adc', adc, 'adc/I') # each one for MASTER X, Y, ...?
    tree.Branch( 'volt', volt, 'volt/F')
    tree.Branch( 'temp', temp, 'temp/F')
    tree.Branch( 'timediff', timediff, 'timediff/F')
    tree.Branch( 'time', time, 'time/F')
    tree.Branch( 'detector_muon_count', detector_muon_count, 'detector_muon_count/I')
    tree.Branch( 'detector_count', detector_count, 'detector_count/I')
    tree.Branch( 'detector_name', detector_name, 'detector_name/I')
    
    # iterate over all files
    for f in files:
        
        f_in = open('%s%s'%(path,f))
        for line in f_readlines():
            
            output.adc == tree.Fill() # how to group events FIXME
            
            if line = '': print()
    
 
    for line in open(fname).readlines():
        t = list(filter( lambda x: x, re.split( '\s+', line ) ) )
        staff.Category = int(t[0])             # assign as integers
        staff.Flag     = int(t[1])
        staff.Age      = int(t[2])
        staff.Service  = int(t[3])
        staff.Children = int(t[4])
        staff.Grade    = int(t[5])
        staff.Step     = int(t[6])
        staff.Hrweek   = int(t[7])
        staff.Cost     = int(t[8])
        staff.Division = t[9]                  # assign as strings
        staff.Nation   = t[10]
        tree.Fill()
    tree.Print()
    tree.Write()
    
    
#### run fill function if invoked on CLI
if __name__ == '__main__':
    files = getFileNames(path, args.ignore, args.filetype)
    readFiles(files, path)