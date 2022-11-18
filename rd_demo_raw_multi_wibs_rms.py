import sys 
import numpy as np
import pickle
import time,  random, statistics
from datetime import datetime
import matplotlib.pyplot as plt
import copy

import struct
from spymemory_decode import wib_spy_dec_syn


fp ="D:/debug_data/Raw_27_09_2022_17_59_32.bin"
fp ="D:/debug_data/Raw_28_09_2022_10_39_00.bin"
fp ="D:/debug_data/Raw_29_09_2022_12_37_40.bin"
fp ="D:/CRP5A/CRP5A_timing_debugging/Raw_17_11_2022_18_15_20.bin"
fp ="D:/CRP5A/CRP5A_timing_debugging/Raw_17_11_2022_18_20_32.bin"
fp ="D:/CRP5A/CRP5A_timing_debugging/Raw_17_11_2022_18_24_50.bin"
fp ="D:/CRP5A/CRP5A_timing_debugging/Raw_17_11_2022_18_27_47.bin"
fp ="D:/CRP5A/CRP5A_timing_debugging/Raw_17_11_2022_18_32_40.bin"
fp ="D:/CRP5A/CRP5A_data/Raw_17_11_2022_19_01_36.bin" #1200mV
fp ="D:/CRP5A/CRP5A_data/Raw_17_11_2022_19_06_24.bin" #1100mV
fp ="D:/CRP5A/CRP5A_data/Raw_17_11_2022_19_21_37.bin" #RMS

#Raw_17_11_2022_19_21_37,  chk.set_fe_board(sts=0, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac ), SG output off
#Raw_17_11_2022_19_28_22,  chk.set_fe_board(sts=1, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac ), SG output off

with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
runi = 0

print (len(rawdata[0]))
print (rawdata[runi][0][0])


all_dec_datas = []
for runi in range(len(rawdata)):
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
    all_dec_datas.append(dec_datas)


#exit()

#print (hex(trigger_command), hex(trigger_rec_ticks), hex(buf0_end_addr), hex(buf1_end_addr)) 

crates = []
fig = plt.figure(figsize=(10,6))
plt.rcParams.update({'font.size':12})
wibi = 0
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
    
    #print (sfs0)
    #print (sfs1)
    
    femb0 = list(zip(*femb0))
    femb1 = list(zip(*femb1))
    femb2 = list(zip(*femb2))
    femb3 = list(zip(*femb3))
    
    wibs = [femb0, femb1, femb2, femb3]
    crates.append(wibs)
    
    T0 = tmts[0]*512
    dt = datetime.utcfromtimestamp(T0 / 1000000000)
    t0_str = dt.strftime('%Y-%m-%d %H:%M:%S.%f')

    x = np.arange(len(tmts)) * 0.5
    #maxpos = np.where(wibs[0][0][0:1500] == np.max(wibs[0][0][0:1500]))[0][0]
    
    #x = np.arange(20)
    
    if False:
    #if True:
        plt.plot(x, np.array(tmts)-tmts[0], label =f"WIB{wibi} Time Master Timestamp")
        plt.plot(x, np.array(cdts_l0)-cdts_l0[0], label =f"WIB{wibi} Coldata0 Timestamp")
        plt.plot(x, np.array(cdts_l1)-cdts_l1[0], label =f"WIB{wibi} Coldata1 Timestamp")
        #for i in range(20):
        wibi = wibi + 1
        #    print (hex(tmts[i]), hex(cdts_l0[i]), hex(cdts_l1[i]), (tmts[i]&0x3ff)-(cdts_l0[i]&0x3ff) )

plt.title ("Timestamp in WIB data")
plt.text(0,1000, "T0 = " + t0_str)
plt.text(0,800, "T0 = %d ns"%T0 )
plt.xlabel ("Time / $\mu$s")
plt.ylabel (f"Timestamp ID - T0({tmts[0]})" )
plt.grid()
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
plt.rcParams.update({'font.size':12})
plt.plot(x, crates[0][0][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB0 Ch1")
plt.plot(x, crates[0][1][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB1 Ch1")
plt.plot(x, crates[0][2][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB2 Ch1")
plt.plot(x, crates[0][3][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB3 Ch1")
plt.plot(x, crates[1][0][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB0 Ch1")
plt.plot(x, crates[1][1][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB1 Ch1")
plt.plot(x, crates[1][2][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB2 Ch1")
plt.plot(x, crates[1][3][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB3 Ch1")

plt.plot(x, crates[0][0][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB0 Ch65")
plt.plot(x, crates[0][1][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB1 Ch65")
plt.plot(x, crates[0][2][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB2 Ch65")
plt.plot(x, crates[0][3][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB3 Ch65")
plt.plot(x, crates[1][0][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB0 Ch65")
plt.plot(x, crates[1][1][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB1 Ch65")
plt.plot(x, crates[1][2][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB2 Ch65")
plt.plot(x, crates[1][3][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB3 Ch65")

plt.title ("Waveforms")
plt.xlabel ("Time / $\mu$s")
plt.ylabel ("ADC / bit" )

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

