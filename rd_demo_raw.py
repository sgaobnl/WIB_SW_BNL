import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
import copy

import struct
from spymemory_decode import wib_spy_dec_syn


fp ="D:/debug_data/RawRMS_23_08_2022_16_28_45.bin" 
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
femb0 = []
femb1 = []
femb2 = []
femb3 = []
for i in range(flen):
    tmts.append(wib_data[0][i]["TMTS"])
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

fig = plt.figure(figsize=(10,6))
plt.plot(x, np.array(tmts)-tmts[0], label ="Timestamp")
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

