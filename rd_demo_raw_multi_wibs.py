import sys 
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
import copy

import struct
from spymemory_decode import wib_spy_dec_syn


#fp ="/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/Raw_29_09_2022_12_37_40.bin"
fp ="data/Raw_29_09_2022_12_37_40.bin"

with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
runi = 0

print (len(rawdata[0]))
print (rawdata[runi][0][0])

dec_datas = []
for wibdata in rawdata[runi]:
    ip = wibdata[0]
    buf0 = wibdata[1][0]
    buf1 = wibdata[1][1]
    trigmode = "HW"
    buf_end_addr = wibdata[2] 
    trigger_rec_ticks = wibdata[3]
    dec_data = wib_spy_dec_syn(buf0, buf1, trigmode, buf_end_addr, trigger_rec_ticks)
    dec_datas.append(dec_data)


#exit()

#print (hex(trigger_command), hex(trigger_rec_ticks), hex(buf0_end_addr), hex(buf1_end_addr)) 

crates = []
for wib_data in dec_datas:
#    wib_data = wib_spy_dec_syn(buf0, buf1, trigmode="HW", buf_end_addr =buf0_end_addr, trigger_rec_ticks=0x3f000)
    
    flen = len(wib_data[0])
    
    tmts = []
    sfs0 = []
    sfs1 = []
    cdts_l0 = []
    cdts_l1 = []
    femb0 = []
    femb1 = []
    femb2 = []
    femb3 = []
    for i in range(flen):
        tmts.append(wib_data[0][i]["TMTS"])
        sfs0.append(wib_data[0][i]["FEMB_SF"])
        sfs1.append(wib_data[1][i]["FEMB_SF"])
        cdts_l0.append(wib_data[0][i]["FEMB_CDTS"])
        cdts_l1.append(wib_data[1][i]["FEMB_CDTS"])
        femb0.append(wib_data[0][i]["FEMB0_2"])
        femb1.append(wib_data[0][i]["FEMB1_3"])
        femb2.append(wib_data[1][i]["FEMB0_2"])
        femb3.append(wib_data[1][i]["FEMB1_3"])
    print (tmts[0:10])

    
    #print (sfs0)
    #print (sfs1)
    
    femb0 = list(zip(*femb0))
    femb1 = list(zip(*femb1))
    femb2 = list(zip(*femb2))
    femb3 = list(zip(*femb3))
    
    wibs = [femb0, femb1, femb2, femb3]
    crates.append(wibs)
    
    x = np.arange(len(tmts))
    #maxpos = np.where(wibs[0][0][0:1500] == np.max(wibs[0][0][0:1500]))[0][0]
    
    #x = np.arange(20)
    
    #if False:
    if True:
        fig = plt.figure(figsize=(10,6))
        plt.plot(x, np.array(tmts)-tmts[0], label ="Time Master Timestamp")
        plt.plot(x, np.array(cdts_l0)-cdts_l0[0], label ="Coldata Timestamp")
        plt.plot(x, np.array(cdts_l1)-cdts_l1[0], label ="Coldata Timestamp")
        #for i in range(20):
        #    print (hex(tmts[i]), hex(cdts_l0[i]), hex(cdts_l1[i]), (tmts[i]&0x3ff)-(cdts_l0[i]&0x3ff) )
        plt.legend()
        plt.show()
        plt.close()
        
#        for fembi in range(4):
#            maxpos = np.where(wibs[fembi][0][0:1500] == np.max(wibs[fembi][0][0:1500]))[0][0]
#            fig = plt.figure(figsize=(10,6))
#            for chip in range(8):
#                for chn in range(16):
#                    i = chip*16 + chn
#                    if chn == 0:
#                        plt.plot(x, wibs[fembi][i],color = 'C%d'%chip, label = "Chip%dCH0"%chip )
#                    else:
#                        plt.plot(x, wibs[fembi][i],color = 'C%d'%chip )
#            plt.title(f"Waveform of FEMB{fembi}")
#            plt.legend()
#            plt.show()
#            plt.close()
#
maxpos = np.where(crates[0][0][0][0:1500] == np.max(crates[0][0][0][0:1500]))[0][0]
x = np.arange(20)
fig = plt.figure(figsize=(10,6))
plt.plot(x, crates[0][0][0][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB0 Ch0")
plt.plot(x, crates[0][1][0][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB1 Ch0")
plt.plot(x, crates[0][2][0][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB2 Ch0")
plt.plot(x, crates[0][3][0][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB3 Ch0")
plt.plot(x, crates[1][0][0][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB0 Ch0")
plt.plot(x, crates[1][1][0][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB1 Ch0")
plt.plot(x, crates[1][2][0][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB2 Ch0")
plt.plot(x, crates[1][3][0][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB3 Ch0")
plt.legend()
plt.show()
plt.close()


#for wibi in range(len(crates)):
#    for fembi in range(4):
#for fembi in range(4):
#    maxpos = np.where(wibs[fembi][0][0:1500] == np.max(wibs[fembi][0][0:1500]))[0][0]
#    fig = plt.figure(figsize=(10,6))
#    plt.plot(x, wibs[fembi][0][maxpos-10: maxpos+10], marker='s', label = f"FEMB{fembi} Ch0")
#    plt.plot(x, wibs[fembi][16][maxpos-10: maxpos+10], marker='o', label = f"FEMB{fembi} Ch16")
#    plt.plot(x, wibs[fembi][32][maxpos-10: maxpos+10], marker='^', label = f"FEMB{fembi} Ch32")
#    plt.plot(x, wibs[fembi][48][maxpos-10: maxpos+10], marker='*', label = f"FEMB{fembi} Ch48")
#    plt.plot(x, wibs[fembi][64][maxpos-10: maxpos+10], marker='>', label = f"FEMB{fembi} Ch64")
#    plt.plot(x, wibs[fembi][80][maxpos-10: maxpos+10], marker='<', label = f"FEMB{fembi} Ch80")
#    plt.plot(x, wibs[fembi][96][maxpos-10: maxpos+10], marker='+', label = f"FEMB{fembi} Ch96")
#    plt.plot(x, wibs[fembi][112][maxpos-10: maxpos+10], marker='.', label = f"FEMB{fembi} Ch112")
#
#    plt.legend()
#    plt.show()
#    plt.close()
#
#fig = plt.figure(figsize=(10,6))
#fembi = 0
#maxpos = np.where(wibs[fembi][0][0:1500] == np.max(wibs[fembi][0][0:1500]))[0][0]
#markers = ['o', '.', '+', '*']
#for fembi in range(4):
#    plt.plot(x, wibs[fembi][0][maxpos-10: maxpos+10],  marker=markers[fembi], label = f"FEMB{fembi} Ch0")
#    plt.plot(x, wibs[fembi][16][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch16")
#    plt.plot(x, wibs[fembi][32][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch32")
#    plt.plot(x, wibs[fembi][48][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch48")
#    plt.plot(x, wibs[fembi][64][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch64")
#    plt.plot(x, wibs[fembi][80][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch80")
#    plt.plot(x, wibs[fembi][96][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch96")
#    plt.plot(x, wibs[fembi][112][maxpos-10: maxpos+10], marker=markers[fembi], label = f"FEMB{fembi} Ch112")
#plt.legend()
#plt.show()
#plt.close()
#
#x = np.arange(20)
#fig = plt.figure(figsize=(10,6))
#fembi = 0
#maxpos = np.where(wibs[fembi][0][0:1500] == np.max(wibs[fembi][0][0:1500]))[0][0]
#markers = ['o', '.', '+', '*']
#for fembi in range(4):
#    for chn in range(128):
#        if chn == 0:
#            plt.plot(x, wibs[fembi][chn][maxpos-10: maxpos+10],  marker='.', color = "C%d"%fembi, label = f"FEMB{fembi}")
#        else:
#            plt.plot(x, wibs[fembi][chn][maxpos-10: maxpos+10],  marker='.', color = "C%d"%fembi)
#plt.legend()
#plt.show()
#plt.close()

