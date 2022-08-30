from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics


ext_cali_flg = True
print ("External Calibration pulse from Signal generator")
gen_on = input ("did you set the generator, Y/N?")
if ("Y" in gen_on) or ("y" in gen_on):
    pass
else:
    print ("Please set the generator first, exit")
    exit()

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
    if ext_cali_flg == True:
        swdac = 2
        dac = 0
    else:
        swdac = 0
        dac = 0
    chk.set_fe_board(sts=1, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac )
    adac_pls_en = 0 #disable LArASIC interal calibraiton pulser
    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
#step 3
    chk.femb_cfg(femb_id, adac_pls_en )
    if ext_cali_flg == True:
        chk.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)

chk.femb_cd_edge()
chk.femb_cd_edge()

chk.femb_cd_sync()
chk.femb_cd_sync()

if ext_cali_flg == True:
    #enable 10MHz output 
    chk.en_ref10MHz(ref_en = True)
    #external calibration from generator through P5 
    chk.wib_mon_switches(dac0_sel=0,dac1_sel=0,dac2_sel=0,dac3_sel=0, mon_vs_pulse_sel=1, inj_cal_pulse=0) 

time.sleep(0.5)
####################FEMBs Data taking################################
pwr_meas = chk.get_sensors()

for i in range(20):
    rawdata = chk.wib_acquire_rawdata(fembs=fembs, num_samples=sample_N) #returns list of size 1
    
#    chk.femb_cd_edge()
#    chk.femb_cd_edge()

    time.sleep(1)
    rdreg = llc.wib_peek(chk.wib, 0xA00C000C)
    print ( 0xA00C000C, hex(rdreg) )
    print (hex( llc.wib_peek(chk.wib, 0xA00C00A8) ))
    print (hex( llc.wib_peek(chk.wib, 0xA00C00AC) ))
    print (hex( llc.wib_peek(chk.wib, 0xA00C00B0) ))
    print (hex( llc.wib_peek(chk.wib, 0xA00C00B4) ))
    print (hex( llc.wib_peek(chk.wib, 0xA00C00BC) ))
    input ("continue")
   
    if save:
        fdir = "D:/debug_data/"
        ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        fp = fdir + "Raw_" + ts  + ".bin"
        with open(fp, 'wb') as fn:
            pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)
    



