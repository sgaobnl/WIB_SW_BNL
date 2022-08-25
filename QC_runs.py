from wib_cfgs import WIB_CFGS
import time
import sys
import numpy as np
import pickle
import copy
import os
import time, datetime, random, statistics

class QC_Runs:
    def __init__(self, fembs, sample_N):
        self.fembs = fembs
        self.sample_N = sample_N
        self.fembNo={}

        self.sncs = ["900mVBL", "200mVBL"]
        self.sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        self.sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]
 
        ####### Test enviroment logs #######

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

        ####### Create data saving directory #######

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

        self.chk=None   # WIB pointer

    def pwr_fembs(self, status):

        self.chk = WIB_CFGS()
        self.chk.wib_init()
        self.chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
        if status=='on':
            print("Turning on FEMBs")
            self.chk.femb_powering(self.fembs)
            pwr_meas = self.chk.get_sensors()
        if status=='off':
            print("Turning off FEMBs")
            self.chk.femb_powering([])

    def check_pwr_off(self, pwr_info):

       pwr_name=['Bias5V', 'PWR_FE', 'PWR_ADC', 'PWR_CD']
       n=0
       for i in self.fembs:
           pwr_meas = pwr_infor['femb{}'.format(i)]
  
           if (pwr_meas[0][1] < 0.5) and (pwr_meas[1][1] < 0.5) and (pwr_meas[2][1] < 0.5) and (pwr_meas[3][1] < 3):
               print ("FEMB {} is turned off".format(i))        
               n=n+1

       if n==4:
          return True
       else:
          return False

    def take_data(self, snc, sg0, sg1, st0, st1, dac, fp, sdd=0, sdf=0, slk0=0, slk1=0, sgp=0):
         
        cfg_paras_rec = []

        self.chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
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
               self.chk.adcs_paras[i][2]=1   # enable differential 

        for femb_id in self.fembs:
            if dac>0:
               self.chk.set_fe_board(sts=1, snc=snc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=1, dac=dac, sdd=sdd, sdf=sdf, slk0=slk0, slk1=slk1, sgp=sgp)
               adac_pls_en = 1
            if dac==0:
               self.chk.set_fe_board(sts=1, snc=snc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=0, dac=0x0, sdd=sdd, sdf=sdf, slk0=slk0, slk1=slk1, sgp=sgp)
               adac_pls_en = 0

            cfg_paras_rec.append( (femb_id, copy.deepcopy(self.chk.adcs_paras), copy.deepcopy(self.chk.regs_int8), adac_pls_en) )
            self.chk.femb_cfg(femb_id, adac_pls_en )

        time.sleep(0.5)
        pwr_meas = self.chk.get_sensors()
        rawdata = self.chk.wib_acquire_data(fembs=self.fembs, num_samples=self.sample_N) 
        
        with open(fp, 'wb') as fn:
            pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, logs], fn)

    def pwr_consumption(self):

        datadir = self.save_dir+"PWR_Meas/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 
        
        snc = 1 # 200 mV
        sg0 = 0
        sg1 = 0 # 14mV/fC
        st0 = 1
        st1 = 1 # 2us 
        dac = 0x20
        
        ####### SE #######
        self.chk.femb_cd_rst()
        fp = datadir + "PWR_SE_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp) 

        ####### SE with LArASIC buffer on #######
        self.chk.femb_cd_rst()
        fp = datadir + "PWR_SE_SDF_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sdf=1) 

        ####### DIFF #######
        self.chk.femb_cd_rst()
        fp = datadir + "PWR_DIFF_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sdd=1) 
        
    def pwr_cycle(self):

        if self.logs['env']=='RT':
           print ("Test is at room temperature, ignore power cycle test")
           return

        datadir = self.save_dir+"PWR_Cycle/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 
        
        snc = 1 # 200 mV
        sg0 = 0
        sg1 = 0 # 14mV/fC
        st0 = 1
        st1 = 1 # 2us 
        dac = 0x20
        
        ####### SE 3 cycles #######
        self.chk.femb_cd_rst()
        for i in range(3):
            fp = datadir + "PWR_cycle{}_SE_{}_{}_{}_0x{:02x}.bin".format(i,"200mVBL","14_0mVfC","2_0us",0x20)
            self.take_data(snc, sg0, sg1, st0, st1, dac, fp) 

            self.pwr_fembs('off')
            pwr_info = self.chk.get_sensors()
            pwr_status = self.check_pwr_off(pwr_info)

            nn=0
            while nn<20 or pwr_status==False:
                  time.sleep(1)
                  nn=nn+1
                  pwr_info = self.chk.get_sensors()
                  pwr_status = self.check_pwr_off(pwr_info)
                  print ("Wait {}s until completely shut down".format(nn))

            self.pwr_fembs('on')

        ####### SE with LArASIC buffer on (1 cycle)#######
        self.chk.femb_cd_rst()
        fp = datadir + "PWR_SE_SDF_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sdf=1) 

        self.pwr_fembs('off')
        pwr_info = self.chk.get_sensors()
        pwr_status = self.check_pwr_off(pwr_info)

        nn=0
        while nn<20 or pwr_status==False:
              time.sleep(1)
              nn=nn+1
              pwr_info = self.chk.get_sensors()
              pwr_status = self.check_pwr_off(pwr_info)
              print ("Wait {}s until completely shut down".format(nn))

        self.pwr_fembs('on')
 
        ####### DIFF (1 cycle) #######
        self.chk.femb_cd_rst()
        fp = datadir + "PWR_DIFF_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sdd=1) 

    def femb_leakage_cur(self):

        datadir = self.save_dir+"Leakage_Current/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 
        
        snc = 1 # 200 mV
        sg0 = 0
        sg1 = 0 # 14mV/fC
        st0 = 1
        st1 = 1 # 2us 
        dac = 0x20
         
        ####### 500 pA #######
        self.chk.femb_cd_rst()
        fp = datadir + "LC_SE_{}_{}_{}_0x{:02x}_{}.bin".format("200mVBL","14_0mVfC","2_0us",0x20, "500pA")
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, slk0=0, slk1=0) 

        ####### 100 pA #######
        self.chk.femb_cd_rst()
        fp = datadir + "LC_SE_{}_{}_{}_0x{:02x}_{}.bin".format("200mVBL","14_0mVfC","2_0us",0x20, "100pA")
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, slk0=1, slk1=0) 

        ####### 5 nA #######
        self.chk.femb_cd_rst()
        fp = datadir + "LC_SE_{}_{}_{}_0x{:02x}_{}.bin".format("200mVBL","14_0mVfC","2_0us",0x20, "5nA")
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, slk0=0, slk1=1) 

        ####### 1 nA #######
        self.chk.femb_cd_rst()
        fp = datadir + "LC_SE_{}_{}_{}_0x{:02x}_{}.bin".format("200mVBL","14_0mVfC","2_0us",0x20, "1nA")
        self.take_data(snc, sg0, sg1, st0, st1, dac, fp, slk0=1, slk1=1) 

    def femb_chk_pulse(self):

        datadir = self.save_dir+"CHK/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        sncs = self.sncs = ["900mVBL", "200mVBL"]
        sgs = self.sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        sts = self.sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]
 
        dac = 0x10
 
        for snci in range(2):
            for sgi in  range(4):
                sg0 = sgi%2
                sg1 = sgi//2 
                for sti in range(4):
                    st0 = sti%2
                    st1 = sti//2 
 
                    self.chk.femb_cd_rst()
                    fp = datadir + "CHK_SE_{}_{}_{}_0x{:02x}.bin".format(sncs[snci],sgs[sgi],sts[sti],dac)
                    self.take_data(snci, sg0, sg1, st0, st1, dac, fp) 

    def femb_rms(self):

        datadir = self.save_dir+"RMS/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        sncs = self.sncs
        sgs = self.sgs
        sts = self.sts
 
        dac = 0
 
        for snci in range(2):
            for sgi in  range(4):
                sg0 = sgi%2
                sg1 = sgi//2 
                for sti in range(4):
                    st0 = sti%2
                    st1 = sti//2 
 
                    self.chk.femb_cd_rst()
                    fp = datadir + "RMS_SE_{}_{}_{}_0x{:02x}.bin".format(sncs[snci],sgs[sgi],sts[sti],dac)
                    self.take_data(snci, sg0, sg1, st0, st1, dac, fp) 

    def femb_CALI_1(self):

        datadir = self.save_dir+"CALI1/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        snc = 1 # 200 mV BL
        sgs = self.sgs
        st0 = 1
        st1 = 1 # 2 us
 
        for sgi in  range(4):
            sg0 = sgi%2
            sg1 = sgi//2 

            for dac in range(0,64,4):
                self.chk.femb_cd_rst()
                fp = datadir + "CALI1_SE_{}_{}_{}_0x{:02x}.bin".format("200mVBL",sgs[sgi],"2_0us",dac)
                self.take_data(snc, sg0, sg1, st0, st1, dac, fp) 

    def femb_CALI_2(self):

        datadir = self.save_dir+"CALI2/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        snc = 0 # 900 mV BL
        sg0 = 0
        sg1 = 0 # 14_0 mv/fC
        st0 = 1
        st1 = 1 # 2 us
 
        for dac in range(0,64,4):
            self.chk.femb_cd_rst()
            fp = datadir + "CALI2_SE_{}_{}_{}_0x{:02x}.bin".format("900mVBL","14_0mVfC","2_0us",dac)
            self.take_data(snc, sg0, sg1, st0, st1, dac, fp) 

    def femb_CALI_3(self):

        datadir = self.save_dir+"CALI3/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        snc = 1 # 200 mV BL
        sg0 = 0
        sg1 = 0 # 14_0 mv/fC
        st0 = 1
        st1 = 1 # 2 us
 
        for dac in range(0,64):
            self.chk.femb_cd_rst()
            fp = datadir + "CALI3_SE_{}_{}_{}_0x{:02x}_sgp1.bin".format("200mVBL","14_0mVfC","2_0us",dac)
            self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sgp=1) 

    def femb_CALI_4(self):

        datadir = self.save_dir+"CALI4/"
        try:
            os.makedirs(datadir)
        except OSError:
            print ("Error to create folder %s !!! Continue to next test........"%datadir)
            return 

        snc = 0 # 900 mV BL
        sg0 = 0
        sg1 = 0 # 14_0 mv/fC
        st0 = 1
        st1 = 1 # 2 us
 
        for dac in range(0,64):
            self.chk.femb_cd_rst()
            fp = datadir + "CALI4_SE_{}_{}_{}_0x{:02x}_sgp1.bin".format("900mVBL","14_0mVfC","2_0us",dac)
            self.take_data(snc, sg0, sg1, st0, st1, dac, fp, sgp=1) 
        

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

   chkout = QC_Runs(fembs, sample_N)
   chkout.pwr_fembs('on')
   chkout.femb_rms()
   chkout.pwr_fembs('off')
   
