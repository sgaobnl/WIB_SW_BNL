import sys
import numpy as np
import pickle
import time, datetime, random, statistics

####################FEMBs Data taking################################
fp =  "D:/debug_data/Raw_MULTCONFIG_03_08_2022.bin"
#fp =  "D:/debug_data/Raw_CALI_200mVBL_14_0mVfC_2_0us_0x2c_03_08_2022.bin"

with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
cfg_paras_rec = raw[2]

#power measurement result
print (pwr_meas)
#configuration for this run of data
print (cfg_paras_rec)

def data_valid (raw):
    sss  = []
    for rawi in raw:
        ts = rawi[0]
        ss = rawi[1]
        chns = []
        for link in range(2):
            tv = [0]
            for i in range(len(ts[link])-1):
                t0 = int(ts[link][i])>>32>>21
                t1 = int(ts[link][i+1])>>32>>21
                if (abs(t1-t0) > 2) and (t1 != 0x000) and (t0 !=0x3ff):
                    tv.append(i)
            tv.append(len(ts[link])-1)
            tg = []
            for tvi in range(len(tv)-1):
                tg.append(tv[tvi+1]-tv[tvi])
            pos = np.where(tg == np.max(tg))[0][0]

            for chi in range(len(ss[0+link*2])):
                chns.append(ss[0+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
            for chi in range(len(ss[1+link*2])):
                chns.append(ss[1+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
        sss.append(chns)
    return sss 

#sss: 2D array [chn_no 0 to 511] [sample1, sample2, ...]
sss = data_valid(rawdata)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10,6))
ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
axs = [ax1, ax2, ax3, ax4]

N = 0
ss = sss[N]
fembs=[0, 1,2,3]
for fembi in fembs:
    for chi in range(128):
        x = (np.arange(len(ss[fembi*128 + chi]))) * 0.5
        axs[fembi].plot(x, ss[fembi*128 + chi], marker = '.')
        axs[fembi].set_xlabel("Time / $\mu$s")
        axs[fembi].set_ylabel("ADC /bin")
        axs[fembi].set_title(f"FEMB{fembi}")
plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
plt.show()
plt.close()

