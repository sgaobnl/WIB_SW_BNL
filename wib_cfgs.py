import low_level_commands as llc
from wib import WIB

import sys, time, random
from fe_asic_reg_mapping import FE_ASIC_REG_MAPPING

class WIB_CFGS( FE_ASIC_REG_MAPPING):
    def __init__(self):
        super().__init__()
        self.wib = WIB("192.168.121.1")
        self.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
                            [0x4, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x5, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x6, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x7, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x8, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x9, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0xA, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0xB, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                          ]
        self.adac_cali_quo = False

    def wib_init(self):
        self.wib = llc.test_connection(self.wib)
        if self.wib==1: #Connection failed
            print ("no WIB is found")
            sys.exit() 
        time.sleep(0.1)
        llc.system_clock_select(self.wib, pll=False)    

    def femb_vol_set(self, vfe=3.0, vcd=3.0, vadc=3.5):
        llc.power_config(self.wib, v1 = vfe, v2=vcd, v3=vadc)
#        llc.get_sensors(self.wib)

    def femb_powering(self, fembs = []):
        if 0 in fembs:
            femb0 = True
        else:
            femb0 = False
        if 1 in fembs:
            femb1 = True
        else:
            femb1 = False
        if 2 in fembs:
            femb2 = True
        else:
            femb2 = False
        if 3 in fembs:
            femb3 = True
        else:
            femb3 = False
        script = bytearray("", 'utf-8')
        if (femb0 | femb1 | femb2 | femb3 ):
            with open("./scripts/bias_on",'rb') as fin:
                script += fin.read()
        else:
            with open("./scripts/bias_off",'rb') as fin:
                script += fin.read()
        if femb0 == True:
            with open("./scripts/femb0_on",'rb') as fin:
                script += fin.read()
        else:
            with open("./scripts/femb0_off",'rb') as fin:
                script += fin.read()
        if femb1 == True:
            with open("./scripts/femb1_on",'rb') as fin:
                script += fin.read()
        else:
            with open("./scripts/femb1_off",'rb') as fin:
                script += fin.read()
        if femb2 == True:
            with open("./scripts/femb2_on",'rb') as fin:
                script += fin.read()
        else:
            with open("./scripts/femb2_off",'rb') as fin:
                script += fin.read()
        if femb3 == True:
            with open("./scripts/femb3_on",'rb') as fin:
                script += fin.read()
        else:
            with open("./scripts/femb3_off",'rb') as fin:
                script += fin.read()
        llc.wib_script(self.wib, script )
        print ("Wait 5 seconds")
        time.sleep(5)

    def get_sensors(self):
        return llc.get_sensors(self.wib)

    def femb_cd_rst(self):
    #Reset COLDATA
    #This fixes the problem where some COLDATAs don't toggle the pulse when they're told to
        llc.fast_command(self.wib, 'reset')
        self.adac_cali_quo = False
        time.sleep(0.05)
    #note: later all registers should be read and stored (to do)

    def femb_cd_sync(self):
        llc.fast_command(self.wib, 'sync')

    def femb_cd_edge(self):
        llc.fast_command(self.wib, 'edge')

    def femb_i2c_wr(self, femb_id, chip_addr, reg_page, reg_addr, wrdata):
        llc.cdpoke(self.wib, femb_id, chip_addr=chip_addr, reg_page=reg_page, reg_addr=reg_addr, data=wrdata)

    def femb_i2c_rd(self, femb_id, chip_addr, reg_page, reg_addr):
        rddata = llc.cdpeek(self.wib, femb_id, chip_addr=chip_addr, reg_page=reg_page, reg_addr=reg_addr )
        return rddata

    def femb_i2c_wrchk(self, femb_id, chip_addr, reg_page, reg_addr, wrdata):
        i = 0 
        while True:
            self.femb_i2c_wr(femb_id, chip_addr, reg_page, reg_addr, wrdata)
            rddata = self.femb_i2c_rd(femb_id, chip_addr, reg_page, reg_addr)
            i = i + 1
            if wrdata != rddata:
                print (f"Error, cd_lvds_current: wrdata {wrdata} != redata {rddata}, retry!")
                if i >= 10:
                    exit()
            else:
                break

    def femb_cd_cfg(self, femb_id):
#set coldata 8b10 
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x03, wrdata=0x3c)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x03, wrdata=0x3c)
#set LVDS current strength
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x11, wrdata=0x07)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x11, wrdata=0x07)
#Lengthen SCK time during SPI write for more stability
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x25, wrdata=0x40)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x25, wrdata=0x40)
#FE power on
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x27, wrdata=0x1f)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x27, wrdata=0x1f)
#tie LArASIC test pin to ground
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x26, wrdata=0x02)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x26, wrdata=0x00)
#Frame14
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x01, wrdata=0x01)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x01, wrdata=0x01)

    def femb_cd_fc_act(self, femb_id, act_cmd="idle"):
        if act_cmd == "idle":
            wrdata = 0
        elif act_cmd == "larasic_pls":
            wrdata = 0x01
        elif act_cmd == "save_timestamp":
            wrdata = 0x02
        elif act_cmd == "save_status":
            wrdata = 0x03
        elif act_cmd == "clr_saves":
            wrdata = 0x04
        elif act_cmd == "rst_adcs":
            wrdata = 0x05
        elif act_cmd == "rst_larasics":
            wrdata = 0x06
        elif act_cmd == "rst_larasic_spi":
            wrdata = 0x07
        elif act_cmd == "prm_larasics":
            wrdata = 0x08
        elif act_cmd == "relay_i2c_sda":
            wrdata = 0x09
        else:
            wrdata = 0

        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=wrdata)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x20, wrdata=wrdata)
#        time.sleep(0.01)
        llc.fast_command(self.wib,'act')
#        time.sleep(0.01)
#return to "idle" in case other FEMB runs FC 
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=0)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x20, wrdata=0)
        
    def femb_adc_cfg(self, femb_id):
        self.femb_cd_fc_act(femb_id, act_cmd="rst_adcs")

        for adc_no in range(8):
            c_id    = self.adcs_paras[adc_no][0]
            data_fmt= self.adcs_paras[adc_no][1] 
            diff_en = self.adcs_paras[adc_no][2] 
            sdc_en  = self.adcs_paras[adc_no][3] 
            vrefp   = self.adcs_paras[adc_no][4] 
            vrefn   = self.adcs_paras[adc_no][5]  
            vcmo    = self.adcs_paras[adc_no][6] 
            vcmi    = self.adcs_paras[adc_no][7] 
            autocali= self.adcs_paras[adc_no][8] 
            #start_data
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=2, reg_addr=0x01, wrdata=0x0c)
            #offset_binary_output_data_format
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x89, wrdata=data_fmt)
            #diff or se
            if diff_en == 0:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x84, wrdata=0x3b)
            if sdc_en == 0:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x80, wrdata=0x23) #SDC bypassed
            else:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x80, wrdata=0x62) #SDC on
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x98, wrdata=vrefp)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x99, wrdata=vrefn)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9a, wrdata=vcmo)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9b, wrdata=vcmi)

            if autocali:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0)
                time.sleep(0.01)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0x03)
        if autocali:
            time.sleep(0.5) #wait for ADC automatic calbiraiton process to complete
            for adc_no in range(8):
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0x00)

    def femb_fe_cfg(self, femb_id):
#reset LARASIC chips
        self.femb_cd_fc_act(femb_id, act_cmd="rst_larasics")
#        time.sleep(0.01)
        self.femb_cd_fc_act(femb_id, act_cmd="rst_larasic_spi")
#program LARASIC chips
#        time.sleep(0.01)
        for chip in range(8):
            for reg_id in range(16+2):
                if (chip < 4):
                    self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=(chip%4+1), reg_addr=(0x91-reg_id), wrdata=self.regs_int8[chip][reg_id])
                else:
                    self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=(chip%4+1), reg_addr=(0x91-reg_id), wrdata=self.regs_int8[chip][reg_id])
        self.femb_cd_fc_act(femb_id, act_cmd="clr_saves")
        time.sleep(0.01)
        self.femb_cd_fc_act(femb_id, act_cmd="prm_larasics")
        time.sleep(0.05)
        self.femb_cd_fc_act(femb_id, act_cmd="save_status")

        sts_cd1 = self.femb_i2c_rd(femb_id, chip_addr=3, reg_page=0, reg_addr=0x24)
        sts_cd2 = self.femb_i2c_rd(femb_id, chip_addr=2, reg_page=0, reg_addr=0x24)

        if (sts_cd1&0xff == 0xff) and (sts_cd2&0xff == 0xff):
            pass
        else:
            print ("LArASIC readback status is {}, {} diffrent from 0xFF".format(sts_cd1, sts_cd2))
            print ("exit anyway")
            exit()

    def femb_adac_cali(self, femb_id, phase0x07=[0,0,0,0,0,0,0,0]):
        for chip in range(8):
            self.femb_i2c_wrchk(femb_id, chip_addr=3-(chip//4), reg_page=(chip%4+1), reg_addr=0x6, wrdata=0x30        )
            self.femb_i2c_wrchk(femb_id, chip_addr=3-(chip//4), reg_page=(chip%4+1), reg_addr=0x7, wrdata=phase0x07[chip])
            self.femb_i2c_wrchk(femb_id, chip_addr=3-(chip//4), reg_page=(chip%4+1), reg_addr=0x8, wrdata=0x38        )
            self.femb_i2c_wrchk(femb_id, chip_addr=3-(chip//4), reg_page=(chip%4+1), reg_addr=0x9, wrdata=0x80        )

        self.adac_cali_quo = not self.adac_cali_quo
        self.femb_cd_fc_act(femb_id, act_cmd="larasic_pls")
        return self.adac_cali_quo

    def femb_cfg(self, femb_id, adac_pls_en = False):
        self.femb_cd_cfg(femb_id)
        self.femb_adc_cfg(femb_id)
        self.femb_fe_cfg(femb_id)
        if adac_pls_en:
            self.femb_adac_cali(femb_id)
        if femb_id == 0:
            unmask = 0xFFFFFFF0
        if femb_id == 1:
            unmask = 0xFFFFFF0F
        if femb_id == 2:
            unmask = 0xFFFFF0FF
        if femb_id == 3:
            unmask = 0xFFFF0FFF
        link_mask = llc.wib_peek(self.wib, 0xA00c0008 ) 
        llc.wib_poke(self.wib, 0xA00c0008, link_mask&unmask) #enable the link
        #self.femb_cd_sync()


#    def cfg_a_wib(self, fembs, adac_pls_en=False):
#        self.femb_cd_rst()
#        for femb_id in fembs:
#            self.femb_cfg(femb_id, adac_pls_en)

    def wib_acquire_data(self, fembs,  num_samples=1): 
        data = []
        #when buf0 is True, there must be FEMB0 or 1 presented
        #when buf1 is True, there must be FEMB2 or 3 presented
        buf0 = True if 0 in fembs or 1 in fembs else False
        buf1 = True if 2 in fembs or 3 in fembs else False 
        if (buf0 == False) and (buf1 == False):
            print("Select which FEMBs you want to read out first!")
            exit()
        for  i in range(num_samples):
            timestamps,samples = llc.llc_acquire_data(wib=self.wib, buf0=buf0, buf1=buf1, ignore_failure=True)
            data.append((timestamps,samples))
        return data


    def wib_acquire_rawdata(self, fembs,  num_samples=1): 
        data = []
        #when buf0 is True, there must be FEMB0 or 1 presented
        #when buf1 is True, there must be FEMB2 or 3 presented
        buf0 = True if 0 in fembs or 1 in fembs else False
        buf1 = True if 2 in fembs or 3 in fembs else False 
        if (buf0 == False) and (buf1 == False):
            print("Select which FEMBs you want to read out first!")
            exit()
        for  i in range(num_samples):
            rawdata = self.wib.acquire_rawdata(buf0, buf1)
            data.append(rawdata)
        return data
   

#        llc.acquire_data(self.wib, fembs, num_samples)

    #def acquire_data_cfg(self,  fembs, num_samples=1): 
        #llc.acquire_data(self.wib, fembs, num_samples)
        #when buf0 is True, there must be FEMB0 or 1 presented
        #when buf1 is True, there must be FEMB2 or 3 presented
        #buf0 = True if 0 in fembs or 1 in fembs else False
        #buf1 = True if 2 in fembs or 3 in fembs else False 
        #print (buf0, buf1, fembs)
        #if (buf0 == False) and (buf1 == False):
        #    print("Select which FEMBs you want to read out first!")
        #    exit()
        #data = []
        #for  i in range(num_samples):
        #    timestamps,samples = llc.acquire_data(self.wib, buf0 = buf0, buf1 = buf1, ignore_failure=True, print_gui = print)
        #    data.append((timestamps,samples))
        #return data
