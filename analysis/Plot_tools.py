import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
from scipy.signal import find_peaks

def data_valid(raw):
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

def GetPeak(rawdata, femb_no):

    pl_data = np.array(data_valid(rawdata),dtype=object)
    nfemb = len(pl_data[0])//128
    nevent = len(pl_data)

    #peaks = np.empty(0)
    for ch in range(128):
        global_ch = femb_no*128+ch
        pmax = np.amax(pl_data[0][global_ch])
            
        p_val=np.empty(0)
        for itr in range(nevent):
            pos_peaks, _ = find_peaks(pl_data[itr][global_ch],height=pmax-100)
            p_val = np.hstack([p_val,pl_data[itr][global_ch][pos_peaks]])

        #peaks=np.append(peaks,np.mean(p_val))
        print(ch,np.mean(p_val))



def PlotWaveforms(data, femb_no, chan): 
    
    pl_data = np.array(data_valid(data),dtype=object)
    nfemb = len(pl_data[0])//128
    nevent = len(pl_data)
    
    peaks = np.empty(0)
    global_ch = femb_no*128+chan
    pmax = np.amax(pl_data[0][global_ch])
    
    p_val=np.empty(0)
    fig, ax =plt.subplots(figsize=(6,4))
    for itr in range(nevent):
        xx = range(len(pl_data[itr][global_ch][:]))
        ax.plot(xx,pl_data[itr][global_ch][:])
    
    ax.set_xlabel('tick')
    ax.set_ylabel('ADC')
    ax.set_title('FEMB{}'.format(i))
    plt.show()

#datafolder = "D:/debug_data/femb1_femb2_femb3_femb4_RT_0pF/"
datafolder = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/femb1_femb2_femb3_femb4_RT_0pF_R001/"

filename = "Raw_CALI_SE_200mVBL_4_7mVfC_2_0us_0x28.bin"
datafile = datafolder+filename

fp = datafile
with open(fp, 'rb') as fn:
     raw = pickle.load(fn)

rawdata = raw[0]

#GetPeak(rawdata,1)

for i in range(112,128):
    PlotWaveforms(rawdata,3,i)
