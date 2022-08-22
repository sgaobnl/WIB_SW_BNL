from wib_cfgs import WIB_CFGS
import time
import sys
import numpy as np
import pickle
import copy
import os
import time, datetime, random, statistics

class FEMB_CHKOUT:
    def __init__(self, fembs, sample_N):
        self.fembs = fembs
        self.sample_N = sample_N
        self.fembNo={}

        self.sncs = ["900mVBL", "200mVBL"]
        self.sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        self.sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

        self.logs={}

        tester=input("please input your name:  ") 
        self.logs['tester']=tester

        env_cs = input("Test is performed at cold(LN2) (Y/N)? : ")
        if ("Y" in env_cs) or ("y" in env_cs):
            env = "LN"
        else:
            env = "RT"
        self.logs['env']=env

        ToyTPC_en = input("ToyTPC at FE inputs (Y/N) : ")
        if ("Y" in ToyTPC_en) or ("y" in ToyTPC_en):
            toytpc = "150pF"
        else:
            toytpc = "0pF"
        self.logs['toytpc']=toytpc

        note = input("A short note (<200 letters):")
        self.logs['note']=note

        for i in self.fembs:
            self.fembNo['femb{}'.format(i)]=input("FEMB{} ID: ".format(i))

        self.logs['femb id']=self.fembNo

        save_dir = "D:/debug_data/"
        for key,femb_no in self.fembNo.items():
            save_dir = save_dir + "femb{}_".format(femb_no)

        save_dir = save_dir+"{}_{}".format(env,toytpc)

        n=1
        while (os.path.exists(save_dir)):
            if n==1:
                save_dir = save_dir + "_R{:03d}".format(n)
            else:
                save_dir = save_dir[:-3] + "{:03d}".format(n)
            n=n+1
            if n>20:
                raise Exception("There are more than 20 folders...") 

        try:
            os.makedirs(save_dir)
        except OSError:
            print ("Error to create folder %s"%save_dir)
            sys.exit()

        self.save_dir = save_dir+"/"

        fp = self.save_dir + "logs_env.bin"
        with open(fp, 'wb') as fn:
             pickle.dump(self.logs, fn)

    def pwr_fembs(self, status):

        chk = WIB_CFGS()
        chk.wib_init()
        chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        if status=='on':
            chk.femb_powering(fembs)
            pwr_meas = chk.get_sensors()
        if status=='off':
            print("Turning off FEMBs")
            chk.femb_powering([])

    def femb_rms(self):

        fembs = self.fembs
        sample_N = self.sample_N
        chk = WIB_CFGS()
        
        chk.wib_init()
        
        chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        chk.femb_powering(fembs)
        pwr_meas = chk.get_sensors()
        
        chk.femb_cd_rst()
        
        sncs = self.sncs
        sgs = self.sgs
        sts = self.sts

        print(" Check LArASIC rms with single-ended interface between FE and ADC")
        for snci in range(2):  # 0=900mV, 1=200mV
            for sgi in range(4):
                sg0=sgi//2
                sg1=sgi%2

                for sti in range(4):
                    st0=sti//2
                    st1=sti%2
     
                    cfg_paras_rec = []
                    time.sleep(1)
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
                        chk.set_fe_board(sts=1, snc=snci, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=0, dac=0x0 )
                        adac_pls_en = 0 # disable LArASIC interal calibraiton pulser
                        cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
                        chk.femb_cfg(femb_id, adac_pls_en )
                    time.sleep(0.5)
                    pwr_meas = chk.get_sensors()
                    rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns lsti of size 1

                    if save:
                        fdir = self.save_dir
                        fp = fdir + "Raw_RMS_SE_{}_{}_{}.bin".format(sncs[snci],sgs[sgi],sts[sti])

                        with open(fp, 'wb') as fn:
                            pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, self.logs], fn)
        
        chk.femb_cd_rst()
             
        print(" Check LArASIC rms with Differential interface between FE and ADC")
        for snci in range(2):  # 0=900mV, 1=200mV
            sg0=0
            sg1=0 # 14mV/fC

            for sti in range(4):
                st0=sti//2
                st1=sti%2
     
                cfg_paras_rec = []
                time.sleep(1)
                for femb_id in fembs:
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
                    chk.set_fe_board(sts=1, snc=snci, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=0, dac=0x0, sdd=1)
                    adac_pls_en = 0 # disable LArASIC interal calibraiton pulser
                    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
                    chk.femb_cfg(femb_id, adac_pls_en )
                time.sleep(0.5)
                pwr_meas = chk.get_sensors()
                rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns lsti of size 1

                if save:
                    fdir = self.save_dir
                    fp = fdir + "Raw_RMS_DIFF_{}_{}_{}.bin".format(sncs[snci],sgs[0],sts[sti])

                    with open(fp, 'wb') as fn:
                        pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, self.logs], fn)

    def femb_asiccali(self):

        fembs = self.fembs
        sample_N = self.sample_N
        chk = WIB_CFGS()
        
        chk.wib_init()
        
        chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        chk.femb_powering(fembs)
        pwr_meas = chk.get_sensors()
        
        chk.femb_cd_rst()
        
        sncs = self.sncs
        sgs = self.sgs
        sts = "2_0us"

        st0=1 
        st1=1 # 2us

        for idac in range(0,64,4):  # dac 
            for snci in range(2):
                for sgi in range(4):
                    sg0=sgi//2
                    sg1=sgi%2

                    cfg_paras_rec = []
                    chk.femb_cd_rst()
                    chk.femb_cd_sync()
                    time.sleep(1)
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
                        chk.set_fe_board(sts=1, snc=snci, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=1, dac=idac )
                        adac_pls_en = 1 # enable LArASIC interal calibraiton pulser
                        cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
                        chk.femb_cfg(femb_id, adac_pls_en )
        
                    time.sleep(0.5)
                    pwr_meas = chk.get_sensors()
                
                    rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns lsti of size 1
                    if save:
                        fdir = self.save_dir
                        fp = fdir + "Raw_CALI_SE_{}_{}_{}_0x{:02x}".format(sncs[snci],sgs[sgi],sts,idac)  + ".bin"
                        with open(fp, 'wb') as fn:
                            pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, self.logs], fn)
        

    def femb_one_config(self, femb_id, chk, snci, sgi, sti, dac, sdd=0, sdf=0):

        sncs = self.sncs 
        sgs = self.sgs
        sts = self.sts

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
        rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns lsti of size 1
        if save:
           fdir = self.save_dir
           fp = fdir + "Raw_MULTCONFIG_"  + ".bin"
           with open(fp, 'wb') as fn:
                pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, self.logs], fn)

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

   chkout = FEMB_CHKOUT(fembs, sample_N)
   chkout.pwr_fembs('on')
   chkout.femb_rms()
   chkout.femb_asiccali()
   chkout.pwr_fembs('off')
   
