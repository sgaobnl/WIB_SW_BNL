import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import sys
from Plot_tools import plot_tools

sys.path.insert(0, '../')
from QC_tools import QC_tools
qc=QC_tools()

def Rebin_time(data, ng):
    
    newdata=[]
    for ich in range(len(data)):
        times = len(data[ich])
        newdata.append([])
        tmp=0
        nn=0
        for j in range(times): 
            tmp = tmp+data[ich][j]
            nn=nn+1
            if nn==ng:
               tmp=tmp/nn
               newdata[ich].append(tmp)
               tmp=0
               nn=0

    return newdata

def GetFFT(data):

    sr = 2e6 #Hz
    a_fft = np.fft.fft(data) 
    N=len(data)
    n = np.arange(N)
    T = N/sr 
    freq = n/T
    oneside = N//2
 
    return freq[1:oneside],a_fft[1:oneside]

datafolder = "D:/debug_data/"
#datafolder = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/"

filename = "Raw_07_09_2022_12_11_42_coherent.bin"
#filename = "CALI1/CALI1_SE_200mVBL_14_0mVfC_2_0us_0x2c.bin"
datafile = datafolder+filename

fp = datafile
with open(fp, 'rb') as fn:
     raw = pickle.load(fn)

rawdata=raw[0]

fembs=[0,1,2,3]
PLT = plot_tools()

pldata = qc.data_decode(rawdata)
pl_data = np.array(pldata)


nevents = len(pldata)
femb_data=[] 
for ifemb in fembs:
    for i in range(128):
        global_ch = 128*ifemb+i
        femb_data.append(pl_data[:,global_ch].ravel())
        #femb_data.append(pl_data[0][global_ch])

femb_data=np.array(femb_data)
avg_data=np.mean(femb_data, 0)

freq,avg_fft = GetFFT(avg_data) 

#xx=range(len(avg_data) )
#fig,axes = plt.subplots(2,1)
#axes[0].plot(xx, avg_data)
#axes[1].plot(freq, np.abs(avg_fft))
#axes[1].set_yscale("log")
#plt.show() 

totalch = len(femb_data)
new_data = []
for i in range(totalch):
    tmp=[]
    for j in range(len(avg_data)):
      tmp.append(femb_data[i][j]-avg_data[j])

    new_data.append(tmp)

newdata = Rebin_time(new_data, 100)
fembdata = Rebin_time(femb_data, 100)
xx = range(len(newdata[0]))
yy = range(128*len(fembs))
fig, ax = plt.subplots(2,1)
im = ax[0].pcolormesh(xx, yy, fembdata)
fig.colorbar(im, ax=ax[0])
im = ax[1].pcolormesh(xx, yy, newdata)
fig.colorbar(im, ax=ax[1])
plt.show() 

