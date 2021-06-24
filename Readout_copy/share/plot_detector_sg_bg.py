# diplay signal and background ADC and mV histograms read from root file
#
# @haslbeck
# 24 June 2021

import os
import ROOT
import argparse
from array import array
from natsort import natsorted # for file name sorting
from sys import exit
import io 
import copy
import txt_to_root_matching_withbg as helper

print("asdfasf")

# parse path
parser = argparse.ArgumentParser(description='display signal and background ADC and mV histograms read from root file')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-name', type=str, default = '', help='File to read in.')
parser.add_argument('-detectors', nargs='+',type=str,default = ['all'], help='detectors to display, default all')

# io
args = parser.parse_args()
path = args.path
if path[-1]!='/': path+='/'
name = args.name
if name[-5]!='.root': name+='.root'


# open ROOT file to read ...
rfile = ROOT.TFile.Open(path+name ,"READ")
# ... and one to save the hist to
wfile = ROOT.TFile(path+name[:-5]+'_hist.root', 'RECREATE' )

setup = helper.getSetup(path, filetye='.txt', name = 'grid_setup')

print(setup)



# Close files
rfile.Close()
wfile.Close()
