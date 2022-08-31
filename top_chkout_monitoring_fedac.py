from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

print ("Monitoring FE Parameters")

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

chk = WIB_CFGS()

####################WIB init################################
#check if WIB is in position
chk.wib_init()
chk.wib_timing(pll=True, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)


sps = 1
chips = 1
mon_fedacs_sgp1 = {}
#for vdac in range(0, 64, 4):
for vdac in range(64):
    print("1 DAC ", vdac)
    for mon_chip in range(chips):
        adcrst = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=mon_chip, sgp=True, vdac=vdac, sps=sps )
        mon_fedacs_sgp1["VDAC%02dCHIP%d_SGP1"%(vdac, mon_chip)] = adcrst
#print (mon_fedacs_sgp1)

mon_fedacs_14mVfC = {}
for vdac in range(0,64,4):
#for vdac in range(0, 64, 16):
    print("2 DAC ", vdac)
    for mon_chip in range(chips):
        adcrst = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=mon_chip, sgp=False, sg0=0, sg1=0, vdac=vdac, sps=sps )
        mon_fedacs_14mVfC["VDAC%02dCHIP%d_SGP1"%(vdac, mon_chip)] = adcrst
#print (mon_fedacs_14mVfC)


if save:
    fdir = "D:/debug_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = fdir + "MON_FE_" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( [mon_fedacs_sgp1, mon_fedacs_14mVfC], fn)

print ("DONE")
