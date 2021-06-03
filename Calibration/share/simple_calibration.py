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


parser = argparse.ArgumentParser(description='Calibration script')
# ports
parser.add_argument('-p',type=str,default='/dev/ttyUSB0',required=False,
                    help='detector port. dont forget to give rw access with sudo chmod 666 <port>')
parser.add_argument('-tti',type=str,default='/dev/ttyACM0',required=False,
                    help='signal generator port (type ACM*)')
# calibration
parser.add_argument('-vmin',type=float,default=0.02,required=False,
                    help='minimum calibration signal voltage [V]')
parser.add_argument('-vmax',type=float,default=0.33,required=False,
                    help='maximum calibration signal voltage [V]')
parser.add_argument('-nsteps',type=int,default=10,required=False,
                    help='n steps per voltage')
parser.add_argument('-vsteps',type=float,default=0.01,required=False,
                    help='voltage step')
parser.add_argument('-period',type=float,default=0.5,required=False,
                    help='injection period [s]')
parser.add_argument('-header',type=int,default=1,required=False,
                    help='header length to read before injection')
# output file
parser.add_argument('-fpath',type=str,default='../data/',required=False,
                    help='filepath, default ../data/')
parser.add_argument('-fname',type=str,default='test',required=False,
                    help='csv filename, default "test", no need to add .txt')
args = parser.parse_args()



# open a file to write to
savefile = open(args.fpath+args.fname+'.csv','w')

# open connection to detector
d = serial.Serial(port=args.p,baudrate=9600, timeout = 1)

# open connection to signal generator
t = TTi_TG5011.TTi_TG5011(args.tti)

# select calibration waveform (needs to be transfered by USB -> Noor)
amp = args.vmin

t.enableOutput('OFF')
t.setAmplitude(amp)

t.setFrequency(1e6) # 1MHz
t.setBurstPhase(340) # degree
t.setBurstPeriod(args.period) # seconds
t.setBurstCount(1)
t.setArbWaveform('ARB1')


# read header
for l in range(args.header): 
    data = d.readline().replace(b'\r\n',b'').decode('utf-8')
    print(data)
    savefile.write(data+'\n')



print('read in header, start calibration')

savefile.write("AMPLITUDE, %s\n"%amp)

t.enableOutput('ON')
i = 0 
while True:
    try:     
        # read the data (byte) as utf8
        data = d.readline().replace(b'\r\n',b'').decode('utf-8')
        print(data)
        savefile.write(data+'\n')

        # increase amplitude every nsteps
        if i>0 and i%args.nsteps==0: 
            amp+=args.vsteps
            if amp >= args.vmax+args.vsteps: break

            t.enableOutput('OFF')                        
            print('increasing amplitude to %.2f V'%amp)
            savefile.write("AMPLITUDE, %s\n"%amp)
            t.setAmplitude(amp)
       
            time.sleep(1)
            t.enableOutput('ON')

        i+=1   
        
    # halfly graceful exit... 
    except KeyboardInterrupt:
        t.enableOutput('OFF')
        break

savefile.close()
print('Saved file to:\npath: %s\nname: %s'%(args.fpath,args.fname))       
print('Goodbye')
