# convert all .txt in folder to single root file
# based on https://root.cern.ch/doc/v612/staff_8py.html by Wim Lavrijsen
# and https://gist.github.com/raggleton/0686060ed1e94894c9cf
#
# # # # # #
# FIXME adc to mV and energy conversion....
# # # # # #
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
import copy


def getFileNames(path, ignore=['setup','data'],filetype='.txt'):
    """ get all file names in given path according to some criteria, requires feeback by user """
    
    files = os.listdir(path) # get file names
    files = [f for f in files if filetype in f] # only consider files of corect type
    for ign in ignore: files = [f for f in files if ign not in f] # remove files with ignore key
    files = natsorted(files, key=lambda y: y.lower()) # natural sort of file names

    print("read in files at %s ... ?"%path)
    for f in files: print("%s"%f)
    
    # give feedback what files have been read
    while True:
        usr = input('continue y/n:\n')
        if 'n' in usr: exit()
        elif 'y' in usr: break
        else: continue
        
    return files

def getSetup(path, filetye='.txt', name = 'grid_setup'):
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


def readFiles(files, setup, path='../output/', cw = 0.1, tw = 0.4):
    """ read in txt files and fill ROOT tree """

    # create ROOT file
    root_fname = "%s/output_cw_%.2f_tw_%.2f.root"%(path,cw,tw)
    root_file = ROOT.TFile(root_fname, 'RECREATE' )
   
    # create tree
    tree = ROOT.TTree('output', 'output for folder %s, consecutive window %f s total window %f s'%(path,cw,tw))
    
    # pointers
    ##number, time = array('i', [0]), std.string
    number = array('i', [0])
    timediff_cons1, timediff_cons2, timediff_total = array('f', [-1.]), array('f', [-1.]), array('f', [-1.])
    temp =  array('f', [-1.])

    # muons: dict of pointer, each detector has own key
    adcs = {detector: array('i', [-1]) for detector in setup}
    adcs_buff = {detector: array('i', [-1]) for detector in setup}
    # 
    mv = {"%s_mV"%detector: array('f', [-1]) for detector in setup}
    mv_buff = {"%s_mV"%detector: array('f', [-1]) for detector in setup}

    # all events dict of pointer, each detector has own key
    adcs_raw = {"%s_bg"%detector: array('i', [-1]) for detector in setup}
    mv_raw = {"%s_bg"%detector: array('f', [-1]) for detector in setup}

    
    # create branches ...
    tree.Branch( 'number', number, 'number/I')
    tree.Branch( 'timediff_cons1', timediff_cons1, 'timediff_cons1/F')
    tree.Branch( 'timediff_cons2', timediff_cons2, 'timediff_cons2/F')
    tree.Branch( 'timediff_total', timediff_total, 'timediff_total/F')
    tree.Branch( 'temp', temp, 'temperature/F')
    
    # ... muons
    for (detector, pointer) in adcs.items(): tree.Branch(detector, pointer, "%s/I"%detector)
    for (detector, pointer) in mv.items():   tree.Branch(detector, pointer, "%s/F"%detector) 
    # ... and events
    for (detector, pointer) in adcs_raw.items(): tree.Branch(detector, pointer, "%s/I"%detector)
    for (detector, pointer) in mv_raw.items():   tree.Branch(detector, pointer, "%s/F"%detector)

    
    print("Created branches for detectors...")
    for key in adcs: print(key)
    
    
    tot_event = 0
    # new event 
    layer_1before, detector_1before = None, None
    layer_2before, detector_2before = None, None
    timediff_now, timediff_before = None, None
    
    # iterate over all files
    for nf, f in enumerate(files):

        #if nf > 0:
        #    print(" read only one file ")
        #    break
        
        # open file
        f_in = io.open('%s%s'%(path,f), encoding='utf-8')
        f_in.readline()  # skip header

        # read data
        event = 0
        
        for l_id, line in enumerate(f_in.readlines()):
            line  = line.split(' ')

            #print(l_id)

            #if l_id > 20:
            #    print("  ")
            #    break
            #if event > 5: break
              

            # define new event -  could this be a muon? 
            layer, detector , timediff_now = int(line[0]), line[-2], float(line[4])
            
            # raw adcs are always filled
            #print("raw adc: ","%s_%s_raw"%(detector,layer))
            adcs_raw["%s_%s_sg"%(detector,layer)][0] = int(line[1])
            #mv_raw["%s_%s_sg"%(detector,layer)][0] = #
            
            # buffer the save the adc to the corresponding branch in order not to count events multiple times for non-muons
            adcs_buff["%s_%s"%(detector,layer)][0] = int(line[1])

            
            # check layers and detectors
            # remove 2 consecutive detector readings
            # 3 different detectors ...
            # .. in 3 different layers
            # check the time difference
            if (( detector_1before != detector_2before ) and
               ( detector != detector_1before ) and ( detector != detector_2before ) and
               ( layer_1before != layer_2before ) and ( layer != layer_1before ) and ( layer != layer_2before ) and 
               ( timediff_now <= cw ) and ( timediff_before <= cw ) and (timediff_now + timediff_before) <= tw ):              
                          
                            # if we are here we have three ... save the event
                            event += 1
                            #print(">>>> %i muon %i<<<<"%(l_id,event))

                            # use pointers to fill the tree
                            number[0] = event
                            timediff_cons2[0] = timediff_before
                            timediff_cons1[0] = timediff_now
                            timediff_total[0] = timediff_now + timediff_before                            
                            temp[0] = float(line[3])
                            adcs = copy.deepcopy(adcs_buff) # fill the buffer, nested dict requires deepcopy
                            
                            tree.Fill()

                            # clear up the pointers so we dont accidentally fill sth twice
                            number[0] = -1
                            timediff_cons2[0] = -1.
                            timediff_cons1[0] = -1.
                            timediff_total[0] = -1.
                            temp[0] = -1.

                            for det in adcs:
                                adcs[det][0] = -1
                                adcs_buff[det][0] = -1
                            for det in adcs_raw: adcs_raw[det][0] = -1

                            #print("cleaned up after muon")
                            #print("adcs")
                            #for det,val in adcs.items(): print(det,val)
                            #print("adcs buff")
                            for det,val in adcs_buff.items(): print(det,val)
                            #print("adcs raw")
                            #for det,val in adcs_raw.items(): print(det,val)
                            
                        
                                
            else:
                # no muon detected, save the adc for background
                #for detector,value in adcs_raw.items():
                #    print("no muon, fill",detector, value)
                #print("<<<<<< no muon, fill >>>>")
                #for det,val in adcs.items(): print(det,val)
                
                tree.Fill()
                for det in adcs_raw: adcs_raw[det][0] = -1

                #print("<<<< %i skipped >>>>>: "%(l_id))
                #print(timediff_before, timediff_now)
                #print(layer, layer_1before, layer_2before)
                #print(detector, detector_1before, detector_2before)
                

            #try:
            #    print( ( detector_1before != detector_2before ) , ( detector != detector_1before ) , ( detector != detector_2before ) )
            #    print( (layer_1before != layer_2before ) , ( layer != layer_1before ) , ( layer != layer_2before ) ) 
            #    print( (timediff_now <= args.cw ) , ( timediff_before <= args.cw ) , (timediff_now + timediff_before) <= args.tw )
            #except: pass
            
            layer_2before, detector_2before = layer_1before, detector_1before
            layer_1before, detector_1before = layer, detector
            timediff_before = timediff_now
            pass
        
        print('Processed %s (%i/%i)'%(f,nf+1,len(files)),"muon events: ",f,event)
           
        f_in.close()
        tot_event+=event
        #tree.Write()
        tree.Write("", ROOT.TFile.kOverwrite)

      
    root_file.Write()
    root_file.Close()
    print("saved to %s"%(root_fname))
    print("read in %s"%path)
    print("consecutive window: %.4f s"%cw)
    print("total window:       %.4f s"%tw)
    print("total muon events: ",tot_event)
    print("="*30)
    

if __name__ == '__main__':
    
    # parse path
    parser = argparse.ArgumentParser(description='convert all .txt in folder to single root file')
    parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
    parser.add_argument('-ignore', nargs='+',default = ['setup','data'], help='file name patterns to ignore.')
    parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
    parser.add_argument('-cw', type=float, default = 0.1, help='acceptance time window for two consecutive readings')
    parser.add_argument('-tw', type=float, default = 0.4, help='total acceptance for a muon')

    args = parser.parse_args()
    path = args.path
    if path[-1]!='/': path+='/'
    
    files = getFileNames(path, args.ignore, args.filetype)
    setup = getSetup(path)
    readFiles(files, setup, path, args.cw, args.tw)
    
