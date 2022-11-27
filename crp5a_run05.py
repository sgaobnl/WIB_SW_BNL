from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
from wib import WIB
import os
from rawdata_dec import rawdata_dec 


if len(sys.argv) < 2:
    print('Please specify at least one FEMB # to test')
    print('Usage: python wib.py 0')
    exit()    

save = True

fembs = [int(a) for a in sys.argv[1:5]] 
ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]
sample_N = int(sys.argv[5]) 

chk = WIB_CFGS()
sts  =      int(sys.argv[6])     
snc  =      int(sys.argv[7])     
sg0  =      int(sys.argv[8])     
sg1  =      int(sys.argv[9])     
st0  =      int(sys.argv[10])    
st1  =      int(sys.argv[11])    
sdf  =     int(sys.argv[12])    
slk0 =     int(sys.argv[13])      
slk1 =     int(sys.argv[14])  
#swdac =    int(sys.argv[15])  
#dac =    int(sys.argv[16])  
#sgp =     int(sys.argv[17])  
swdac = 0 
dac =   0 
sgp =   0 

adac_pls_en = sts
set_paras = [sts, snc, sg0, sg1, st0, st1, sdf, slk0, slk1] 
print (f"sts={sts},snc={snc},sg0={sg0}, sg1={sg1}, st0={st0}, st1={st1}, sdf={sdf}, slk0={slk0}, slk1={slk1}, swdac={swdac}, dac={dac}, sgp={sgp}") 

#run#1
runno = "Run05_DIFF"
cfg_paras_rec = []

print ("Start...")
if True:
    for ip in ips:
        chk.wib = WIB(ip) 
    
        ####################WIB init################################
        #check if WIB is in position
        #chk.wib_init()
        ####################FEMBs Configuration################################
        #chk.femb_cd_rst()
        
        for femb_id in fembs:
        #step 2
        #Configur Coldata, ColdADC, and LArASIC parameters. 
        #Here Coldata uses default setting in the script (not the ASIC default register values)
        #ColdADC configuraiton
            chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
                                [0x4, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0x5, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0x6, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0x7, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0x8, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0x9, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0xA, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                                [0xB, 0x08, 1, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                              ]
        
            chk.set_fe_board(sts=sts, snc=snc,sg0=sg0, sg1=sg1, st0=st0, st1=st1, sdf=sdf, slk0=slk0, slk1=slk1, swdac=swdac, dac=dac, sgp=sgp, sdd=1 )
            cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
        #step 3
            chk.femb_fe_cfg(femb_id)
            if adac_pls_en :
                chk.femb_adac_cali(femb_id) #disable interal calibraiton pulser from RUN01
            print (ip, "FEs on FEMB%d are configured"%femb_id)
        
if True:
    time.sleep(0.1)

    rawdata = chk.wib_acq_raw_extrig(wibips=ips, fembs=fembs, num_samples=sample_N, trigger_command=0x00,trigger_rec_ticks=0x3f000, trigger_timeout_ms = 200000) 

    pwr_meas = chk.get_sensors()

    if adac_pls_en:
        for ip in ips:
            chk.wib = WIB(ip) 
            for femb_id in fembs:
                chk.femb_adac_cali(femb_id) #disable interal calibraiton pulser from RUN01

if True:
    root_dir = sys.argv[-1]
    save_dir = "D:/CRP5A/" + root_dir + "/" + runno + "/"

    i = 0
    while (True):
        i = i + 1
        fd_new = save_dir[:-1]+"_R{:03d}/".format(i)
        if (os.path.exists(fd_new)):
            pass
        else:
            try:
                os.makedirs(fd_new)
            except OSError:
                print ("Error to create folder %s"%fd_new)
                input ("hit any button and then 'Enter' to exit")
                sys.exit()    
            save_dir = fd_new
            break

    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = save_dir + "Raw_SW_Trig" + ts  + ".bin"
    rawinfo =  [rawdata, pwr_meas, cfg_paras_rec, set_paras]
    with open(fp, 'wb') as fn:
        pickle.dump( rawinfo, fn)
        #pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, trigger_command, trigger_rec_ticks, buf0_end_addr, buf1_end_addr], fn)
    rawdata_dec(raw=rawinfo, runi=0, plot_show_en = False, plot_fn = save_dir + "pulse_response" + ts + ".png", rms_flg=True)


print (" Done!")   
