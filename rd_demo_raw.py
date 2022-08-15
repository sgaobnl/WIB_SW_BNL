import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt


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
            print (tv[pos],tv[pos+1])


            for chi in range(len(ss[0+link*2])):
                chns.append(ss[0+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
            for chi in range(len(ss[1+link*2])):
                chns.append(ss[1+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
        sss.append(chns)
    return sss 

#sss: 2D array [chn_no 0 to 511] [sample1, sample2, ...]


####################FEMBs Data taking################################
#fp =  "D:/debug_data/Raw_MULTCONFIG_03_08_2022.bin"
import struct

for xxxx in range(1):
    #fp =  "D:/debug_data/Raw_CALI_200mVBL_14_0mVfC_2_0us_0x{:02x}_03_08_2022.bin".format(i)
    fp =  "D:/debug_data/RawRMS_14_08_2022_17_00_44.bin"
#    fp =  "D:/debug_data/RawRMS_14_08_2022_20_01_09.bin"
    fp =  "D:/debug_data/RawRMS_14_08_2022_23_29_48.bin"
    fp =  "D:/debug_data/RawRMS_15_08_2022_09_12_48.bin"
    
    with open(fp, 'rb') as fn:
        raw = pickle.load(fn)
    
    rawdata = raw[0]
    pwr_meas = raw[1]
    cfg_paras_rec = raw[2]
#    print (len(rawdata[0][0]))
#    print ((rawdata[0][0][0:100]))
#    for runi in range(len(rawdata)):
    for runi in [0,1]:
        #words = len(rawdata[0][0])//4
        words = len(rawdata[runi][0])//4
        frames = words//120
        dd =struct.unpack_from("<%dI"%(words),rawdata[runi][0])
        N = 120
        #for i in range(N):
        #    print ("%08x, %08x, %08x, %08x, %08x, %08x, %08x, %08x, %08x "%(dd[i],dd[i+N],dd[i+N*2],dd[i+N*3],dd[i+N*4],dd[i+N*5],dd[i+N*6],dd[i+N*7],dd[i+N*8] ))
        ts_links = []
        tss = []
        for i in range(words//120):
            ts_link = (dd[N*i+3] & 0x0000e000)>>13
            ts = (dd[N*i+4]>>21)&0x3ff
#            print ("%08x, %08x, %02d, %04d"%(dd[N*i+3],dd[N*i+4], ts_link, ts))
            ts_links.append(ts_link)
            tss.append(ts)

#        re_tss = []
        for i in range(len(tss)-1):
            if tss[i+1] - tss[i] == 2:
                if ts_links[i+1]-ts_links[i] == 1:
                    tss[i+1] = (tss[i+1] - 1)&0x3ff
            elif tss[i+1] == tss[i]:
                if ts_links[i+1]-ts_links[i] == 1:
                    tss[i+1] = (tss[i+1] + 1)&0x3ff
            elif tss[i+1] < tss[i] == 0:
                if  0x400 - tss[i] == 2:
                    if ts_links[i+1]-ts_links[i] == 1:
                        tss[i+1]

        for i in range(len(tss)-1):
            if (tss[i+1] - tss[i]) != 1:
                print (runi, tss[i+1], tss[i])


    rawdata = raw[0]
    #for runi in range(len(rawdata)):
    for runi in [0,1]:
        #words = len(rawdata[0][0])//4
        words = len(rawdata[runi][1])//4
        frames = words//120
        dd =struct.unpack_from("<%dI"%(words),rawdata[runi][0])
        N = 120
        #for i in range(N):
        #    print ("%08x, %08x, %08x, %08x, %08x, %08x, %08x, %08x, %08x "%(dd[i],dd[i+N],dd[i+N*2],dd[i+N*3],dd[i+N*4],dd[i+N*5],dd[i+N*6],dd[i+N*7],dd[i+N*8] ))
        ts_links = []
        tss = []
        for i in range(words//120):
            ts_link = (dd[N*i+3] & 0x0000e000)>>13
            ts = (dd[N*i+4]>>21)&0x3ff
#            print ("%08x, %08x, %02d, %04d"%(dd[N*i+3],dd[N*i+4], ts_link, ts))
            ts_links.append(ts_link)
            tss.append(ts)

#        re_tss = []
        for i in range(len(tss)-1):
            if tss[i+1] - tss[i] == 2:
                if ts_links[i+1]-ts_links[i] == 1:
                    tss[i+1] = (tss[i+1] - 1)&0x3ff
            elif tss[i+1] == tss[i]:
                if ts_links[i+1]-ts_links[i] == 1:
                    tss[i+1] = (tss[i+1] + 1)&0x3ff
            elif tss[i+1] < tss[i] == 0:
                if  0x400 - tss[i] == 2:
                    if ts_links[i+1]-ts_links[i] == 1:
                        tss[i+1]

        for i in range(len(tss)-1):
            if (tss[i+1] - tss[i]) != 1:
                print (runi, tss[i+1], tss[i])
       
    exit()
    
    #power measurement result
#    print (pwr_meas)
    #configuration for this run of data
#    print (cfg_paras_rec)
    
    
    fig = plt.figure(figsize=(10,6))
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
    axs = [ax1, ax2, ax3, ax4]
    
    sss = data_valid(rawdata)
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
    #plt.close()

