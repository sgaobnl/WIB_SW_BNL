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

localclk_cs = False
ext_cali_flg = False

if len(sys.argv) < 2:
    print('Please specify at least one FEMB # to test')
    print('Usage: python wib.py 0')
    exit()    

save = True
sample_N = 1

fembs = [int(a) for a in sys.argv[1:5]] 
ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]

chk = WIB_CFGS()

#run#1
runno = "Run10_ADC_DBEN"
cfg_paras_rec = []
adac_pls_en = 1 #enable LArASIC interal calibraiton pulser

if True:
    for ip in ips:
#        if ip == "10.73.137.27":
#            fembs=[0,1,3]
#        else:
#            fembs=[0,1,2,3]
        while True:
            chk.wib = WIB(ip) 
    
            ####################WIB init################################
            #check if WIB is in position
            #chk.wib_init()
            ####################FEMBs Configuration################################
            #step 1
            #reset all FEMBs on WIB
            chk.femb_cd_rst()
            
            for femb_id in fembs:
            #step 2
            #Configur Coldata, ColdADC, and LArASIC parameters. 
            #Here Coldata uses default setting in the script (not the ASIC default register values)
            #ColdADC configuraiton
                chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80, 1-SDC_ON, 2-DB_ON), vrefp, vrefn, vcmo, vcmi, autocali
                                    [0x4, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0x5, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0x6, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0x7, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0x8, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0x9, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0xA, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                    [0xB, 0x08, 0, 2, 0xDF, 0x33, 0x89, 0x67, 1],
                                  ]
            
            #LArASIC register configuration
                if ext_cali_flg == True:
                    swdac = 2
                    dac = 0
                else:
                    swdac = 1
                    dac = 0x20
                chk.set_fe_board(sts=1, snc=1,sg0=0, sg1=0, st0=1, st1=1, swdac=swdac, dac=dac, sdd=1 )
                #chk.set_fe_board(sts=0, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac )
                cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
            #step 3
                chk.femb_cfg(femb_id, adac_pls_en )
                if ext_cali_flg == True:
                    chk.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)
            align_flg = chk.data_align()
            if align_flg:
                break
            else:
#                pass
                chk.wib_timing(localclk_cs=localclk_cs, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
        
        if ext_cali_flg == True:
            #enable 10MHz output 
            chk.en_ref10MHz(ref_en = True)
            #external calibration from generator through P5 
            chk.wib_mon_switches(dac0_sel=0,dac1_sel=0,dac2_sel=0,dac3_sel=0, mon_vs_pulse_sel=1, inj_cal_pulse=0) 
    
if True:
    time.sleep(0.5)

    rawdata = chk.wib_acq_raw_extrig(wibips=ips, fembs=fembs, num_samples=sample_N, trigger_command=0x00,trigger_rec_ticks=0x3f000, trigger_timeout_ms = 200000) 

    pwr_meas = []
    for ip in ips:
#        if ip == "10.73.137.27":
#            fembs=[0,1,3]
#        else:
#            fembs=[0,1,2,3]
        chk.wib = WIB(ip) 
        pwr = chk.get_sensors()
        pwr_meas.append([ip, pwr])


    if adac_pls_en:
        for ip in ips:
#            if ip == "10.73.137.27":
#                fembs=[0,1,3]
#            else:
#                fembs=[0,1,2,3]
            chk.wib = WIB(ip) 
        
            for femb_id in fembs:
                chk.femb_adac_cali(femb_id) #disable interal calibraiton pulser from RUN01

if True:
    root_dir = sys.argv[-1]
    save_dir = "D:/CRP5A_3rd/" + root_dir + "/" + runno + "/"

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
    rawinfo =  [rawdata, pwr_meas, cfg_paras_rec]
    with open(fp, 'wb') as fn:
        pickle.dump( rawinfo, fn)
        #pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, trigger_command, trigger_rec_ticks, buf0_end_addr, buf1_end_addr], fn)

    chped, chmax, chmin, chped = rawdata_dec(raw=rawinfo, runs=1, plot_show_en = False, plot_fn = save_dir + "pulse_respons.png")
#
#    for ch in range(len(chped)):
#        if (chped[ch] < 4000) and ((chmax[ch]-chped[ch]) > 4000):
#            pass
#        else:
#            print ("Error, check the plot and CNTL+C to exit")

    print ("Done!")
