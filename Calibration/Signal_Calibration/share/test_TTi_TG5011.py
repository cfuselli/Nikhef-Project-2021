# a simple scrip to test the TTi TG5011 class

import TTi_TG5011
import time 


#t = TTi_TG5011.TTi_TG5011("/dev/tty.usbmodemC28D26971")
t = TTi_TG5011.TTi_TG5011("/dev/ttyACM0")

t.setVerbose(True)

#print("init")
#t.init()
print('set waveform')
tstart = time.time()
#t.setArbWaveform('ARB2')
input("press any key")
print(tstart-time.time())


#t.setWaveType('PULSE')
#t.setFrequency(1123e-3)
print("set PULSE")
#t.setWaveType('PULSE')

print("set SINE")
t.setWaveType('SINE')
t.enableOutput('OFF')
#t.setOutputLoad(55)

print("going in the loop")

for i in range(1,3):
    tstart = time.time()
    v = i/10
    print(v)
    t.setAmplitudeUnit('VRMS')
    t.setAmplitude(v)
    t.setFrequency(v)
   
    #if i%2==0: 
    #    print("set PULSE")
    #    t.setWaveType('PULSE')
    #else: 
    #    print("set SINE")
    #    t.setWaveType('SINE')
    input("press any key")
    print(tstart-time.time())


#print("get model")
#print(t.getModel())
#print("set output ON")
#t.enableOutput("ON")

#print("set output OFF")
#t.enableOutput("OFF")

#t.beep()

#t.setLocal()

#print(t.getStatus())

#t.clearStatus()
#t.setOutputLoad(1243)
#t.clearStatus()
#t.setPulseFrequency(145)

'''
t.setVoltageLimit(1,15.1)
t.setCurrentLimit(1,0.15)
t.setVoltage(1,12)
t.enableOutput(1,True)
time.sleep(5)

print(t.getVoltage(1))
time.sleep(5)
t.enableOutput(1,False)
'''
