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
parser.add_argument('--nsteps',type=int,default=10,required=False,
                    help='n steps per voltage')
parser.add_argument('--vsteps',type=float,default=0.01,required=False,
                    help='voltage step')
                    
# output file
parser.add_argument('--fpath',type=str,default='../data/',required=False,
                    help='filepath, default ../data/')
parser.add_argument('--fname',type=str,default='test',required=False,
                    help='csv filename, default "", no need to add .txt')
args = parser.parse_args()



# open a file to write to
savefile = open(args.fpath+args.fname+'.txt','a')

# open connection to detector
d = serial.Serial(port=args.p,baudrate=9600, timeout = 1)

# open connection to signal generator
t = TTi_TG5011.TTi_TG5011(args.tti)

# select calibration waveform (needs to be transfered by USB -> Noor)

a = args.vmin

t.setAmplitude(a-.01)
t.setFrequency(1)
t.setArbWaveform('ARB1')
t.burstCount(1)
t.enableOutput('ON')
t.burst('OFF')
time.sleep(3)


# read header
header_l = 5
for l in range(header_l): 
    data = d.readline().replace(b'\r\n',b'').decode('utf-8')
    print(data)
    savefile.write(data+'\n')
print('read header, start calibration')

i = 0 
while True:
    try:
        # read the data (byte) as utf8
        data = d.readline().replace(b'\r\n',b'').decode('utf-8')
        print(data)
        savefile.write(data+'\n')

        # increase amplitude every nsteps
        if i%args.nsteps==0: 
            a+=args.vsteps
            if a >= args.vmax+.01: break
            print('increasing amplitude to %.2f V'%a)
            savefile.write("SET AMPLITUDE %s\n"%a)
            t.setAmplitude(a)
            t.syncOut('ON')
            time.sleep(1)
            
        # trigger
        t.burst('NCYC')
        t.burst('OFF')
        time.sleep(2)
        
        i+=1   
        
    # halfly graceful exit... 
    except KeyboardInterrupt:
        break

savefile.close()
print('Saved file to:\npath: %s\nname: %s'%(args.fpath,args.fname))       
print('Goodbye')