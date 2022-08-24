import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
import copy

import struct

for xxxx in range(1):
    fp =  "D:/debug_data/RawRMS_15_08_2022_16_43_56.bin"
    fp =  "D:/debug_data/RawRMS_15_08_2022_16_46_25.bin"
    fp =  "D:/debug_data/RawRMS_15_08_2022_18_47_30.bin"
#    fp =  "D:/debug_data/RawRMS_15_08_2022_18_49_58.bin"
    fp =  "D:/debug_data/RawRMS_15_08_2022_19_06_40.bin"
    fp =  "D:/debug_data/RawRMS_16_08_2022_05_30_26.bin"
#    fp =  "D:/debug_data/RawRMS_16_08_2022_06_23_22.bin"
    fp =  "D:/debug_data/RawRMS_23_08_2022_16_28_45.bin"
    
    with open(fp, 'rb') as fn:
        raw = pickle.load(fn)
    
    rawdata = raw[0]
    pwr_meas = raw[1]
    cfg_paras_rec = raw[2]

    fm = 0

#Frame0 FEMB0&1
    ftls = []
    ftss = []
    fdts = []
    for runi in [fm]:
        words = len(rawdata[runi][0])//4
        frames = words//120
        dd =struct.unpack_from("<%dI"%(words),rawdata[runi][0])
        print ([hex(ddi) for ddi in dd[120*0:120*1]])
        print ([hex(ddi) for ddi in dd[120*1:120*2]])
        print ([hex(ddi) for ddi in dd[120*2:120*3]])
#        print ([hex(ddi) for ddi in dd[120*3:120*4]])
#        print ([hex(ddi) for ddi in dd[120*4:120*5]])
#        print ([hex(ddi) for ddi in dd[120*5:120*6]])
#        print ([hex(ddi) for ddi in dd[-120*1:-120*0]])
#        print ([hex(ddi) for ddi in dd[-120*2:-120*1]])
#        print ([hex(ddi) for ddi in dd[-120*3:-120*2]])
#        print ([hex(ddi) for ddi in dd[-120*4:-120*3]])
#        print ([hex(ddi) for ddi in dd[-120*5:-120*4]])
#        print ([hex(ddi) for ddi in dd[-120*6:-120*5]])
        N = 120
        ts_links = []
        tls = []
        tss = []
        dts = []
        print ("word#1, word#2, word#3, word#4, timing master time stamp, CDTS-ID[0-2], Coldata time stampe")
        for i in range(words//120):
            dt = ((dd[N*i+2]<<32) + dd[N*i+1])>>5
            ts_link = (dd[N*i+3] & 0x0000e000)>>13
            ts = (dd[N*i+4]>>21)&0x3ff
            dt_low5 = (dd[N*i+1])&0x1f
            ts_low5 = (dd[N*i+4]>>16)&0x1f
            if dt_low5 != ts_low5:
                print ("error....")
                print (dt_low5, ts_low5)
                exit()
            #if i >= words//120 - 20:
            if i < 20:
            #if (i > 480) and (i <500):
                print (hex(dd[N*i+1]),hex(dd[N*i+2]), hex(dd[N*i+3]), hex(dd[N*i+4]), hex(dt), hex(ts_link), hex(ts))
            ts_links.append(ts_link)
            tls.append(ts_link)
            tss.append(ts)
            dts.append(dt)

        ftls.append(tls)
        ftss.append(tss)
        fdts.append(dts)
    ftls0 = copy.deepcopy(ftls)
#    print (len(ftls0), len(ftls0[0]))
    ftss0 = copy.deepcopy(ftss)
    fdts0 = copy.deepcopy(fdts)
#    print (len(fdts0), len(fdts0[0]))
#    exit()



#Frame0 FEMB2&3
    ftls = []
    ftss = []
    fdts = []
    for runi in [fm]:
        words = len(rawdata[runi][1])//4
        frames = words//120
        dd =struct.unpack_from("<%dI"%(words),rawdata[runi][1])
        N = 120
        ts_links = []
        tls = []
        tss = []
        dts = []
        print ("word#1, word#2, word#3, word#4, timing master time stamp, CDTS-ID[0-2], Coldata time stampe")
        for i in range(words//120):
            dt = (dd[N*i+2] + dd[N*i+1])>>5
            ts_link = (dd[N*i+3] & 0x0000e000)>>13
            ts = (dd[N*i+4]>>21)&0x3ff
            dt_low5 = (dd[N*i+2] + dd[N*i+1])&0x1f
            ts_low5 = (dd[N*i+4]>>16)&0x1f
            if dt_low5 != ts_low5:
                print ("error....")
                exit()
            if i >= words//120 - 20:
            #if i < 20:
            #if (i > 480) and (i <500):
                print (hex(dd[N*i+1]),hex(dd[N*i+2]), hex(dd[N*i+3]), hex(dd[N*i+4]), hex(dt), hex(ts_link), hex(ts))
            ts_links.append(ts_link)
            tls.append(ts_link)
            tss.append(ts)
            dts.append(dt)

        ftls.append(tls)
        ftss.append(tss)
        fdts.append(dts)
    ftls1 = copy.deepcopy(ftls)
    ftss1 = copy.deepcopy(ftss)
    fdts1 = copy.deepcopy(fdts)

    fig = plt.figure(figsize=(10,6))
    x0 = np.arange(len(fdts0[0]))
    y0 = fdts0[0]
    print (len(y0))
    x1 = np.arange(len(fdts1[fm]))
    y1 = fdts1[fm]
    plt.plot(x0, y0, label ="FEMB0&1")
    plt.plot(x1, y1, label ="FEMB2&3")
    plt.legend()
    plt.show()
    plt.close()


    fig = plt.figure(figsize=(10,6))
    x0 = np.arange(len(ftss0[0]))
    y0 = ftss0[0]
    print (len(y0))
    x1 = np.arange(len(ftss1[fm]))
    y1 = ftss1[fm]
    plt.plot(x0, y0, label ="FEMB0&1")
    plt.plot(x1, y1, label ="FEMB2&3")
    plt.legend()
    plt.show()
    plt.close()

    fig = plt.figure(figsize=(10,6))
    x0 = np.arange(len(ftls0[0]))
    y0 = ftls0[0]
    print (len(y0))
    x1 = np.arange(len(ftls1[fm]))
    y1 = ftls1[fm]
    plt.plot(x0, y0, label ="FEMB0&1")
    plt.plot(x1, y1, label ="FEMB2&3")
    plt.legend()
    plt.show()
    plt.close()

    exit()


#    fig = plt.figure(figsize=(10,6))
#    x0 = np.arange(len(fdts0[0]))
#    y0 = fdts0[0]
#    print (len(y0))
##    x1 = np.arange(len(fdts1[fm]))
##    y1 = fdts1[fm]
#    plt.plot(x0, y0, label ="FEMB0&1")
##    plt.plot(x1, y1, label ="FEMB2&3")
#    plt.legend()
#    plt.show()
#    plt.close()
#
#    exit()
#    
##    ftss = []
##    for runi in [fm]:
##        words = len(rawdata[runi][0])//4
##        frames = words//120
##        dd =struct.unpack_from("<%dI"%(words),rawdata[runi][0])
##        N = 120
##        ts_links = []
##        tss = []
##        for i in range(words//120):
##            ts_link = (dd[N*i+3] & 0x0000e000)>>13
##            ts = (dd[N*i+4]>>21)&0x3ff
##            ts_links.append(ts_link)
##            tss.append(ts)
##
##        for i in range(len(tss)-1):
##            if tss[i+1] - tss[i] == 2:
##                if ts_links[i+1]-ts_links[i] == 1:
##                    tss[i+1] = (tss[i+1] - 1)&0x3ff
##            elif tss[i+1] == tss[i]:
##                if ts_links[i+1]-ts_links[i] == 1:
##                    tss[i+1] = (tss[i+1] + 1)&0x3ff
##            elif tss[i+1] < tss[i] == 0:
##                if  0x400 - tss[i] == 2:
##                    if ts_links[i+1]-ts_links[i] == 1:
##                        tss[i+1]
###        for i in range(len(tss)-1):
###            if (tss[i+1] - tss[i]) != 1:
###                print (runi, tss[i+1], tss[i])
##        ftss.append(tss)
##    ftss1 = ftss
##    print (ftss1[0][0], ftss1[0][-1])
##    exit()
#      
#    fig = plt.figure(figsize=(10,6))
#    x0 = np.arange(len(ftss0[0]))
#    y0 = ftss0[0]
#    x1 = np.arange(len(ftss1[0]))
#    y1 = ftss1[0]
#    plt.plot(x0, y0, label ="FEMB0&1")
#    plt.plot(x1, y1, label ="FEMB2&3")
#    plt.legend()
#    plt.show()
#    plt.close()
#
#    
#    #power measurement result
##    print (pwr_meas)
#    #configuration for this run of data
##    print (cfg_paras_rec)
#    
#    
#    fig = plt.figure(figsize=(10,6))
#    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
#    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
#    ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
#    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
#    axs = [ax1, ax2, ax3, ax4]
#    
#    sss = data_valid(rawdata)
#    N = 0
#    ss = sss[N]
#    fembs=[0, 1,2,3]
#    for fembi in fembs:
#        for chi in range(128):
#            x = (np.arange(len(ss[fembi*128 + chi]))) * 0.5
#            axs[fembi].plot(x, ss[fembi*128 + chi], marker = '.')
#            axs[fembi].set_xlabel("Time / $\mu$s")
#            axs[fembi].set_ylabel("ADC /bin")
#            axs[fembi].set_title(f"FEMB{fembi}")
#    plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
#    plt.show()
#    #plt.close()
#
##        for i in range(len(tss)-1):
##            if tss[i+1] - tss[i] == 2:
##                if ts_links[i+1]-ts_links[i] == 1:
##                    tss[i+1] = (tss[i+1] - 1)&0x3ff
##            elif tss[i+1] == tss[i]:
##                if ts_links[i+1]-ts_links[i] == 1:
##                    tss[i+1] = (tss[i+1] + 1)&0x3ff
##            elif tss[i+1] < tss[i] == 0:
##                if  0x400 - tss[i] == 2:
##                    if ts_links[i+1]-ts_links[i] == 1:
##                        tss[i+1]
##        for i in range(len(tss)-1):
##            if (tss[i+1] - tss[i]) != 1:
##                print (runi, i, tss[i+1], tss[i])
#
##            if (i < 10) or (i > words//120 - 10):
##                print (hex(dd[N*i+1]),hex(dd[N*i+2]), hex(dd[N*i+3]), hex(dd[N*i+4]), hex((dd[N*i+1]&0x7ffffff)>>5), hex((dd[N*i+3] & 0x0000e000)>>13), hex((dd[N*i+4]>>21)&0x3ff))
#
