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
chips = 8
if True:
    print ("monitor bandgap reference")
    mon_refs = {}
    for mon_chip in range(chips):
        adcrst = chk.wib_fe_mon(femb_ids=fembs, mon_type=2, mon_chip=mon_chip, sps=sps)
        mon_refs[f"chip{mon_chip}"] = adcrst

if True:
    print ("monitor temperature")
    mon_temps = {}
    for mon_chip in range(chips):
        adcrst = chk.wib_fe_mon(femb_ids=fembs, mon_type=1, mon_chip=mon_chip, sps=sps)
        mon_temps[f"chip{mon_chip}"] = adcrst

#if False:
if True:
    print ("monitor BL 200mV")
    mon_200bls = {}
    for mon_chip in range(chips):
        for mon_chipchn in range(16):
            adcrst = chk.wib_fe_mon(femb_ids=fembs, mon_type=0, snc=1, mon_chip=mon_chip, mon_chipchn=mon_chipchn, sps=sps)
            mon_200bls["chip%dchn%02d"%(mon_chip, mon_chipchn)] = adcrst

#if False:
if True:
    print ("monitor BL 900mV")
    mon_900bls = {}
    for mon_chip in range(chips):
        for mon_chipchn in range(16):
            adcrst = chk.wib_fe_mon(femb_ids=fembs, mon_type=0, snc=0, mon_chip=mon_chip, mon_chipchn=mon_chipchn, sps=sps)
            mon_900bls["chip%dchn%02d"%(mon_chip, mon_chipchn)] = adcrst
   
#for i in range(4,64,8):
#    b = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=0, sgp=True, sg0=0, sg1=0, vdac=i, sps=1 )
#    print (b)

#for chip in range(8):
#    c = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=chip, sgp=True, sg0=0, sg1=0, vdac=chip*5, sps=1 )
#    print (c)

#chk.wib_adc_mon(femb_ids=fembs, sps=1  ) 

if save:
    fdir = "D:/debug_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = fdir + "MON_FE_" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( [mon_refs, mon_temps, mon_200bls, mon_900bls], fn)

print ("DONE")
