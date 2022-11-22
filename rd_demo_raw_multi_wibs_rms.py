import sys 
import numpy as np
import pickle
import time,  random, statistics
from datetime import datetime
import matplotlib.pyplot as plt
import copy

import struct
from spymemory_decode import wib_spy_dec_syn


fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_13_04.bin" #good,DAC= 0x30, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_19_08.bin" #good,DAC= 0x28, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_21_51.bin" #good,DAC= 0x20, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_26_01.bin" #good,DAC= 0x10, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_27_42.bin" #good,DAC= 0x18, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_30_43.bin" #good,DAC= 0x08, 14, 1, 900mV

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_32_36.bin" #good,DAC= 0x08, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_33_49.bin" #good,DAC= 0xl0, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_35_00.bin" #good,DAC= 0xl8, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_35_59.bin" #good,DAC= 0x20, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_36_56.bin" #good,DAC= 0x28, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_37_31.bin" #good,DAC= 0x30, 14, 1, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_40_17.bin" #good,DAC= 0x38, 14, 1, 200mV

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_45_03.bin" #good,DAC= 0x38, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_45_57.bin" #good,DAC= 0x30, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_46_44.bin" #good,DAC= 0x28, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_47_35.bin" #good,DAC= 0x20, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_48_32.bin" #good,DAC= 0x18, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_49_21.bin" #good,DAC= 0x10, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_50_25.bin" #good,DAC= 0x08, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_51_53.bin" #good,DAC= 0x04, 14, 2, 200mV

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_54_17.bin" #good,DAC= 0x04, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_56_09.bin" #good,DAC= 0x08, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_57_09.bin" #good,DAC= 0x10, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_58_16.bin" #good,DAC= 0x18, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_59_10.bin" #good,DAC= 0x18, 14, 2, 900mV


fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_03_23.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_06_02.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_06_45.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 900mV(snc0)

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_08_37.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_09_53.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_11_10.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_40_47.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_43_13.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 0.5(st0=1,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_45_10.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 3(st0=0,st1=1), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_45_45.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 2(st0=1,st1=1), 200mV(snc0)


fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_48_23.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 2(st0=1,st1=1), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_49_48.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 0.5(st0=1,st1=0), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_50_33.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 3(st0=0,st1=1), 900mV(snc0)

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_48_23.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 2(st0=1,st1=1), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_06_45.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 900mV(snc0)

fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_13_04.bin" #good,DAC= 0x30, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_27_42.bin" #good,DAC= 0x18, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_19_26_01.bin" #good,DAC= 0x10, 14, 1, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_57_09.bin" #good,DAC= 0x10, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_11_10.bin" #good,DAC= 0x0, 14(sg0=0,sg1=0), 1(st0=0,st1=0), 200mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_48_23.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 2(st0=1,st1=1), 900mV(snc0)
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_49_21.bin" #good,DAC= 0x10, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_48_32.bin" #good,DAC= 0x18, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_47_35.bin" #good,DAC= 0x20, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_45_57.bin" #good,DAC= 0x30, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_46_44.bin" #good,DAC= 0x28, 14, 2, 200mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_57_09.bin" #good,DAC= 0x10, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_21_58_16.bin" #good,DAC= 0x18, 14, 2, 900mV
fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig19_11_2022_22_48_23.bin" #bad,DAC= 0x0, 14(sg0=0,sg1=0), 2(st0=1,st1=1), 900mV(snc0)


#fp ="D:/CRP5A/CRP5A_data/Raw_SW_Trig21_11_2022_17_03_30.bin"
with open(fp, 'rb') as fn:
    raw = pickle.load(fn)

rawdata = raw[0]
pwr_meas = raw[1]
runi = 0

print (len(rawdata[0]))
print (rawdata[runi][0][0])


crate_runs = []
#for runi in range(len(rawdata)):
for runi in [0]:
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

    crate = []
    wibi = 0
    for wib_data in dec_datas:
        
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
        
        femb0 = list(zip(*femb0))
        femb1 = list(zip(*femb1))
        femb2 = list(zip(*femb2))
        femb3 = list(zip(*femb3))
        
        wibs = [femb0, femb1, femb2, femb3]
        crate.append(wibs)
        
        T0 = tmts[0]*512
        dt = datetime.utcfromtimestamp(T0 / 1000000000)
        t0_str = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    crate_runs.append(crate)

chns_data =[]
runs = len(crate_runs)
wib_num = 3
femb_num = 4
for wibi in  range(wib_num):
    for fembi in  range(femb_num):
        for ch in range(128):
            chns_data.append([])

for runi in range(runs):
    for wibi in  range(wib_num):
        for fembi in  range(femb_num):
            for ch in range(128):
                chns_data[wibi*512 + fembi*128 + ch] += crate_runs[runi][wibi][fembi][ch]

print (len(chns_data[0]))

chped = []
chmax = []
chmin = []
chrms = []
for ch in range(len(chns_data)):
    chmax.append(np.max(chns_data[ch][0:1000]))
    chped.append(np.mean(chns_data[ch][0:1000]))
#    if np.max(chns_data[ch][0:1000]) - np.mean(chns_data[ch][0:1000]) > 5000:
#        print (ch, hex(ch))
    chmin.append(np.min(chns_data[ch][0:1000]))
    chrms.append(np.std(chns_data[ch][0:1000]))
#exit()
fig = plt.figure(figsize=(10,6))
plt.rcParams.update({'font.size':12})
#for ch in range(0,128*12,128):
for ch in range(3,128,128):
    x = np.arange(1000)
    y = chns_data[ch][0:1000]
    plt.plot(x, y, marker='.',label = "waveform of ch%d"%ch)

plt.legend()
plt.ylabel ("ADC / bit" )
plt.grid()
plt.show()
plt.close()


x = np.arange(len(chns_data))
fig = plt.figure(figsize=(10,6))
plt.rcParams.update({'font.size':12})
plt.plot(x, chmax, marker='.',color='r', label = "pp")
plt.plot(x, chped, marker='.',color='b',  label = "ped")
plt.plot(x, chmin, marker='.',color='g',  label = "np")
plt.legend()
plt.title ("Pedestal Distribution")
plt.xlabel ("CH#")
plt.ylabel ("ADC / bit" )
plt.grid()
plt.show()
plt.close()

fig = plt.figure(figsize=(10,6))
plt.rcParams.update({'font.size':12})
plt.plot(x, chrms, marker='.', label = "rms")
plt.legend()
plt.title ("RMS Distribution")
plt.xlabel ("CH#")
plt.ylabel ("ADC / bit" )
plt.grid()
plt.show()
plt.close()


    #x = np.arange(len(tmts)) * 0.5
    #maxpos = np.where(wibs[0][0][0:1500] == np.max(wibs[0][0][0:1500]))[0][0]
    
    #x = np.arange(20)
    
#    if False:
#    #if True:
#        plt.plot(x, np.array(tmts)-tmts[0], label =f"WIB{wibi} Time Master Timestamp")
#        plt.plot(x, np.array(cdts_l0)-cdts_l0[0], label =f"WIB{wibi} Coldata0 Timestamp")
#        plt.plot(x, np.array(cdts_l1)-cdts_l1[0], label =f"WIB{wibi} Coldata1 Timestamp")
#        #for i in range(20):
#        wibi = wibi + 1
#        #    print (hex(tmts[i]), hex(cdts_l0[i]), hex(cdts_l1[i]), (tmts[i]&0x3ff)-(cdts_l0[i]&0x3ff) )
#
#plt.title ("Timestamp in WIB data")
#plt.text(0,1000, "T0 = " + t0_str)
#plt.text(0,800, "T0 = %d ns"%T0 )
#plt.xlabel ("Time / $\mu$s")
#plt.ylabel (f"Timestamp ID - T0({tmts[0]})" )
#plt.grid()
#plt.legend()
#plt.show()
#plt.close()
        
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
#maxpos = np.where(crates[0][0][0][0:1500] == np.max(crates[0][0][0][0:1500]))[0][0]
#x = np.arange(20)
#fig = plt.figure(figsize=(10,6))
#plt.rcParams.update({'font.size':12})
#plt.plot(x, crates[0][0][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB0 Ch1")
#plt.plot(x, crates[0][1][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB1 Ch1")
#plt.plot(x, crates[0][2][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB2 Ch1")
#plt.plot(x, crates[0][3][1][maxpos-10: maxpos+10], marker='o', label = "WIB0FEMB3 Ch1")
#plt.plot(x, crates[1][0][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB0 Ch1")
#plt.plot(x, crates[1][1][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB1 Ch1")
#plt.plot(x, crates[1][2][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB2 Ch1")
#plt.plot(x, crates[1][3][1][maxpos-10: maxpos+10], marker='o', label = "WIB1FEMB3 Ch1")
#
#plt.plot(x, crates[0][0][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB0 Ch65")
#plt.plot(x, crates[0][1][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB1 Ch65")
#plt.plot(x, crates[0][2][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB2 Ch65")
#plt.plot(x, crates[0][3][65][maxpos-10: maxpos+10], marker='s', label = "WIB0FEMB3 Ch65")
#plt.plot(x, crates[1][0][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB0 Ch65")
#plt.plot(x, crates[1][1][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB1 Ch65")
#plt.plot(x, crates[1][2][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB2 Ch65")
#plt.plot(x, crates[1][3][65][maxpos-10: maxpos+10], marker='s', label = "WIB1FEMB3 Ch65")
#
#plt.title ("Waveforms")
#plt.xlabel ("Time / $\mu$s")
#plt.ylabel ("ADC / bit" )
#
#plt.legend()
#plt.show()
#plt.close()


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

