from wib_cfgs import WIB_CFGS
import low_level_commands as llc
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

print ("Monitoring , external timing from backplane")
#input ("Please make sure the connection is correct, any key to continue")

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

ext_mon_flg = True

chk = WIB_CFGS()


#if True:
#    ####################WIB init################################
#    #check if WIB is in position
#    chk.wib_init(pll=False)
    
#a = chk.wib_fe_mon(femb_ids=fembs, mon_type=0, snc=1, sps=1)
#print (a)
#for i in range(4,64,8):
#    b = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=0, sgp=True, sg0=0, sg1=0, vdac=i, sps=1 )
#    print (b)

#for chip in range(8):
#    c = chk.wib_fe_dac_mon(femb_ids=fembs, mon_chip=chip, sgp=True, sg0=0, sg1=0, vdac=chip*5, sps=1 )
#    print (c)

chk.wib_adc_mon(femb_ids=fembs, sps=1  ) 
print ("AAAAAAAAAA")

if False:
    ####################FEMBs powering################################
    #set FEMB voltages
    chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
    
    #check time system status
    #rdreg = llc.wib_peek(chk.wib, 0xA00c0090)
    rdreg = llc.wib_peek(chk.wib, 0xA00c0004)
    fp_sfp_sel = False
    if fp_sfp_sel:
        llc.wib_poke(chk.wib, 0xA00c0004, (rdreg&0xFFFFFFFF)|0x20) #front_panel
    else:
        llc.wib_poke(chk.wib, 0xA00c0004, (rdreg&0xFFFFFFDF)) #backplane
    rdreg = llc.wib_peek(chk.wib, 0xA00c0004)
    time.sleep(0.1)
    rdreg = llc.wib_peek(chk.wib, 0xA00c0090)
    
    
    
    #power on FEMBs
    chk.femb_powering(fembs)
    #Measure powers on FEMB
    #pwr_meas = chk.get_sensors()


if False:
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
        mon_chip = 0
        mon_chn = 0

        mon_type = 0
        if (mon_type==2): #monitor bandgap 
            stb0=1
            stb1=1
            chn=0
        elif (mon_type==1): #monitor temperature
            stb0=1
            stb1=0
            chn=0
        else: #monitor analog
            stb0=0
            stb1=0
            chn=mon_chn


        chk.set_fe_reset()
        chk.set_fe_board(sts=0, snc=1,sg0=0, sg1=0, st0=0, st1=0, swdac=0, sdd=0,dac=0 )
        chk.set_fechip_global(chip=mon_chip&0x07, stb1=stb1, stb=stb0, swdac=1, dac=0x10)
        chk.set_fechn_reg(chip=mon_chip&0x07, chn=chn, sts=1, snc=femb_id%2, sg0=0, sg1=0, smn=1, sdf=1)
        adac_pls_en = 1 #enable LArASIC interal calibraiton pulser
        cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )

        chk.femb_cfg(femb_id, adac_pls_en )

        if ext_mon_flg == True:
            chk.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)

    chk.femb_cd_edge()
    chk.femb_cd_sync()
    #chk.femb_cd_sync()
    
    fake_ts = False
    if fake_ts:
        rdreg = llc.wib_peek(chk.wib, 0xA00c000C)
        #disable fake time stamp
        llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFF1))
        #set the init time stamp
        llc.wib_poke(chk.wib, 0xA00c0018, 0x00000000)
        llc.wib_poke(chk.wib, 0xA00c001C, 0x00000000)
        #enable fake time stamp
        #align_en = 1, cmd_stamp_sync_en = 1
        llc.wib_poke(chk.wib, 0xA00c000C, (rdreg|0x0e))
    else:
        rdreg = llc.wib_peek(chk.wib, 0xA00c000C)
        #disable fake time stamp
        llc.wib_poke(chk.wib, 0xA00c000C, (rdreg&0xFFFFFFF1))
        #set the init time stamp
        #align_en = 1, cmd_stamp_sync_en = 1
        llc.wib_poke(chk.wib, 0xA00c000C, (rdreg|0x0C))
        rdreg = llc.wib_peek(chk.wib, 0xA00c000C)
        cmd_stamp_sync = 0x7fff #send SYNC_FAST command when cmd_stamp_syn match the DTS time stamp
        llc.wib_poke(chk.wib, 0xA00c000C, (cmd_stamp_sync<<16) + ((rdreg&0x8000FFFF)|0x0C) )
    
    time.sleep(0.5)

    #enable 10MHz output 
    chk.en_ref10MHz(ref_en = True)
    #external calibration from generator through P5 
    if ext_mon_flg == True:
        chk.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        adcs = chk.wib_mon_adcs()
        print (adcs)


#rdreg = llc.wib_peek(chk.wib, 0xff5e00c4 )
#print (hex(rdreg))
#rdreg = llc.wib_peek(chk.wib, 0xff5e00c4 )
#print (hex(rdreg))


exit()
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
