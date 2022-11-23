import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
import copy

import struct

if len(sys.argv) < 2:
    print('Please specify a filename')
    print('Usage: python lowlevel_frameread.py file')
    exit()  
    
fp = sys.argv[1]
with open(fp, 'rb') as fn:
    raw = pickle.load(fn)
#buf0 = raw[0]
#buf1 = raw[1]

print(len(raw))
rawdata = raw[0]
pwr_meas = raw[1]
cfg_paras_rec = raw[2]

sample0 = rawdata[0]
buf0 = sample0[0]
buf1 = sample0[1]

print(len(buf0))
print(len(buf1))

SOF = 0X3C
IDLE = 0XBC
PACKET_LENGTH = 119



for bufnum, buf in enumerate([buf0, buf1]):
    frames_unordered = []
    frames_ordered = []   
    dropped_frames = []
    timestamps = []
    timestamps_ordered = []
    if len(buf) > 0:
        #implement extract_frames
        num_words = int(len(buf) // 4)
        words = list(struct.unpack_from("<%dI"%(num_words),buf))       
        print(len(words))
        i = 0
        while i < num_words:
            if words[i] == SOF:
                # for j in range(i+1, i+PACKET_LENGTH):
                new_frame = []
                print("SOF at %d"%(i))
                sof_i = i
                j = i + 1
                #print("Raw header data pre-extraction:")
                #print ("word#1, word#2, word#3, word#4, timing master time stamp, CDTS-ID[0-2], Coldata time stampe")                
                dt = (words[i+1+2] + words[i+1+1])>>5
                ts_link = (words[i+1+3] & 0x0000e000)>>13
                ts = (words[i+1+4]>>21)&0x3ff
                dt_low5 = (words[i+1+2] + words[i+1+1])&0x1f
                ts_low5 = (words[i+1+4]>>16)&0x1f
                print (hex(words[i+1+1]),hex(words[i+1+2]), hex(words[i+1+3]), hex(words[i+1+4]), hex(dt), hex(ts_link), hex(ts))                
                while j < i + PACKET_LENGTH:                    
                    
                    if words[j%num_words] == SOF or words[j%num_words] == IDLE:
                        print("bad frame word at %d"%(j%num_words))
                        for x in range(PACKET_LENGTH+1):
                            if i+x == j:
                                print("*%08x*"%(words[(i+x)%num_words]),end=" ")
                            else:
                                print("%08x"%(words[(i+x)%num_words]),end=" ")
                            if x%8 == 7:
                                print("")
                        print("")                        
                        i = j                        
                        break
                    j = j + 1
                if i == j:
                    print("Wasn't a full frame")
                    dropped_frames.append(sof_i)
                    continue
                if words[(i+PACKET_LENGTH+1)%num_words] != IDLE:                    
                    print("Missing trailing idle in word %d"%(len(frames_unordered)))
                    for x in range(141):
                        if x == PACKET_LENGTH+1:
                            print("*%08x*"%(words[(i+x)%num_words]),end=" ")
                        else:
                            print("%08x"%(words[(i+x)%num_words]),end=" ")
                        if x%8 == 7:
                            print("")
                    print("")
                    dropped_frames.append(sof_i)
                    i = i + 1
                    continue
                #Frame is valid
                print("SOF at %d is a valid frame"%(i))
                if i+PACKET_LENGTH+1 > num_words: #wrapped around buffer
                    start = num_words - i
                    rest = PACKET_LENGTH + 1 - start
                    new_frame = new_frame + words[i+1:i+1+start]
                    new_frame = new_frame + words[:rest]
                else:   #one segment
                    new_frame = words[i+1:i+1+PACKET_LENGTH+1]
                #print("new_frame created of length %d"%(len(new_frame)))
                frames_unordered.append(new_frame)
                timestamps.append(dt)
                i = i + PACKET_LENGTH + 1
            else:
                i = i + 1
        print("Found %d valid frames"%(len(frames_unordered)))
        print("Dropped frames: from SOFs at "+str(dropped_frames))

        #implement reorder_frames
        min_t = timestamps[0]
        min_i = 0
        for i, t in enumerate(timestamps):
            if t < min_t:
                print("min timestamp is %x and this timestamp is %x for frame %d\n"%(min_t, t, i))
                min_t = t
                min_i = i
        if min_i is not 0:
            start = len(frames_unordered) - min_i
            rest = min_i
            frames_ordered = frames_ordered + frames_unordered[min_i:min_i+start]
            frames_ordered = frames_ordered + frames_unordered[:rest]
            timestamps_ordered = timestamps_ordered + timestamps[min_i:min_i+start]
            timestamps_ordered = timestamps_ordered + timestamps[:rest]
        else:
            print("Did not have to reorder")
            frames_ordered = frames_unordered[:]
            timestamps_ordered = timestamps[:]
        #graph timestamps
        # plt.plot(timestamps, label='Unordered')
        # plt.plot(timestamps_ordered, label = 'ordered')
        # plt.title('WIB Timestamps')
        # plt.legend()
        ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        # plt.savefig('timestamps_'+ts+'.png')  
        # plt.close()
        for i in range(len(timestamps_ordered) - 1):
            if timestamps_ordered[i+1] - timestamps_ordered[i] is not 0x1:
                print("Between frame %d and %d, jump from %x to %x"%(i,i+1,frames_ordered[i],frames_ordered[i+1]))
        
        unpacked_buf = { #modeled after channel_data https://github.com/DUNE-DAQ/dune-wib-firmware/blob/master/sw/src/unpack.h#L79
            "channel_data": [[[0 for sample in range(len(frames_ordered))] for channel in range(128)] for femb in range(2)],
            "timestamp": [0 for sample in range(len(frames_ordered))],
            "crate_num": 0,
            "wib_num": 0
        }
        
        # how U,V,X numbers map to channels on a single FEMB
        u_to_ch = [20, 59, 19, 60, 18, 61, 17, 62, 16, 63, 4, 43, 3, 44, 2, 
            45, 1, 46, 0, 47, 68, 107, 67, 108, 66, 109, 65, 110, 64, 
            111, 84, 123, 83, 124, 82, 125, 81, 126, 80, 127];
        v_to_ch = [25, 54, 24, 55, 23, 56, 22, 57, 21, 58, 9, 38, 8, 39, 7, 
            40, 6, 41, 5, 42, 73, 102, 72, 103, 71, 104, 70, 105, 69,
            106, 89, 118, 88, 119, 87, 120, 86, 121, 85, 122];
        x_to_ch = [31, 48, 30, 49, 29, 50, 28, 51, 27, 52, 26, 53, 15, 32,
            14, 33, 13, 34, 12, 35, 11, 36, 10, 37, 79, 96, 78, 97, 
            77, 98, 76, 99, 75, 100, 74, 101, 95, 112, 94, 113, 93, 
            114, 92, 115, 91, 116, 90, 117];        
        
        #deframe data
        #unpack14 https://github.com/DUNE-DAQ/dune-wib-firmware/blob/master/sw/src/unpack.cc#L6        
        for n, frame in enumerate(frames_ordered):
            frame_data = [frame[5:5+56], frame[5+56:5+56*2]]
            if n == 0:
                for w, word in enumerate(frame):
                    print("%08x"%(word),end=" ")
                    if w%8 == 7:
                        print("")
            for femb in range(2):
            
                u = [0 for l in range(40)]
                v = [0 for l in range(40)]
                x = [0 for l in range(48)]
                #see https://docs.google.com/spreadsheets/d/1-Ag-uCqHwvNReRzjYC8EQuY1Dn0n_ttM/edit#gid=1930588249
                #for channel data structure
                
                for i in range(128): #i == n'th U,V,X value
                    if i < len(u):
                        a = u
                        ii = i
                    elif i < len(u) + len(v):
                        a = v
                        ii = i - len(v)
                    else:
                        a = x
                        ii = i - len(u) - len(v)
                    low_bit = i*14
                    low_word = low_bit // 32
                    high_bit = (i+1)*14-1
                    high_word = high_bit // 32
                    #print("word %d :: low %d (%d[%d]) high %d (%d[%d])"%(i,low_bit,low_word,low_bit%32,high_bit,high_word,high_bit%32));
                    #channel endianness?
                    if low_word == high_word:
                        a[ii] = (frame_data[femb][low_word] >> (low_bit%32)) & 0x3fff
                    else:
                        high_off = high_word*32-low_bit

                        a[ii] = (frame_data[femb][low_word] >> (low_bit%32)) & (0x3fff >> (14-high_off))
                        a[ii] = a[ii] | (frame_data[femb][high_word] << high_off) & ((0x3fff << high_off) & 0x3fff)
                    #uvx to channel index converter
                unpacked_buf["timestamp"][n] = timestamps_ordered[n]

                for j in range(len(u)):
                    k = u_to_ch[j]
                    unpacked_buf["channel_data"][femb][k][n] = u[j]
                for j in range(len(v)):
                    k = v_to_ch[j]
                    unpacked_buf["channel_data"][femb][k][n] = v[j]
                for j in range(len(x)):
                    k = x_to_ch[j]
                    unpacked_buf["channel_data"][femb][k][n] = x[j]     
                
        #add crate_num and wib_num assignment
        
            #plot data to see if it's coherent
        for femb in range(2):
            for i in range(128):
                t = unpacked_buf["timestamp"]
                adc = unpacked_buf["channel_data"][femb][i]
                plt.plot(t,adc)
            plt.xlabel('WIB timestamp')
            plt.ylabel('ADC counts')
            plt.title('FEMB%d'%(2*bufnum+femb))
            plt.savefig('FEMB%d'%(2*bufnum+femb)+ts)