#!/usr/bin/env python3
import sys
from ctypes import *

from wib import WIB
import wib_pb2 as wibpb

# // Words in the binary format of the FELIX frame14 from the WIB
# typedef struct {
    # uint32_t start_frame;
    # uint32_t wib_pre[4];
    # uint32_t femb_a_seg[56];
    # uint32_t femb_b_seg[56];
    # uint32_t wib_post[2];
    # uint32_t idle_frame;
# } __attribute__ ((packed)) frame14;

DAQ_SPY_SIZE = 0x00100000

class Frame14(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [ ('start_frame', c_uint32),
                 ('wib_pre', c_uint32*4),
                 ('femb_a_seg', c_uint32*56),
                 ('femb_b_seg', c_uint32*56),
                 ('wib_post', c_uint32*2),
                 ('idle_frame', c_uint32)]

if __name__ == "__main__":   
    #parse cmd line args
    if len(sys.argv) < 2:
        print('Please specify a file to interpret')
        print('Usage: python3')
        exit()  
        
    file = sys.argv[1]
    frames = []
    with open(file,'rb') as fin: #ref: https://dev.to/totally_chase/porting-c-structs-into-python-because-speed-2aio
        # buf0 = fin.read(DAQ_SPY_SIZE)
        # buf1 = fin.read(DAQ_SPY_SIZE)    
        frame = Frame14()
        while fin.readinto(frame) == sizeof(frame):
            frames.append(frame)
    
    print(len(frames))
    print(format(frames[0].start_frame,"08x"))
    
    
   
    
    
    
    