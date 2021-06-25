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




def readHist(names, rfile, treename = 'output', bins=32, xmin = 0, xmax = 1024, ymax = None, xlabel = "ADC", ylabel = "Entries / 32 ADC", normalize = True, colors = [ROOT.kRed+1, ROOT.kBlue+1, ROOT.kBlack]):
    """ read hists (list branch names in *names*) from open ROOT file, save to open ROOT file """

    def getHist(branch, tree, bins=bins, xmin=xmin, xmax=xmax, normalize = normalize, ymax = ymax):
        """ get histogram out of branch from tree """
        tree.Draw("%s >> %s(%i,%i,%i)"%(branch,branch,bins,xmin,xmax)) # store branch in histogram
        hist = ROOT.gROOT.FindObject(branch) # get histogram
        if normalize: hist.Scale(1./hist.GetEntries())
        if ymax is not None: hist.SetMaximum(ymax)
        return hist
    
    def styleHist(hist, color,xlabel=xlabel, ylabel=ylabel):
        """ better visuals """
        hist.SetLineColor(color)
        hist.SetLineWidth(2)
        hist.GetXaxis().SetTitle("#font[52]{%s}"%xlabel)
        hist.GetYaxis().SetTitle("#font[52]{%s}"%ylabel)
        return hist

    # get tree
    tree = rfile.Get(treename)
    hists = [styleHist(getHist(name,tree), color) for color, name in zip(colors,names)]

    
    # draw
    c = ROOT.TCanvas()
    for hist in hists: hist.Draw("hist same")
        
    #sg.Draw("hist")
    #bg.Draw("hist same")
    c.BuildLegend() # make this better
    c.Update()
    c.Draw()
    

    # let the hists and cv exists outside of function
    #ROOT.SetOwnership(sg,False)
    #ROOT.SetOwnership(bg,False)
    for hist in hists: ROOT.SetOwnership(hist,False)
    ROOT.SetOwnership(c,False)
    
    # ave plot
    cname = ''
    for name in names: cname += name
    c.SaveAs("%s.C"%cname)
    c.SaveAs("%s.root"%cname)
    c.SaveAs("%s.PDF"%cname)
    return c

if __name__ == '__main__':

    #  make root look a bit better
    ROOT.gStyle.SetPadLeftMargin(0.14)  # make room for y-title, adjust with pad.SetLeftMargin()
    ROOT.gStyle.SetTitleOffset(1.8,"y") # adjust with histogram.GetYaxis().SetTitleOffset)
    ROOT.gROOT.SetStyle("ATLAS")  
    
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

    # signal background plots
    sg_bg_ADC = [readHist([detector,'%s_bg'%detector], rfile, ymax = 0.1) for detector in setup]
    sg_bg_mv = [readHist([detector,'%s_bg'%detector], rfile, ymax = 0.1) for detector in setup] # how to get mv FIXME
    #sg = [readHist([detector], rfile) for detector in setup] 
    #bg = [readHist(['%s_raw'%detector], rfile) for detector in setup] 
    # time differnce
    time = readHist(['timediff_cons1','timediff_cons2','timediff_total'], rfile, bins=50, xmin = 0., xmax = 0.5, xlabel = "Time difference [s]")
    # TODO check why this has weird limits
    
    # overlay detctors
    sg_mV = [readHist([detector,'%s_bg'%detector], rfile, ymax = 0.1) for detector in setup]

    # Close files
    rfile.Close()
    wfile.Close()

    input()
    print("Goodbye")
