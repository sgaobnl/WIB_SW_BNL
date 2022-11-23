import numpy as np
import pickle
from tools import Tools
import matplotlib.pyplot as plt


fp ="../data/Raw_SW_Trig19_11_2022_22_48_23.bin"
with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
print(len(rawdata))

tl=Tools()
ch_data = tl.data_ana(rawdata)   # return data is a numpy array, axis=0: event No., axis=1: Chan No, axis=2: ADC bit
ch_rms = np.std(ch_data, axis =(0,2) )  # rms for each channel

#uplane=[]*476
#vplane=[]*476
#xplane=[]*584
uplane = np.zeros(476)
vplane = np.zeros(476)
xplane = np.zeros(584)

for i in range(1536):
    nfemb = i//128 + 1
    nch = i %128

    dfmap = tl.LoadMap(nfemb)
    plane,strip = tl.FindStrips(dfmap, nfemb, nch)
    #print(i, plane, strip)

    if plane==1:
       uplane[strip-1]=ch_rms[i]
    if plane==2:
       vplane[strip-1]=ch_rms[i]
    if plane==3:
       xplane[strip-1]=ch_rms[i]

xx=range(1536)
#plt.plot(xx, ch_rms)
ch_rms_map = np.concatenate((uplane,vplane,xplane))
plt.plot(xx, ch_rms_map)
plt.axvline(x=475, color = 'r', linestyle='--')
plt.axvline(x=951, color = 'r', linestyle='--')

plt.show()

