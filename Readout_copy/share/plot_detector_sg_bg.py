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


def readHist(name, rfile, treename = 'output', bins=256, xmin = 0, xmax = 1024):
    """ read hist from open ROOT file, save to open ROOT file """

    def getHist(branch, tree, bins=bins, xmin=xmin ,xmax=xmax):
        """ get histogram from tree """
        tree.Draw("%s >> %s(%i,%i,%i)"%(branch,branch,bins,xmin,xmax)) # store branch in histogram
        hist = ROOT.gROOT.FindObject(branch) # get histogram
        return hist
    
    def styleHist(hist, color,xlabel="ADC", ylabel="Entries"):
        """ better visuals """
        hist.SetLineColor(color)
        hist.SetLineWidth(2)
        hist.GetXaxis().SetTitle("#font[52] %s"%xlabel)
        hist.GetXaxis().SetTitle("#font[52] %s"%ylabel)
        return hist

    # get tree
    tree = rfile.Get(treename)
    
    sg = getHist(name, tree)
    sg = styleHist(sg, ROOT.kRed+1)
    
    bg = getHist("%s_raw"%name, tree)
    bg = styleHist(bg, ROOT.kBlue+1)
    
    # draw
    c = ROOT.TCanvas()
    sg.Draw("hist")
    bg.Draw("hist")
    c.BuildLegend()
    c.Update()
    c.Draw()

    # let the hists and cv exists outside of function
    ROOT.SetOwnership(sg,False)
    ROOT.SetOwnership(bg,False)
    ROOT.SetOwnership(c,False)
    return c
    

# parse path
parser = argparse.ArgumentParser(description='display signal and background ADC and mV histograms read from root file')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-name', type=str, default = '', help='File to read in.')
#parser.add_argument('-detectors', nargs='+',type=str,default = ['all'], help='detectors to display, default all')

# io
args = parser.parse_args()
path = args.path
if path[-1]!='/': path+='/'
name = args.name
if name[-5:]!='.root': name+='.root'


# open ROOT file to read ...
rfile = ROOT.TFile.Open(path+name ,"READ")
# ... and one to save the hist to
wfile = ROOT.TFile(path+name[:-5]+'_hist.root', 'RECREATE' )

setup = helper.getSetup(path, filetye='.txt', name = 'grid_setup')
#print("file contains detectors:")
#for d in setup: print(d)
#detectors = setup if args.detectors[0]=='all' else args.detectors
#print("reading in ",detectors)

cvs = [readHist(detector) for detector in setup] 



# Close files
rfile.Close()
wfile.Close()

input()
print("Goodbye")
