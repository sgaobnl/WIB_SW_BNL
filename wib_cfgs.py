import low_level_commands as llc
from wib import WIB
import copy

import sys, time, random
from fe_asic_reg_mapping import FE_ASIC_REG_MAPPING

class WIB_CFGS( FE_ASIC_REG_MAPPING):
    def __init__(self):
        super().__init__()
        self.wib = WIB("192.168.121.1")
        #self.wib = WIB("10.73.137.24")
        #self.wib = WIB("10.73.137.22")
        self.adcs_paras_init = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
                            [0x4, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x5, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x6, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x7, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x8, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0x9, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0xA, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                            [0xB, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                          ]
        self.adcs_paras = self.adcs_paras_init
        self.adac_cali_quo = False

    def wib_init(self):
        print (f"Initilize WIB")
        self.wib = llc.test_connection(self.wib)

    def wib_timing(self, pll=False, fp1_ptc0_sel=0, cmd_stamp_sync = 0x7fff):
        if self.wib==1: #Connection failed
            print ("no WIB is found")
            sys.exit() 
        llc.system_clock_select(self.wib, pll, fp1_ptc0_sel, cmd_stamp_sync)    

    def femb_vol_set(self, vfe=3.0, vcd=3.0, vadc=3.5):
        llc.power_config(self.wib, v1 = vfe, v2=vcd, v3=vadc)
#        llc.get_sensors(self.wib)

    def femb_powering(self, fembs = []):
        print (f"FEMB powering...")
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
        llc.get_sensors(self.wib) #get rid of previous measurement result
        return llc.get_sensors(self.wib)

    def en_ref10MHz(self, ref_en = False):
        if ref_en:
            llc.wib_poke(self.wib, 0xff5e00c4, 0x1033200)
            print ("P12 outputs 10MHz reference clock for signal generator")
        else:
            llc.wib_poke(self.wib, 0xff5e00c4, 0x52000)

    def wib_mon_switches(self, dac0_sel=0, dac1_sel=0, dac2_sel=0, dac3_sel=0, mon_vs_pulse_sel=0, inj_cal_pulse=0):
        reg_value = (dac0_sel&0x01) + ((dac1_sel&0x01)<<1) + ((dac2_sel&0x01)<<2) + ((dac2_sel&0x01)<<3) + ((mon_vs_pulse_sel&0x01)<<4)+ ((inj_cal_pulse&0x01)<<5)
        rdreg = llc.wib_peek(self.wib, 0xA00C003C)
        llc.wib_poke(self.wib, 0xA00C003C, (rdreg&0xffffffC0)|reg_value)

    def wib_mon_adcs(self):
        rdreg = llc.wib_peek(self.wib, 0xA00C0004, print_flg=False)
        #set bit19(mon_adc_start) to 1 and then to 0 to start monitring ADC conversion
        llc.wib_poke(self.wib, 0xA00C0004,(rdreg&0xfff7ffff)|0x80000, print_flg=False) #Set bit19 to 1
        llc.wib_poke(self.wib, 0xA00C0004,rdreg&0xfff7ffff) #set bit19 to 0
        time.sleep(0.001)
        while True:
            rdreg = llc.wib_peek(self.wib, 0xA00C0090)
            mon_adc_busy = (rdreg>>19)&0x01 
            if mon_adc_busy == 0:
                break
            else:
                time.sleep(0.001)
        rdadc01 = llc.wib_peek(self.wib, 0xA00C00C4)
        rdadc23 = llc.wib_peek(self.wib, 0xA00C00C8)
        adc0 = rdadc01&0xffff
        adc1 = (rdadc01>>16)&0xffff
        adc2 = rdadc23&0xffff
        adc3 = (rdadc23>>16)&0xffff
        return adc0, adc1, adc2, adc3

    def femb_cd_rst(self):
    #Reset COLDATA
    #This fixes the problem where some COLDATAs don't toggle the pulse when they're told to
        print ("Sending Fast command reset")
        self.adcs_paras = self.adcs_paras_init
        llc.fast_command(self.wib, 'reset')
        self.adac_cali_quo = False
        time.sleep(0.05)
    #note: later all registers should be read and stored (to do)

    def femb_cd_sync(self):
        print ("Sending Fast command sync")
        llc.fast_command(self.wib, 'sync')

    def femb_cd_edge(self):
        print ("Sending Fast command edge")
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
                if i >= 5:
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

    def femb_cd_gpio(self, femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f):
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x27, wrdata=cd1_0x27)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x27, wrdata=cd2_0x27)
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x26, wrdata=cd1_0x26)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x26, wrdata=cd2_0x26)

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
        print (f"FEMB{femb_id} is configurated")


    def femb_fe_mon(self, femb_id, adac_pls_en = 0, rst_fe=0, mon_type=2, mon_chip=0, mon_chipchn=0, snc=0,sg0=0, sg1=0 ):
        if (rst_fe != 0):
            self.set_fe_reset()

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
            chn=mon_chipchn

        self.set_fe_reset()
        self.set_fechn_reg(chip=mon_chip&0x07, chn=chn, snc=snc, sg0=sg0, sg1=sg1, smn=1, sdf=1)
        self.set_fechip_global(chip=mon_chip&0x07, stb1=stb1, stb=stb0)
        self.set_fe_sync()

        #self.femb_cfg(femb_id )
        self.femb_fe_cfg(femb_id)

        self.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)


    def wib_fe_mon(self, femb_ids, adac_pls_en = 0, rst_fe=0, mon_type=2, mon_chip=0, mon_chipchn=0, snc=0,sg0=0, sg1=0, sps=10 ):
        #step 1
        #reset all FEMBs on WIB
        self.femb_cd_rst()
        
        #step 2
        for femb_id in femb_ids:
            self.femb_fe_mon(femb_id, adac_pls_en, rst_fe, mon_type, mon_chip, mon_chipchn, snc,sg0, sg1 )
            print (f"FEMB{femb_id} is configurated")

        #step4
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        time.sleep(1)
        adcss = []
        self.wib_mon_adcs() #get rid of previous result
        for i in range(sps):
            adcs = self.wib_mon_adcs()
            adcss.append(adcs)
        return adcss

    def femb_fe_dac_mon(self, femb_id, mon_chip=0,sgp=False, sg0=0, sg1=0, vdac=0  ):
        self.set_fe_reset()
        self.set_fe_board(sg0=sg0, sg1=sg1)
        self.set_fechip_global(chip=mon_chip&0x07, swdac=3, dac=vdac, sgp=sgp)
        self.set_fe_sync()
        #self.femb_cfg(femb_id )
        self.femb_fe_cfg(femb_id)
        self.femb_cd_gpio(femb_id, cd1_0x26 = 0x00,cd1_0x27 = 0x1f, cd2_0x26 = 0x00,cd2_0x27 = 0x1f)

    def wib_fe_dac_mon(self, femb_ids, mon_chip=0,sgp=False, sg0=0, sg1=0, vdac=0, sps = 10 ): 
        #step 1
        #reset all FEMBs on WIB
        self.femb_cd_rst()
        
        #step 2
        for femb_id in femb_ids:
            self.femb_fe_dac_mon(femb_id, mon_chip,sgp=sgp, sg0=sg0, sg1=sg1, vdac=vdac  )
            print (f"FEMB{femb_id} is configurated")

        #step4
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        time.sleep(1)
        adcss = []
        self.wib_mon_adcs() #get rid of previous result
        for i in range(sps):
            adcs = self.wib_mon_adcs()
            adcss.append(adcs)
        return adcss

    def femb_adc_mon(self, femb_id, mon_chip=0, mon_i=0  ):
        adcs_addr=[0x08,0x09,0x0A,0x0B,0x04,0x05,0x06,0x07]  
        cd2_iobit432 = [6,4,5,7,3,1,0,2]
        self.femb_cd_gpio(femb_id, cd1_0x26 = 0x04,cd1_0x27 = 0x1f, cd2_0x26 = cd2_iobit432[mon_chip]<<2,cd2_0x27 = 0x1f)
        vrefp   = self.adcs_paras[mon_chip][4] 
        vrefn   = self.adcs_paras[mon_chip][5]  
        vcmo    = self.adcs_paras[mon_chip][6] 
        vcmi    = self.adcs_paras[mon_chip][7] 
        #    self.femb_i2c_wrchk(femb_id, chip_addr=3-(chip//4), reg_page=(chip%4+1), reg_addr=0x9, wrdata=0x80        )
        self.femb_i2c_wrchk(femb_id=femb_id, chip_addr=adcs_addr[mon_chip], reg_page=1, reg_addr=0x98, wrdata=vrefp) #vrefp
        self.femb_i2c_wrchk(femb_id=femb_id, chip_addr=adcs_addr[mon_chip], reg_page=1, reg_addr=0x99, wrdata=vrefn) #vrefn
        self.femb_i2c_wrchk(femb_id=femb_id, chip_addr=adcs_addr[mon_chip], reg_page=1, reg_addr=0x9a, wrdata=vcmo) #vcmo
        self.femb_i2c_wrchk(femb_id=femb_id, chip_addr=adcs_addr[mon_chip], reg_page=1, reg_addr=0x9b, wrdata=vcmi) #vcmi
        self.femb_i2c_wr(femb_id=femb_id,    chip_addr=adcs_addr[mon_chip], reg_page=1, reg_addr=0xaf, wrdata=(mon_i<<2)|0x01)

    def wib_adc_mon(self, femb_ids, sps=10, adcs_paras=self.adcs_paras_init): 
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        #step 1
        #reset all FEMBs on WIB
        self.femb_cd_rst()
           
        self.adcs_paras = adcs_paras
 
        #step 2
        mon_items = []
        mons = ["VBGR", "VCMI", "VCMO", "VREFP", "VREFN", "VBGR", "VSSA", "VSSA"]
        for mon_i in range(8):
            print (f"Monitor ADC {mons[mon_i]}")
            mon_dict = {}
            for mon_chip in range(8):
            #for mon_chip in range(1):
                for femb_id in femb_ids:
                    self.femb_adc_cfg(femb_id)
                    self.femb_adc_mon(femb_id, mon_chip=mon_chip, mon_i=mon_i  )
                    print (f"FEMB{femb_id} is configurated")
                adcss = []
                time.sleep(1)
                self.wib_mon_adcs() #get rid of previous result
                self.wib_mon_adcs() #get rid of previous result
                for i in range(sps):
                    adcs = self.wib_mon_adcs()
                    adcss.append(adcs)
                mon_dict[f"chip{mon_chip}"] = [mon_chip, mons[mon_i], self.adcs_paras[mon_chip], adcss]
                print (mon_dict[f"chip{mon_chip}"])
            mon_items.append(mon_dict)
        return mon_items

    def wib_adc_mon_chip(self, femb_ids, mon_chip=0, sps=10): 
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        #reset all FEMBs on WIB
        self.femb_cd_rst()
        
        mon_dict = {}
        mons = ["VBGR", "VCMI", "VCMO", "VREFP", "VREFN", "VBGR", "VSSA", "VSSA"]
        for mon_i in range(len(mons)):
            print (f"Monitor ADC {mons[mon_i]}")
            for femb_id in femb_ids:
                self.femb_adc_cfg(femb_id)
                self.femb_adc_mon(femb_id, mon_chip=mon_chip, mon_i=mon_i  )
                print (f"FEMB{femb_id} is configurated")
            adcss = []
            time.sleep(0.5)
            self.wib_mon_adcs() #get rid of previous result
            self.wib_mon_adcs() #get rid of previous result
            for i in range(sps):
                adcs = self.wib_mon_adcs()
                adcss.append(adcs)
            mon_dict[mons[mon_i]] = [self.adcs_paras[mon_chip], adcss]
        return mon_dict


#    def cfg_a_wib(self, fembs, adac_pls_en=False):
#        self.femb_cd_rst()
#        for femb_id in fembs:
#            self.femb_cfg(femb_id, adac_pls_en)

#    def wib_acquire_data(self, fembs,  num_samples=1): 
#        print (f"Data collection for FEMB {fembs}")
#        data = []
#        #when buf0 is True, there must be FEMB0 or 1 presented
#        #when buf1 is True, there must be FEMB2 or 3 presented
#        buf0 = True if 0 in fembs or 1 in fembs else False
#        buf1 = True if 2 in fembs or 3 in fembs else False 
#        if (buf0 == False) and (buf1 == False):
#            print("Select which FEMBs you want to read out first!")
#            exit()
#        for  i in range(num_samples):
#            timestamps,samples = llc.llc_acquire_data(wib=self.wib, buf0=buf0, buf1=buf1, ignore_failure=True)
#            data.append((timestamps,samples))
#        return data


    def wib_acquire_rawdata(self, fembs,  num_samples=1): 
        print (f"Data collection for FEMB {fembs}")
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
