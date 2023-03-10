import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
import os
from rawdata_dec import rawdata_dec 
from tools import Tools
import matplotlib.pyplot as plt


tl = Tools()
fp = sys.argv[1] 

with open(fp, 'rb') as fn:
    chns_c = pickle.load(fn)

uplanecap = np.zeros(476)
vplanecap = np.zeros(476)
xplanecap = np.zeros(584)

for i in range(3*4*128):
    nfemb = i//128 + 1
    nch = i %128

    dfmap = tl.LoadMap(nfemb)
    plane,strip = tl.FindStrips(dfmap, nfemb, nch)

    if plane==1:
       uplanecap[strip-1]=chns_c[i]
       if chns_c[i] < 80:
           print ("U", i, strip-1)
    if plane==2:
       vplanecap[strip-1]=chns_c[i]
    if plane==3:
       xplanecap[strip-1]=chns_c[i]

chns_c_map = np.concatenate((uplanecap,vplanecap,xplanecap)) 


chs = np.arange(12*128)
fig = plt.figure(figsize=(14,8))
plt.rcParams.update({'font.size':12})
plt.plot(chs[0:476], chns_c_map[0:476], marker='.',color='r', label = "U plane")
plt.plot(chs[476:476*2], chns_c_map[476:476*2], marker='.',color='b', label = "V plane")
plt.plot(chs[476*2:], chns_c_map[476*2:], marker='.',color='g', label = "X plane")
plt.legend()
#plt.title ("RMS Noise Distribution")
plt.xlabel ("CH# (According to CRP mapping)")
plt.ylabel ("Capacitance / pF" )
plt.ylim((0,250))
plt.grid()
plt.axvline(x=475, color = 'm', linestyle='--')
plt.axvline(x=951, color = 'm', linestyle='--')

#
plt.tight_layout()

plt.show()
plt.close()



#while True:
#    strch =  input("CH/PX/PU/PV#(EX to exit) : ")
#    if "EX" in strch:
#        exit()
#    elif "CH" in strch:
#        chn = int(strch[2:])
#
#    elif "PX" in strch:
#        pxch = int(strch[2:])
#        find_flg = False
#        for fembi in range(1,13,1):
#            dfmap = tl.LoadMap(fembi)
#            for chi in range(128):
#                plane,strip = tl.FindStrips(dfmap, fembi, chi)
#                if (plane == 3) and (strip == pxch):
#                    chn = (fembi-1)*128 + chi
#                    find_flg = True
#                    break
#            if find_flg:
#                break
#
#    elif "PU" in strch:
#        puch = int(strch[2:])
#        find_flg = False
#        for fembi in range(1,13,1):
#            dfmap = tl.LoadMap(fembi)
#            for chi in range(128):
#                plane,strip = tl.FindStrips(dfmap, fembi, chi)
#                if (plane == 1) and (strip == puch):
#                    chn = (fembi-1)*128 + chi
#                    find_flg = True
#                    break
#            if find_flg:
#                break
#
#    elif "PV" in strch:
#        pvch = int(strch[2:])
#        find_flg = False
#        for fembi in range(1,13,1):
#            dfmap = tl.LoadMap(fembi)
#            for chi in range(128):
#                plane,strip = tl.FindStrips(dfmap, fembi, chi)
#                if (plane == 2) and (strip == pvch):
#                    chn = (fembi-1)*128 + chi
#                    find_flg = True
#                    break
#            if find_flg:
#                break
#    else:
#        continue
    
#    wibi = chn//512
#    fembi = chn//128 + 1
#    chi = chn%128
#    dfmap = tl.LoadMap(fembi)
#    plane,strip = tl.FindStrips(dfmap, fembi, chi)
#    if plane ==1:
#        pl = "U"
#    if plane ==2:
#        pl = "V"
#    if plane ==3:
#        pl = "X"
#    print ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))

#    chrms = []
#    for chx in range(12*128):
#        chrms.append(np.std(rawdata[chx][0:1000]))
#        if np.std(rawdata[chx][0:1000]) > 100:
#                print ("Large RMS", chx, np.std(rawdata[chx][0:1000]))


#    chnrmsdata= rawdata[chn]
#    chninfo = noise_a_chn(chnrmsdata, chnno=chn, fft_en = True, fft_s=2000, fft_avg_cycle=50)
#    
#    import matplotlib.pyplot as plt
#    fig = plt.figure(figsize=(10,8))
#    plt.rcParams.update({'font.size':12})
#    plt.subplot(221)
#    xlen = 2000
#    x = (np.arange(xlen))*512/1000.0
#    plt.plot(x, chninfo[3][0:xlen], marker='.',color='r', label = "%d"%chn)
#    plt.legend()
#    plt.title ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
#    plt.xlabel ("Time / us")
#    plt.ylabel ("ADC / bit" )
#    plt.grid()
#    
#    plt.subplot(222)
#    xlen = 200000
#    if xlen > len(chninfo[3]):
#        xlen = len(chninfo[3])
#    x = (np.arange(xlen))*512/1000.0
#    plt.plot(x, chninfo[3][0:xlen], marker='.',color='r', label = "%d"%chn)
#    print (np.std(chninfo[3][0:2000]), np.std(chninfo[3][0:20000]), len(chninfo[3]))
#    plt.legend()
#    plt.title ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
#    plt.xlabel ("Time / us")
#    plt.ylabel ("ADC / bit" )
#    plt.grid()
#    
#    plt.subplot(223)
#    plt.plot(chninfo[4], chninfo[5], marker='.',color='r', label = "%d"%chn)
#    plt.legend()
#    plt.title ("FFT @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
#    plt.xlabel ("Frequency / Hz")
#    plt.ylabel (" / dB" )
#    plt.grid()
#
#    plt.subplot(224)
#    plt.plot(chninfo[6], chninfo[7], marker='.',color='r', label = "%d"%chn)
#    plt.legend()
#    plt.title ("FFT @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
#    plt.xlim((0,30000))
#    plt.xlabel ("Frequency / Hz")
#    plt.ylabel (" / dB" )
#    plt.grid()
#
    #chrms =  np.std(rawdata, axis=(1)) 
    #chped = np.mean(rawdata, axis=(1)) 
    #chmax =  np.max(rawdata, axis=(1)) 
    #chmin =  np.min(rawdata, axis=(1)) 


