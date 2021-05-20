# simple calibration script
# - connect detector via usb (--p)
# - connect signal generator (TG5011(A)) via usb 
#
# @haslbeck
# May 2021
import serial
import argparse
import TTi_TG5011
import time


parser = argparse.ArgumentParser(description='simple readout')
# ports
parser.add_argument('--p',type=str,default='/dev/ttyUSB0',required=False,
                    help='detector port. dont forget to give rw access with sudo chmod 666 <port>')
parser.add_argument('--tti',type=str,default='/dev/ttyACM0',required=False,
                    help='signal generator port (type ACM*)')
# calibration
parser.add_argument('--vmin',type=float,default=0.02,required=False,
                    help='minimum calibration signal voltage [V]')
parser.add_argument('--vmax',type=float,default=1.0,required=False,
                    help='maximum calibration signal voltage [V]')
parser.add_argument('--n',type=int,default=10,required=False,
                    help='n steps per voltage')
                    
# output file
parser.add_argument('--fpath',type=str,default='../data/',required=False,
                    help='filepath, default ../data/')
parser.add_argument('--fname',type=str,default='test',required=False,
                    help='csv filename, default "", no need to add .txt')
args = parser.parse_args()


# open a file to write to
savefile = open(args.fpath+args.fname+'.txt','a')

# open connection to detector
d = serial.Serial(port=args.p,baudrate=9600)

# open connection to signal generator
t = TTi_TG5011.TTi_TG5011(args.tti)
# select calibration waveform (needs to be transfered by USB -> Noor)
a = args.vmin
t.setArbWaveform('AXP_BRB')
t.setAmplitude(a)
t.enableOutput('ON')
t.burstCount(1) # 
t.burst('OFF')

# read header outside of loop? FIXME
#for i in range(7):
#    data = d.readline().replace(b'\r\n',b'').decode('utf-8')
#    print(data)
#    savefile.write(data+'\n')
# i = 0

i = -5 # to readout for the headers fastly
while True:
    try:
        # read the data (byte) and transform to utf8
        data = d.readline().replace(b'\r\n',b'').decode('utf-8')
        print(data)
        savefile.write(data+'\n')

        # increase amplitudes every steps after reading header
        if i%args.nsteps==0 and i > 0 : 
            a+=.01
            print('increasing amplitude to %.2f V'%a)
            savefile.write("SET AMPLITUDE %s\n"%a)
            t.setAmplitude(a)
            t.syncOut('ON')
            
        # trigger after header has been read
        if i >= 0:
            t.burstCount(1)
            t.burst('NCYC')
            t.burst('OFF')
            time.sleep(1)
            
        if a == args.vmax: break
        i+=1   
        
    # halfly graceful exit... 
    except KeyboardInterrupt:
        savefile.close()
        print('Saved file to:\npath: %s\nname: %s'%(args.fpath,args.fname))        
        break

print('Goodbye')
