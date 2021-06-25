import argparse
import numpy as np
import txt_to_root_matching_withbg as txthelper
import converter



    
    # parse path
parser = argparse.ArgumentParser(description='convert all .txt in folder to single root file')
parser.add_argument('-path', type=str, required = True, help='relative path to txt files to be read in.')
parser.add_argument('-ignore', nargs='+',default = ['setup','master'], help='file name patterns to ignore.')
parser.add_argument('-filetype', type=str, default = '.txt', help='Filetype to read in.')
#parser.add_argument('-cw', type=float, default = 0.1, help='acceptance time window for two consecutive readings')
#parser.add_argument('-tw', type=float, default = 0.4, help='total acceptance for a muon')

args = parser.parse_args()
path = args.path
if path[-1]!='/': path+='/'

files = txthelper.getFileNames(path, args.ignore, args.filetype)
setup = txthelper.getSetup(path)

print(setup,files)


counts = {detector : [] for detector in setup}
print(counts)
    

'''
for f in files: 
    
    if '.csv' in f: f = f[:-4]
    
    timestamp, adc = [], []
    with open(args.path+ f + '.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, line in enumerate(reader):
            # skip header
            if i < args.header : continue
            # read in data
            timestamp.append(float(line[0]))
            adc.append(float(line[1]))
'''