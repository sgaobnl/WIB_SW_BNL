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
adcrst = chk.wib_adc_mon(femb_ids=fembs, sps=sps  ) 


if save:
    fdir = "D:/debug_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = fdir + "MON_ColdADC_" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( adcrst, fn)

print ("DONE")
