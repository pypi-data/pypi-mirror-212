import time as _time
import numpy as np
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti
from threading import Thread

amti.AMTIUSBDevice.InitializeLibrary(dll_path="./tests/bin/AMTIUSBDevice - 64.dll")
a = amti.AMTIUSBDevice("gen5")
a.init()

a.broadcastStart()
samples = 0
val = np.empty((0,a.getDeviceCount()*a.data_format[1]))

for i in range(0, 1000):
    _time.sleep(0.05)
    
    t, b = a.getData(opt=1)
    samples += b
    val = np.round(np.append(val, t, axis=0),2)

a.broadcastStop()

print(samples)
for row in val:
    print(row)
    _time.sleep(0.250)
    
    
del a
