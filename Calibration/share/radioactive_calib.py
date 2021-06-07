# calibration script for radioactive sources
# - connect detector via usb (--p)
# - 
# @haslbeck
# june 2021
import serial
import argparse
import time


parser = argparse.ArgumentParser(description='Radioactive Calibration script')
# ports
parser.add_argument('-p',type=str,default='/dev/ttyUSB0',required=False,
                    help='detector port. dont forget to give rw access with sudo chmod 666 <port>')
# calibration
parser.add_argument('-tmax',type=float,default=None,required=False,
                    help='maximum time to record [s]')
parser.add_argument('-nmax',type=int,default=None,required=False,
                    help='max data points to record')
parser.add_argument('-pause',type=float,default=0.5,required=False,
                    help='injection period [s]')
parser.add_argument('-header',type=int,default=6,required=False,
                    help='header length to read before injection. For OLED.ino: 6')
# output file
parser.add_argument('-fpath',type=str,default='../data/',required=False,
                    help='filepath, default ../data/')
parser.add_argument('-fname',type=str,default='test',required=False,
                    help='csv filename, default "test", no need to add .csv')
args = parser.parse_args()



# open a file to write to
savefile = open(args.fpath+args.fname+'.csv','w')

# open connection to detector
d = serial.Serial(port=args.p,baudrate=9600, timeout = None)

# read header
for l in range(args.header): 
    data = d.readline().replace(b'\r\n',b'').decode('utf-8')
    print(data)
    savefile.write(data+'\n')
print('read in header, start calibration')


tstart = time.time()
i = 0 
while True:
    try:   
        
        # check for break conditions
        if args.nmax is not None: 
            if i > args.nmax: break
        if args.tmax is not None:
            if time.time() - tstart > args.tmax: break
        
        # read the data (byte) as utf8
        data = d.readline().replace(b'\r\n',b'').decode('utf-8')
        print(data)
        savefile.write(data+'\n')
        time.sleep(args.pause)

        i+=1   
        
    # halfly graceful exit... 
    except KeyboardInterrupt:
        break

print("="*20)
print("Total events: %i"%i)
print("Total time:   %s s"%(time.time()-tstart))

savefile.close()
print('Saved file to:\npath: %s\nname: %s'%(args.fpath,args.fname))
print('Goodbye')
