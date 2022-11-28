import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
import os
from rawdata_dec import rawdata_dec 
from fft_chn import chn_rfft_psd
from highpass_filter import hp_flt_applied
from tools import Tools

def noise_a_chn(chnrmsdata, chnno, fft_en = True, fft_s=2000, fft_avg_cycle=50, wibno=0,  fembno=0 ):
    len_chnrmsdata = len(chnrmsdata)
    chnrmsdata = chnrmsdata[0:len_chnrmsdata ]
    rms =  np.std(chnrmsdata[0:10000])
    ped = np.mean(chnrmsdata[0:10000])
    data_slice = chnrmsdata

    avg_cycle_l = 1
    if (len_chnrmsdata >= 400000):
        fft_s_l = 400000//avg_cycle_l
    else:
        fft_s_l =len(chnrmsdata) 

    if (fft_en):
        f,p = chn_rfft_psd(chnrmsdata,  fft_s = fft_s, avg_cycle = fft_avg_cycle)
        f_l, p_l = chn_rfft_psd(chnrmsdata, fft_s = fft_s_l, avg_cycle = avg_cycle_l)
    else:
        f = None
        p = None
        f_l = None
        p_l = None

#   data after highpass filter
    flt_chn_data = hp_flt_applied(chnrmsdata, fs = 1953125, passfreq = 1000, flt_order = 3)
    flt_chn_data = np.array(flt_chn_data) +  ped 
    hfped = ped
    hfrms = np.std(flt_chn_data)
    if (fft_en):
        hff,hfp = chn_rfft_psd(flt_chn_data, fft_s = fft_s, avg_cycle = fft_avg_cycle)
        hff_l,hfp_l = chn_rfft_psd(flt_chn_data, fft_s = fft_s_l, avg_cycle = avg_cycle_l)
    else:
        hff = None
        hfp = None
        hff_l = None
        hfp_l = None
        
    hfdata_slice = flt_chn_data

    chn_noise_paras = [chnno, 
                       rms,   ped,   data_slice, f,  p, f_l, p_l,
                       hfrms, hfped, hfdata_slice, hff, hfp, hff_l, hfp_l]
    return chn_noise_paras


fp = sys.argv[1] 

with open(fp, 'rb') as fn:
    rawdata = pickle.load(fn)

fp = fp[0:-4] + ".set"
with open(fp, 'rb') as fn:
    fesets = pickle.load(fn)
[sts, snc, sg0, sg1, st0, st1, sdf, slk0, slk1] = fesets
tl=Tools()

while True:
    try:
        chn = int(input("CH#(-1 to exit) = "))
    except :
        continue
    if chn == -1:
        exit()

    wibi = chn//512
    fembi = chn//128 + 1
    chi = chn%128
    dfmap = tl.LoadMap(fembi)
    plane,strip = tl.FindStrips(dfmap, fembi, chi)
    if plane ==1:
        pl = "U"
    if plane ==2:
        pl = "V"
    if plane ==3:
        pl = "X"
    print ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))

    chrms = []
    for chx in range(12*128):
        chrms.append(np.std(rawdata[chx][0:1000]))
        if np.std(rawdata[chx][0:1000]) > 100:
                print ("Large RMS", chx, np.std(rawdata[chx][0:1000]))


    chnrmsdata= rawdata[chn]
    chninfo = noise_a_chn(chnrmsdata, chnno=chn, fft_en = True, fft_s=2000, fft_avg_cycle=50)
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6,10))
    plt.rcParams.update({'font.size':12})
    plt.subplot(411)
    xlen = 200
    x = (np.arange(xlen))*512/1000.0
    plt.plot(x, chninfo[3][0:xlen], marker='.',color='r', label = "%d"%chn)
    plt.legend()
    plt.title ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
    plt.xlabel ("Time / us")
    plt.ylabel ("ADC / bit" )
    plt.grid()
    
    plt.subplot(412)
    xlen = 20000
    if xlen > len(chninfo[3]):
        xlen = len(chninfo[3])
    x = (np.arange(xlen))*512/1000.0
    plt.plot(x, chninfo[3][0:xlen], marker='.',color='r', label = "%d"%chn)
    plt.legend()
    plt.title ("Waveform @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
    plt.xlabel ("Time / us")
    plt.ylabel ("ADC / bit" )
    plt.grid()
    
    plt.subplot(413)
    plt.plot(chninfo[4], chninfo[5], marker='.',color='r', label = "%d"%chn)
    plt.legend()
    plt.title ("FFT @ WIB%dFEMB%dCH%d, %s plane # %d"%(wibi, (fembi%4-1), chi, pl, strip ))
    plt.xlabel ("Frequency / Hz")
    plt.ylabel (" / dB" )
    plt.grid()

    plt.subplot(414)
    x = np.arange(12*128)
    plt.plot(x, chrms, marker='.',color='r', label = "RMS")
    plt.legend()
    plt.title("RMS noise distribution")
    plt.xlabel ("CH# ")
    plt.ylabel ("ADC / bit" )
    plt.grid()

    plt.tight_layout()
    
    plt.show()
    plt.close()

