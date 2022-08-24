from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

if len(sys.argv) < 2:
    print('Please specify at least one FEMB # to test')
    print('Usage: python wib.py 0')
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
#chk.wib_init(pll=False)
chk.wib_init(pll=True)

####################FEMBs powering################################
#set FEMB voltages
#chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
#rdreg = llc.wib_peek(chk.wib, 0xA00c0090)
#print (hex(rdreg))
#rdreg = llc.wib_peek(chk.wib, 0xA00c0004)
#print (hex(rdreg))
#llc.wib_poke(chk.wib, 0xA00c0004, 0x20)
#rdreg = llc.wib_peek(chk.wib, 0xA00c0004)
#print (hex(rdreg))
#exit()

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
#chk.femb_cd_sync()

rdreg = llc.wib_peek(chk.wib, 0xA00c000C)
#disable fake time stamp
llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFF3))
llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFFD))
#set the init time stamp
llc.wib_poke(chk.wib, 0xA00c0018, 0x00000000)
llc.wib_poke(chk.wib, 0xA00c001C, 0x00000000)
llc.wib_poke(chk.wib, 0xA00c000C, (rdreg|0x0D))

time.sleep(0.5)

####################FEMBs Data taking################################
#rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns list of size 1
rawdata = chk.wib_acquire_rawdata(fembs=fembs, num_samples=sample_N) #returns list of size 1

pwr_meas = chk.get_sensors()

if save:
    fdir = "D:/debug_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = fdir + "RawRMS_" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)

chk.femb_powering(fembs=[])
pwr_meas = chk.get_sensors()
