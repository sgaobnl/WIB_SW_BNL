import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import sys

sys.path.insert(0, '../')
from QC_tools import QC_tools
qc=QC_tools()

def PlotWaveforms(data, femb_no, chan): 
    
    pldata = qc.data_decode(rawdata)
    pl_data = np.array(pldata,dtype=object)
    nfemb = len(pl_data[0])//128
    nevent = len(pl_data)
    
    global_ch = femb_no*128+chan
    for itr in range(nevent):
        fig, ax =plt.subplots(figsize=(6,4))
        xx = range(len(pl_data[itr][global_ch][:]))
        ax.plot(xx,pl_data[itr][global_ch][:])
    
        ax.set_xlabel('tick')
        ax.set_ylabel('ADC')
        ax.set_title('FEMB{} ch# {} event# {}'.format(femb_no, chan, itr))
        plt.show()

def GetRMS(data, nfemb, chan):
    
    nevent = len(data)

    global_ch = nfemb*128+chan
    peddata=np.empty(0)

    npulse=0
    first = True
    allpls=np.empty(0)
    for itr in range(nevent):
        evtdata = data[itr][global_ch]
        allpls=np.append(allpls,evtdata)

    ch_ped = np.mean(allpls)
    ch_rms = np.std(allpls)

    return ch_ped,ch_rms

def GetGain(nfemb, chan, dac_list, snc, sgs, sgp, namepat):

    dac_v = {}  # mV/bit
    dac_v['4_7mVfC']=18.66
    dac_v['7_8mVfC']=14.33
    dac_v['14_0mVfC']=8.08
    dac_v['25_0mVfC']=4.61

    CC=1.85*pow(10,-13)
    e=1.602*pow(10,-19)

    if "sgp1" in namepat:
        dac_du = dac_v['4_7mVfC']
    else:
        dac_du = dac_v[sgs]

    pk_list=[]
    for dac in dac_list:
        afile = namepat.format(snc, sgs, "2_0us", dac)
        with open(afile, 'rb') as fn:
             raw = pickle.load(fn)

        rawdata=raw[0]
        pldata = qc.data_decode(rawdata)
        pldata = np.array(pldata, dtype=object)

        if dac==0:
           tmpped,_ = GetRMS(pldata, nfemb, chan)
           pk_list.append(tmpped)
        else:
           ana = qc.data_ana(pldata, nfemb)
           pk_list.append(ana[2][chan])

    ana=CheckLinearty(dac_list, pk_list, 10, 4)

    fig1,ax1 = plt.subplots(1,2)
    ax1[0].plot(dac_list, pk_list)
    ax1[0].set_xlabel('DAC')
    ax1[0].set_ylabel('Peak value')
    ax1[0].set_title('FEMB{} ch# {}'.format(i, chan))

    ax1[1].plot(dac_list, ana[1])
    ax1[1].set_xlabel('DAC')
    ax1[1].set_ylabel('inl')
    ax1[1].set_title('FEMB{} ch# {}'.format(i, chan))

    plt.show()

def CheckLinearty(dac_list, pk_list, updac, lodac):

    dac=[]
    pk=[]
    for i in range(len(dac_list)):
        if dac_list[i]<updac and dac_list[i]>=lodac:
           dac.append(dac_list[i])
           pk.append(pk_list[i])

    slope,intercept=np.polyfit(dac,pk,1)

    y_min = pk_list[0]
    y_max = pk_list[-1]
    inl_list=[]

    for i in range(len(dac_list)):
        y_r = pk_list[i]
        y_p = dac_list[i]*slope + intercept
        inl = abs(y_r-y_p)/(y_max-y_min)
        inl_list.append(inl)

    return slope,inl_list 

def FEMB_SUB_PLOT(ax, x, y, title, xlabel, ylabel, color='b', marker='.', ylabel_twx = "", limit=False, ymin=0, ymax=1000):
     ax.set_title(title)
     ax.set_xlabel(xlabel)
     ax.set_ylabel(ylabel)
     ax.grid(True)
     if limit:
         ax.plot(x,y, marker=marker, color=color)
         ax.set_ylim([ymin, ymax])
     else:
         ax.plot(x,y, marker=marker, color=color)


def FEMB_CHK_PLOT(chn_rmss,chn_peds, chn_pkps, chn_pkns, chn_onewfs, chn_avgwfs):
    fig = plt.figure(figsize=(10,5))
    fn = fp.split("/")[-1]
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
    chns = range(128)

    FEMB_SUB_PLOT(ax1, chns, chn_rmss, title="RMS Noise", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_peds, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='b', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_pkps, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_pkns, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='g', marker='.')
    for chni in chns:
        ts = 100
        x = (np.arange(ts)) * 0.5
        y3 = chn_onewfs[chni][25:ts+25]
        y4 = chn_avgwfs[chni][25:ts+25]
        FEMB_SUB_PLOT(ax3, x, y3, title="Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))
        FEMB_SUB_PLOT(ax4, x, y4, title="Averaging Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))

    #fig.suptitle(fn)
    plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
    plt.show()

datafolder = "D:/IO-1865-1C/QC/data/femb102_femb113_femb114_femb106_LN_150pF/"
#datafolder = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/femb101_femb107_femb105_femb111_LN_150pF/"

filename = "Raw_SE_200mVBL_14_0mVfC_2_0us_0x20.bin"
#filename = "CALI3/CALI3_SE_200mVBL_14_0mVfC_2_0us_0x22_sgp1.bin"
datafile = datafolder+filename

fp = datafile
with open(fp, 'rb') as fn:
     raw = pickle.load(fn)

rawdata = raw[0]

nfemb=3
dac_list=range(0,20)
snc = "900mVBL"
sgs = "14_0mVfC" 
sgp = 1
namepat = datafolder + "CALI4/CALI4_SE_{}_{}_{}_0x{:02x}_sgp1.bin"

for i in range(120,127):
    PlotWaveforms(rawdata, nfemb, i)
#    GetGain(nfemb, i, dac_list, snc, sgs, sgp, namepat)

# make the rms, pulse, waveform plots

#pldata = qc.data_decode(rawdata)
#pldata = np.array(pldata,dtype=object)
#ana = qc.data_ana(pldata,nfemb)
#FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5])

