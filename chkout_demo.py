from wib_cfgs import WIB_CFGS
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

class FEMB_CHKOUT:
    def __init__(self, fembs, sample_N):
        self.fembs = fembs
        self.sample_N = sample_N

    def femb_rms(self):

        fembs = self.fembs
        sample_N = self.sample_N
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
        
        sncs = ["900mVBL", "200mVBL"]
        sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

        sg0=0
        sg1=0  # 14 mV/fC

        for isnc in range(2):  # 0=900mV, 1=200mV
            for ist in range(4):
                st0=ist//2
                st1=ist%2

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
                    chk.set_fe_board(sts=1, snc=isnc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=0, dac=0x0 )
                    adac_pls_en = 0 # disable LArASIC interal calibraiton pulser
                    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
                    chk.femb_cfg(femb_id, adac_pls_en )
                time.sleep(0.5)
        
                ####################FEMBs Data taking################################
                rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns list of size 1
                if save:
                    fdir = "D:/debug_data/"
                    ts = datetime.datetime.now().strftime("%d_%m_%Y")
                    fp = fdir + "Raw_RMS_{}_{}_{}_".format(sncs[isnc],sgs[0],sts[ist]) + ts  + ".bin"
                    with open(fp, 'wb') as fn:
                        pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)
        

    def femb_asiccali(self):

        fembs = self.fembs
        sample_N = self.sample_N
        chk = WIB_CFGS()
        
        chk.wib_init()
        
        chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        chk.femb_powering(fembs)
        pwr_meas = chk.get_sensors()
        
        chk.femb_cd_rst()
        
        sncs = "200mVBL"
        sgs = "14_0mVfC"
        sts = "2_0us"

        sg0=0
        sg1=0  # 14 mV/fC
  
        snc=1 # 200 mV
        st0=1 
        st1=1 # 2us

        for idac in range(0,64,4):  # dac 
        #for idac in range(0,5,4):
            cfg_paras_rec = []
            chk.femb_cd_rst()
            for femb_id in fembs:
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
                chk.set_fe_board(sts=1, snc=snc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=1, dac=idac )
                adac_pls_en = 1 # enable LArASIC interal calibraiton pulser
                cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
                chk.femb_cfg(femb_id, adac_pls_en )
            time.sleep(0.5)
        
            rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns list of size 1
            if save:
                fdir = "D:/debug_data/"
                ts = datetime.datetime.now().strftime("%d_%m_%Y")
                fp = fdir + "Raw_CALI_{}_{}_{}_0x{:02x}_".format(sncs,sgs,sts,idac) + ts  + ".bin"
                with open(fp, 'wb') as fn:
                    pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)


    def femb_one_config(self, femb_id, chk, snci, sgi, sti, dac, sdd=0, sdf=0):

        sncs = ["900mVBL", "200mVBL"]
        sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

        snc = sncs.index(snci)
        sg0 = sgs.index(sgi)//2
        sg1 = sgs.index(sgi)%2
        st0 = sts.index(sti)//2
        st1 = sts.index(sti)%2

        cfg_paras_rec = []
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

        if sdd==1:
            for i in range(8):
                chk.adcs_paras[i][2]=1   # enable differential 

        chk.set_fe_board(sts=1, snc=snc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=1, dac=dac, sdd=sdd, sdf=sdf)
        adac_pls_en = 1 # enable LArASIC interal calibraiton pulser
        cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
        chk.femb_cfg(femb_id, adac_pls_en )
        return cfg_paras_rec
        

    def femb_difconfig(self):
        fembs = self.fembs
        sample_N = self.sample_N
        chk = WIB_CFGS()
        
        chk.wib_init()
        
        chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        chk.femb_powering(fembs)
        
        chk.femb_cd_rst()
        cfg_paras_rec = []

        cfg_paras = self.femb_one_config(0, chk, '200mVBL', '14_0mVfC', '2_0us', 0x20, 0, 0)
        cfg_paras_rec.append(cfg_paras)

        cfg_paras = self.femb_one_config(1, chk, '900mVBL', '25_0mVfC', '1_0us', 0x10, 0, 0)
        cfg_paras_rec.append(cfg_paras)

        cfg_paras = self.femb_one_config(2, chk, '200mVBL', '14_0mVfC', '2_0us', 0x20, 1, 0)
        cfg_paras_rec.append(cfg_paras)

        cfg_paras = self.femb_one_config(3, chk, '900mVBL', '14_0mVfC', '2_0us', 0x20, 0, 1)
        cfg_paras_rec.append(cfg_paras)

        time.sleep(0.5)
        pwr_meas = chk.get_sensors()
        rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns list of size 1
        if save:
           fdir = "D:/debug_data/"
           ts = datetime.datetime.now().strftime("%d_%m_%Y")
           fp = fdir + "Raw_MULTCONFIG_" + ts  + ".bin"
           with open(fp, 'wb') as fn:
                pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)

if __name__=='__main__':
                        

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

   fembs = FEMB_CHKOUT(fembs, sample_N)
   #fembs.femb_rms()
   #fembs.femb_asiccali()
   fembs.femb_difconfig()
   
#chk = WIB_CFGS()
#
#####################WIB init################################
##check if WIB is in position
#chk.wib_init()
#
#####################FEMBs powering################################
##set FEMB voltages
#chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
##power on FEMBs
#chk.femb_powering(fembs)
##Measure powers on FEMB
#pwr_meas = chk.get_sensors()
#
#####################FEMBs Configuration################################
##step 1
##reset all FEMBs on WIB
#chk.femb_cd_rst()
#
#cfg_paras_rec = []
#for femb_id in fembs:
##step 2
##Configur Coldata, ColdADC, and LArASIC parameters. 
##Here Coldata uses default setting in the script (not the ASIC default register values)
##ColdADC configuraiton
#    chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
#                        [0x4, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0x5, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0x6, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0x7, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0x8, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0x9, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0xA, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                        [0xB, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
#                      ]
#
##LArASIC register configuration
#    chk.set_fe_board(sts=1, snc=femb_id%2, st0=1, st1=1, swdac=1, dac=0x20 )
#    adac_pls_en = 1 #enable LArASIC interal calibraiton pulser
#    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
##step 3
#    chk.femb_cfg(femb_id, adac_pls_en )
#time.sleep(0.5)
#
#####################FEMBs Data taking################################
#rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns list of size 1
#if save:
#    fdir = "D:/debug_data/"
#    ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
#    fp = fdir + "Raw_" + ts  + ".bin"
#    with open(fp, 'wb') as fn:
#        pickle.dump( [rawdata, pwr_meas, cfg_paras_rec], fn)
#
