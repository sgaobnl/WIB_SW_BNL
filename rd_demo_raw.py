import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
import copy

import struct
from spymemory_decode import wib_spy_dec_syn


fp ="D:/debug_data/RawRMS_24_08_2022_13_31_47.bin" #this data is using PLL on board and fake timing system
fp ="D:/debug_data/RawRMS_24_08_2022_14_29_46.bin" #this data is using external timing system from the front panel sfp"
fp ="D:/debug_data/RawRMS_24_08_2022_14_41_07.bin" #this data is using external timing system from the front panel sfp"
fp ="D:/debug_data/RawRMS_24_08_2022_15_53_20.bin" #this data is using external timing system from the backplane"
fp ="D:/debug_data/RawRMS_24_08_2022_17_28_05.bin" #this data is using external timing (backplane), external pulser"
#fp ="D:/debug_data/RawRMS_24_08_2022_17_40_03.bin" #this data is using external timing (backplane), external pulser"
fp ="D:/debug_data/Raw_26_08_2022_10_27_33.bin"
fp ="D:/debug_data/Raw_26_08_2022_10_35_51.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, 1 offset between link0 & 1
fp ="D:/debug_data/Raw_26_08_2022_10_39_33.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, 1 offset between link0 & 1
fp ="D:/debug_data/Raw_26_08_2022_10_40_00.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, 1 offset between link0 & 1
fp ="D:/debug_data/Raw_26_08_2022_10_41_31.bin" #external pls, fake timing, 2 edge fc, 2 sync fc, link0 & 1 synced
#power cycling FEMBs
fp ="D:/debug_data/Raw_26_08_2022_10_47_15.bin" #external pls, fake timing, 1 edge fc, 1 sync fc,, 1 offset between link0 & 1 
fp ="D:/debug_data/Raw_26_08_2022_10_48_32.bin" #external pls, fake timing, 2 edge fc, 1 sync fc,, 1 offset between link0 & 1 
fp ="D:/debug_data/Raw_26_08_2022_10_49_28.bin" #external pls, fake timing, 2 edge fc, 2 sync fc,, 1 offset between link0 & 1 
#power cycling FEMBs
fp ="D:/debug_data/Raw_26_08_2022_10_52_04.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, synced 
#power cycling FEMBs
fp ="D:/debug_data/Raw_26_08_2022_10_54_01.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, synced 
#power cycling FEMBs
fp ="D:/debug_data/Raw_26_08_2022_10_55_37.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, synced 
#power cycling WIB & FEMBs
fp ="D:/debug_data/Raw_26_08_2022_10_58_00.bin" #external pls, fake timing, 1 edge fc, 1 sync fc, 1 offset
fp ="D:/debug_data/Raw_26_08_2022_10_59_02.bin" #external pls, fake timing, 1 edge fc, 2 sync fc, 1 offset
fp ="D:/debug_data/Raw_26_08_2022_11_00_34.bin" #external pls, fake timing, 1 edge fc, 2 sync fc, 1 offset
fp ="D:/debug_data/Raw_26_08_2022_11_01_39.bin" #external pls, fake timing, 2 edge fc, 2 sync fc, synced



with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
cfg_paras_rec = raw[2]
runi = 0
buf0 = rawdata[runi][0]
buf1 = rawdata[runi][1]

wib_data = wib_spy_dec_syn(buf0, buf1)

flen = len(wib_data[0])

tmts = []
cdts_l0 = []
cdts_l1 = []
femb0 = []
femb1 = []
femb2 = []
femb3 = []
for i in range(flen):
    tmts.append(wib_data[0][i]["TMTS"])
    cdts_l0.append(wib_data[0][i]["FEMB_CDTS"])
    cdts_l1.append(wib_data[1][i]["FEMB_CDTS"])
    femb0.append(wib_data[0][i]["FEMB0_2"])
    femb1.append(wib_data[0][i]["FEMB1_3"])
    femb2.append(wib_data[1][i]["FEMB0_2"])
    femb3.append(wib_data[1][i]["FEMB1_3"])

femb0 = list(zip(*femb0))
femb1 = list(zip(*femb1))
femb2 = list(zip(*femb2))
femb3 = list(zip(*femb3))

wibs = [femb0, femb1, femb2, femb3]

x = np.arange(len(tmts))

if False:
    fig = plt.figure(figsize=(10,6))
    plt.plot(x, np.array(tmts)-tmts[0], label ="Time Master Timestamp")
    plt.plot(x, np.array(cdts_l0)-cdts_l0[0], label ="Coldata Timestamp")
    plt.plot(x, np.array(cdts_l1)-cdts_l1[0], label ="Coldata Timestamp")
    #for i in range(20):
    #    print (hex(tmts[i]), hex(cdts_l0[i]), hex(cdts_l1[i]), (tmts[i]&0x3ff)-(cdts_l0[i]&0x3ff) )
    plt.legend()
    plt.show()
    plt.close()
    
    for fembi in range(4):
        fig = plt.figure(figsize=(10,6))
        for i in range(128):
            plt.plot(x, wibs[fembi][i])
        plt.title(f"Waveform of FEMB{fembi}")
        plt.show()
        plt.close()

fig = plt.figure(figsize=(10,6))
for fembi in range(4):
    plt.plot(x, wibs[fembi][0], label = f"FEMB{fembi} Ch0")
plt.legend()
plt.show()
plt.close()

