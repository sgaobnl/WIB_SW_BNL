#using wib_cfgs->zmq for configuring, but doing daqspy manually
from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

from ctypes import *

if len(sys.argv) < 2:
    print('Please specify at least one FEMB # to test')
    print('Usage: python wib.py 0 [save num_packets]')
    exit()    

if 'save' in sys.argv:
    save = True
    for i in range(len(sys.argv)):
        if sys.argv[i] == 'save':
            pos = i
            break
    sample_N = int(sys.argv[pos+1] )
    sys.argv.remove('save')
else:
    save = False
    sample_N = 1

fembs = [int(a) for a in sys.argv[1:pos]] 
print (fembs)

chk = WIB_CFGS()

####################WIB init################################
#check if WIB is in position
chk.wib_init()

####################FEMBs powering################################
#set FEMB voltages
chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
#power on FEMBs
chk.femb_powering(fembs)
#Measure powers on FEMB
pwr_meas = chk.get_sensors()

####################FEMBs Configuration################################
#step 1
#reset all FEMBs on WIB
chk.femb_cd_rst()


cfg_paras_rec = []
for femb_id in fembs:
#step 2
#Configur Coldata, ColdADC, and LArASIC parameters. 
#Here Coldata uses default setting in the script (not the ASIC default register values)
#ColdADC configuraiton
    chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
                        [0x4, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x5, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x6, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x7, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x8, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x9, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0xA, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0xB, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                      ]

#LArASIC register configuration
    chk.set_fe_board(sts=1, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=1, sdd=0,dac=0x10 )
    adac_pls_en = 1 #enable LArASIC interal calibraiton pulser
    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
#step 3
    chk.femb_cfg(femb_id, adac_pls_en )
chk.femb_cd_edge()
chk.femb_cd_sync()
chk.femb_cd_sync()

rdreg = llc.wib_peek(chk.wib, 0xA00c000C)
#disable fake time stamp
llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFF1))
#llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFFD))
#set the init time stamp
llc.wib_poke(chk.wib, 0xA00c0018, 0x00000000)
llc.wib_poke(chk.wib, 0xA00c001C, 0x00000000)
#enable fake time stamp
#llc.wib_poke(chk.wib, 0xA00c000C, (rdreg|0x02))
llc.wib_poke(chk.wib, 0xA00c000C, (rdreg|0x0e))

time.sleep(0.5)

#######NEW CODE##########
#implementing wib.cc::read_daq_spy
def wib_write_mask(wib, addr, val, mask = 0xFFFFFFFF):
    if mask == 0xFFFFFFFF:
        llc.wib_poke(wib, addr, val)
    else:
        old = llc.wib_peek(wib, addr)
        val = (val & mask) | ((~mask) & old)
        llc.wib_poke(wib, addr, val)
  
    #could verify after writing?
DAQ_SPY_0               = 0xA0100000;
DAQ_SPY_1               = 0xA0200000;
REG_FW_CTRL             = 0xA00c0004
REG_TIMING_CMD_1        = 0xA00c0014
REG_DAQ_SPY_REC         = 0xA00c0024   

DAQ_SPY_SIZE            = 0x00100000

buf0 = True if 0 in fembs or 1 in fembs else False
buf1 = True if 2 in fembs or 3 in fembs else False 
prev = llc.wib_peek(chk.wib, REG_FW_CTRL)
mask = 0
if (buf0):
	mask = mask | (1 << 0)
if (buf1):
	mask = mask | (1 << 1)
prev = prev & (~(mask << 6))
nxt = prev | (mask << 6)
print("Starting acquisition...")
trig_code = 0
spy_rec_time = 0
wib_write_mask(chk.wib, REG_TIMING_CMD_1, trig_code<<16, 0xFF0000)
wib_write_mask(chk.wib, REG_DAQ_SPY_REC, spy_rec_time, 0x3FFFF)
llc.wib_poke(chk.wib, REG_FW_CTRL, nxt)
llc.wib_poke(chk.wib, REG_FW_CTRL, prev)
time.sleep(0.01)
print("Performed asynchronous acquisition")
#buf0 = ctypes.string_at(DAQ_SPY_0, DAQ_SPY_SIZE) if buf0 else ""
#buf1 = ctypes.string_at(DAQ_SPY_1, DAQ_SPY_SIZE) if buf1 else ""
# buf0 = (c_char * DAQ_SPY_SIZE)()
# buf1 = (c_char * DAQ_SPY_SIZE)()
# memmove(buf0, DAQ_SPY_0, DAQ_SPY_SIZE)
# memmove(buf1, DAQ_SPY_1, DAQ_SPY_SIZE)

rawdata = chk.wib_acquire_rawdata(fembs=fembs, num_samples=sample_N) #returns list of size 1
#print(rawdata)
sample0 = rawdata[0]
buf0, buf1 = sample0
print(len(buf0))
print(len(buf1))
# print(buf0)
# print(buf1)
 
if save:
    #fdir = "D:/debug_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = "RawRMS_" + ts  + ".bin"#fp = fdir + "RawRMS_" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( [buf0, buf1], fn)
    print("Wrote into: "+fp)
    
# print("Testing accessing a single byte at DAQ_SPY_0")
# if not isinstance(cptr, ctypes.POINTER(ctypes.c_char)):
    # raise TypeError('expected char pointer')
# res = bytearray(length)
# rptr = (ctypes.c_char * length).from_buffer(res)
# if not ctypes.memmove(rptr, cptr, length):
    # raise RuntimeError('memmove failed')
