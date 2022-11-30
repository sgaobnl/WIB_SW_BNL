from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
from wib import WIB

ext_cali_flg = False
#print ("External Calibration pulse from Signal generator")
#gen_on = input ("did you set the generator, Y/N?")
#gen_on = "Y"
#if ("Y" in gen_on) or ("y" in gen_on):
#    pass
#else:
#    print ("Please set the generator first, exit")
#    exit()

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
ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]

chk = WIB_CFGS()

#if False:
if True:
    for ip in ips:
        chk.wib = WIB(ip) 
    
        ####################WIB init################################
        #check if WIB is in position
        chk.wib_init()
    
        chk.wib_timing(pll=False, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
        time.sleep(1)
    
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

            top : FE(15-0), FE(15-0), FE(15-0), FE(15-0)
        chip_id :  0            3        4          7
        logic_ch: 31-16     15-0
        
        #LArASIC register configuration
            if ext_cali_flg == True:
                swdac = 2
                dac = 0
            else:
                swdac = 1
                dac = 0x20
            chk.set_fe_board(sts=0, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac )
            chk.set_fechn_reg(chip=0, chn=0, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=1, chn=1, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=2, chn=2, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=3, chn=3, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=4, chn=4, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=5, chn=5, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=6, chn=6, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            chk.set_fechn_reg(chip=7, chn=7, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            if femb_id ==0: 
                chk.set_fechn_reg(chip=0, chn=8, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            elif femb_id ==1: 
                chk.set_fechn_reg(chip=0, chn=9, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            elif femb_id ==2: 
                chk.set_fechn_reg(chip=0, chn=10, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            elif femb_id ==3: 
                chk.set_fechn_reg(chip=0, chn=11, sts=1, snc=0, sg0=0, sg1=0, st0=0, st1=0, smn=0, sdf=0 )
            #chk.set_fe_board(sts=0, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=swdac, dac=dac )
            adac_pls_en = 1 #disable LArASIC interal calibraiton pulser
            cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
        #step 3
            chk.femb_cfg(femb_id, adac_pls_en )
            if ext_cali_flg == True:
                chk.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)
        chk.data_align()
        
        if ext_cali_flg == True:
            #enable 10MHz output 
            chk.en_ref10MHz(ref_en = True)
            #external calibration from generator through P5 
            chk.wib_mon_switches(dac0_sel=0,dac1_sel=0,dac2_sel=0,dac3_sel=0, mon_vs_pulse_sel=1, inj_cal_pulse=0) 
    
time.sleep(0.5)

sample_N = 10
rawdata = chk.wib_acq_raw_extrig(wibips=ips, fembs=fembs, num_samples=sample_N, trigger_command=0x00,trigger_rec_ticks=0x3f000, trigger_timeout_ms = 200000) 

####################FEMBs Data taking################################
#while True:
#    rdreg = llc.wib_peek(chk.wib, 0xA00C0004)
#    wrreg = (rdreg&0xffff3fff)|0xC0
#    llc.wib_poke(chk.wib, 0xA00C0004, wrreg) #reset spy buffer
#    wrreg = (rdreg&0xffff3fff)|0x00
#    llc.wib_poke(chk.wib, 0xA00C0004, wrreg) #reset spy buffer
#    
#    llc.wib_poke(chk.wib, 0xA00C0024, 0x0ffff) #spy rec time
#    rdreg = llc.wib_peek(chk.wib, 0xA00C0014)
#    wrreg = (rdreg&0xff00ffff)|0x080000
#    llc.wib_poke(chk.wib, 0xA00C0014, wrreg) #program cmd_code_trigger
#    time.sleep(1)
#
#    rdreg0 = llc.wib_peek(chk.wib, 0xA00C0004)
#    rdreg1 = llc.wib_peek(chk.wib, 0xA00C0014)
#    rdreg2 = llc.wib_peek(chk.wib, 0xA00C0080)
#    rdreg20 = llc.wib_peek(chk.wib, 0xA00C0084)
#    rdreg3 = llc.wib_peek(chk.wib, 0xA00C0094)
#    rdreg4 = llc.wib_peek(chk.wib, 0xA00C0098)
#    print (hex(rdreg0), hex(rdreg1), hex(rdreg2),hex(rdreg20), hex(rdreg3), hex(rdreg4) )
#
#    input ("send trigger")
#
#    rdreg0 = llc.wib_peek(chk.wib, 0xA00C0004)
#    rdreg1 = llc.wib_peek(chk.wib, 0xA00C0014)
#    rdreg2 = llc.wib_peek(chk.wib, 0xA00C0080)
#    rdreg20 = llc.wib_peek(chk.wib, 0xA00C0084)
#    rdreg3 = llc.wib_peek(chk.wib, 0xA00C0094)
#    rdreg4 = llc.wib_peek(chk.wib, 0xA00C0098)
#    print (hex(rdreg0), hex(rdreg1), hex(rdreg2),hex(rdreg20), hex(rdreg3), hex(rdreg4) )
#    #wrreg = (rdreg&0xff00ffff)|0x000000
#    #llc.wib_poke(chk.wib, 0xA00C0014, wrreg) #program cmd_code_trigger

#chk = WIB_CFGS()
#trigger_command = 0x08
#trigger_rec_ticks = 0x3f000
#
#for ip in ips:
#    chk.wib = WIB(ip) 
#
#    rdreg = llc.wib_peek(chk.wib, 0xA00C0004)
#    wrreg = (rdreg&0xffff3fff)|0xC0
#    llc.wib_poke(chk.wib, 0xA00C0004, wrreg) #reset spy buffer
#    wrreg = (rdreg&0xffff3fff)|0x00
#    llc.wib_poke(chk.wib, 0xA00C0004, wrreg) #reset spy buffer
#    
#    llc.wib_poke(chk.wib, 0xA00C0024, trigger_rec_ticks) #spy rec time
#    rdreg = llc.wib_peek(chk.wib, 0xA00C0014)
#    wrreg = (rdreg&0xff00ffff)|(trigger_command<<16)
#    llc.wib_poke(chk.wib, 0xA00C0014, wrreg) #program cmd_code_trigger
#
#input ("trigger...")
#
#for ip in ips:
#    chk.wib = WIB(ip) 
#    while True:
#        rdreg = llc.wib_peek(chk.wib, 0xA00C0080)
#        if rdreg&0x3 == 0x03:
#            print ("Full")
#            break
#    rawdata = chk.wib_acquire_rawdata(fembs=fembs, num_samples=sample_N, trigger_command=trigger_command,trigger_rec_ticks=trigger_rec_ticks, trigger_timeout_ms = 200000) #returns list of size 1
#    print (len(rawdata), len(rawdata[0]), len(rawdata[0][0]))
#    trigger_rec_ticks = llc.wib_peek(chk.wib, 0xA00C0024)
#    buf0_end_addr = llc.wib_peek(chk.wib, 0xA00C0094)
#    buf1_end_addr = llc.wib_peek(chk.wib, 0xA00C0098)
#    rdreg2 = llc.wib_peek(chk.wib, 0xA00C0080)
#    print (hex(trigger_rec_ticks), hex(buf0_end_addr ), hex(buf1_end_addr), hex(rdreg2)) 
#
#exit()

pwr_meas = chk.get_sensors()

if save:
    fdir = "D:/CRP5A/CRP5A_data/"
    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    fp = fdir + "Raw_SW_Trig" + ts  + ".bin"
    with open(fp, 'wb') as fn:
        pickle.dump( [rawdata, pwr_meas], fn)
        #pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, trigger_command, trigger_rec_ticks, buf0_end_addr, buf1_end_addr], fn)

