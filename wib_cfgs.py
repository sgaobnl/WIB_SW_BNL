import low_level_commands as llc
from wib import WIB
import copy
import sys, time, random
from fe_asic_reg_mapping import FE_ASIC_REG_MAPPING

class WIB_CFGS( FE_ASIC_REG_MAPPING):
    def __init__(self):
        super().__init__()
        #self.wib = WIB("192.168.121.1")
        self.wib = WIB("10.73.137.27")
        self.i2cerror = False
        #self.wib = WIB("10.73.137.30")
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

    def wib_i2c_adj(self, n = 300):
        rdreg = llc.wib_peek(self.wib, 0xA00C0004)
        for i in range(n):
            llc.wib_poke(self.wib,0xA00C0004 , rdreg|0x00040000) 
            rdreg = llc.wib_peek(self.wib, 0xA00C0004)
            llc.wib_poke(self.wib,0xA00C0004 , rdreg&0xfffBffff) 

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
        if len(fembs) != 0:
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

    def femb_cd_edge_act(self, fembs):
        wrdata = 0x05
        for femb_id in fembs:
            self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=wrdata)
            self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x20, wrdata=wrdata)
        llc.fast_command(self.wib, 'edge_act')
        wrdata = 0x00
        for femb_id in fembs:
            self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=wrdata)
            self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x20, wrdata=wrdata)


    def femb_i2c_wr(self, femb_id, chip_addr, reg_page, reg_addr, wrdata):
        llc.cdpoke(self.wib, femb_id, chip_addr=chip_addr, reg_page=reg_page, reg_addr=reg_addr, data=wrdata)

    def femb_i2c_rd(self, femb_id, chip_addr, reg_page, reg_addr):
        rddata = llc.cdpeek(self.wib, femb_id, chip_addr=chip_addr, reg_page=reg_page, reg_addr=reg_addr )
        return rddata

    def femb_i2c_wrchk(self, femb_id, chip_addr, reg_page, reg_addr, wrdata):
        i = 0 
        self.femb_i2c_wr(femb_id, chip_addr, reg_page, reg_addr, wrdata)
        rddata = self.femb_i2c_rd(femb_id, chip_addr, reg_page, reg_addr)
        i = i + 1
        if wrdata != rddata:
            print ("Error, I2C: femb_id=%x, chip_addr=%x, reg_page=%x, reg_addr=%x, wrdata=%x, rddata=%x, retry!"%(femb_id, chip_addr, reg_page, reg_addr, wrdata, rddata))
            self.i2cerror = True
        
    def data_cable_latency(self, femb_id):
        # set WIB_FEEDBACK_CODE registers to B2
        self.femb_i2c_wr(femb_id, chip_addr=3, reg_page=0, reg_addr=0x2B, wrdata=0xB2)
        self.femb_i2c_wr(femb_id, chip_addr=3, reg_page=0, reg_addr=0x2C, wrdata=0xB2)
        self.femb_i2c_wr(femb_id, chip_addr=3, reg_page=0, reg_addr=0x2D, wrdata=0xB2)
        # set ACTCOMMANDREG register to 9
        self.femb_i2c_wr(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=0x09)
        #issue FAST ACT command to enable loopback
        llc.fast_command(self.wib,'act')
        for i in range(6):
            if femb_id == 0:
                btr = 0xA0010000
            elif femb_id == 1:
                btr = 0xA0050000
            elif femb_id == 2:
                btr = 0xA0070000
            elif femb_id == 3:
                btr = 0xA0090000
            llc.wib_poke(self.wib, btr + 0x8, 0) #dummy writes
        llc.wib_poke(self.wib, btr + 0x8, 1) #issue stimulus
        time.sleep(0.01)
        rdreg = llc.wib_peek(self.wib, btr + 0x8) #read measured latency
        print (hex(rdreg))
        llc.wib_poke(self.wib, btr + 0x8, 0) #dummy writes
        self.femb_i2c_wr(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=0x00)

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
        time.sleep(0.001)
#return to "idle" in case other FEMB runs FC 
        self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=0, reg_addr=0x20, wrdata=0)
        self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=0, reg_addr=0x20, wrdata=0)
        time.sleep(0.01)
        
    def data_align(self, fembs=[0, 1, 2,3]):
        print ("Data aligning...")
        self.femb_cd_sync() #sync should be sent before edge
        time.sleep(0.01)
        self.femb_cd_edge()
        time.sleep(0.1)
        
        rdaddr = 0xA00C0010
        rdreg = llc.wib_peek(self.wib, rdaddr)
        wrvalue = 0x10 #cmd_code_edge = 0x10
        wrreg = (rdreg & 0xffff00ff) + ((wrvalue&0xff)<<8)
        llc.wib_poke(self.wib, rdaddr, wrreg) 
        
        rdaddr = 0xA00C000C
        rdreg = llc.wib_peek(self.wib, rdaddr)
        wrvalue = 0x7fec #cmd_stamp_sync = 0x7fec
        wrreg = (rdreg & 0x0000ffff) + ((wrvalue&0xffff)<<16)
        llc.wib_poke(self.wib, rdaddr, wrreg) 
        
        rdaddr = 0xA00C000C
        rdreg = llc.wib_peek(self.wib, rdaddr)
        wrvalue = 0x1 #cmd_stamp_sync_en = 1
        wrreg = (rdreg & 0xfffffffb) + ((wrvalue&0x1)<<2)
        llc.wib_poke(self.wib, rdaddr, wrreg) 
                
        for dts_time_delay in  range(0x48, 0x90,1):
            rdaddr = 0xA00C000C
            rdreg = llc.wib_peek(self.wib, rdaddr)
            wrvalue = dts_time_delay #0x58 #dts_time_delay = 1
            wrreg = (rdreg & 0xffff00ff) + ((wrvalue&0xff)<<8)
            llc.wib_poke(self.wib, rdaddr, wrreg) 
            rdaddr = 0xA00C000C
            rdreg = llc.wib_peek(self.wib, rdaddr)
            wrvalue = 0x1 #align_en = 1
            wrreg = (rdreg & 0xfffffff7) + ((wrvalue&0x1)<<3)
            llc.wib_poke(self.wib, rdaddr, wrreg) 
            time.sleep(0.2)
            if 0 in fembs:
                link0to3 = llc.wib_peek(self.wib, 0xA00C00A8)
            else:
                link0to3 = 0x0
            if 1 in fembs:
                link4to7 = llc.wib_peek(self.wib, 0xA00C00AC)
            else:
                link4to7 = 0x0
            if 2 in fembs:
                link8tob = llc.wib_peek(self.wib, 0xA00C00B0)
            else:
                link8tob = 0x0
            if 3 in fembs:
                linkctof = llc.wib_peek(self.wib, 0xA00C00B4)
            else:
                linkctof = 0x0

            if ((link0to3 & 0xe0e0e0e0) == 0) and ((link4to7 & 0xe0e0e0e0) == 0)and ((link8tob & 0xe0e0e0e0) == 0) and ((linkctof & 0xe0e0e0e0) == 0):
                print ("Data is aligned when dts_time_delay = 0x%x"%dts_time_delay )
                return True
            if dts_time_delay >= 0x8f:
                print ("Error: data can't be aligned, Retry...")
                return False

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
            elif sdc_en == 1:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x80, wrdata=0x62) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x8F, wrdata=0x9D) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x90, wrdata=0x9D) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x91, wrdata=0x9D) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x92, wrdata=0x9D) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9D, wrdata=0x27) #SDC on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9E, wrdata=0x27) #SDC on
            else:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x80, wrdata=0xA1) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x8F, wrdata=0x9D) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x90, wrdata=0x9D) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x91, wrdata=0x9D) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x92, wrdata=0x9D) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9D, wrdata=0x27) #DB on
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9E, wrdata=0x27) #DB on

            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x98, wrdata=vrefp)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x99, wrdata=vrefn)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9a, wrdata=vcmo)
            self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9b, wrdata=vcmi)

            if autocali:
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0)
                time.sleep(0.01)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0x03)
        if autocali&0x01:
            time.sleep(0.5) #wait for ADC automatic calbiraiton process to complete
            for adc_no in range(8):
                c_id    = self.adcs_paras[adc_no][0]
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0x9f, wrdata=0x00)
        if autocali&0x02: #output ADC back-end data pattern
            for adc_no in range(8):
                c_id    = self.adcs_paras[adc_no][0]
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0xB2, wrdata=0x20)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0xB3, wrdata=0xCD)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0xB4, wrdata=0xAB)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0xB5, wrdata=0x34)
                self.femb_i2c_wrchk(femb_id, chip_addr=c_id, reg_page=1, reg_addr=0xB6, wrdata=0x12)

    def femb_fe_cfg(self, femb_id):
        #reset LARASIC chips
        self.femb_cd_fc_act(femb_id, act_cmd="rst_larasics")
        time.sleep(0.01)
        self.femb_cd_fc_act(femb_id, act_cmd="rst_larasic_spi")
        #program LARASIC chips
        time.sleep(0.01)
        for chip in range(8):
            for reg_id in range(16+2):
                if (chip < 4):
                    self.femb_i2c_wrchk(femb_id, chip_addr=3, reg_page=(chip%4+1), reg_addr=(0x91-reg_id), wrdata=self.regs_int8[chip][reg_id])
                else:
                    self.femb_i2c_wrchk(femb_id, chip_addr=2, reg_page=(chip%4+1), reg_addr=(0x91-reg_id), wrdata=self.regs_int8[chip][reg_id])
        i = 0
        while True:
            self.femb_cd_fc_act(femb_id, act_cmd="clr_saves")
            time.sleep(0.01)
            self.femb_cd_fc_act(femb_id, act_cmd="prm_larasics")
            time.sleep(0.05)
            self.femb_cd_fc_act(femb_id, act_cmd="save_status")
            time.sleep(0.005)

            sts_cd1 = self.femb_i2c_rd(femb_id, chip_addr=3, reg_page=0, reg_addr=0x24)
            sts_cd2 = self.femb_i2c_rd(femb_id, chip_addr=2, reg_page=0, reg_addr=0x24)

            if (sts_cd1&0xff == 0xff) and (sts_cd2&0xff == 0xff):
                break
            else:
                print ("LArASIC readback status is {}, {} diffrent from 0xFF".format(sts_cd1, sts_cd2))
                if i > 10:
                    print ("exit anyway")
                    exit()
                else:
                    time.sleep(0.1)
            i = i + 1

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
        refi= 0
        while True:
            self.femb_cd_cfg(femb_id)
            self.femb_adc_cfg(femb_id)
            self.femb_fe_cfg(femb_id)
            if adac_pls_en:
                self.femb_adac_cali(femb_id)
            link_mask = llc.wib_peek(self.wib, 0xA00C0008)
            if femb_id == 0:
                link_mask = link_mask&0xfff0
            if femb_id == 1:
                link_mask = link_mask&0xff0f
            if femb_id == 2:
                link_mask = link_mask&0xf0ff
            if femb_id == 3:
                link_mask = link_mask&0x0fff
            llc.wib_poke(self.wib, 0xA00C0008, link_mask)
            #self.femb_cd_sync()
            if self.i2cerror:
                print ("Reconfigure due to i2c error!")
                self.i2cerror = False
                refi += 1
                if refi > 5:
                    print ("I2C failed! exit anyway")
                    exit()
            else:
                print (f"FEMB{femb_id} is configurated")
                break

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
        #ONlY one channel of a FEMB can set smn to 1 at a time
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

    def wib_adc_mon(self, femb_ids, sps=10  ): 
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        #step 1
        #reset all FEMBs on WIB
        self.femb_cd_rst()
        
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

    def wib_adc_mon_chip(self, femb_ids, mon_chip=0, sps=10): 
        self.wib_mon_switches(dac0_sel=1,dac1_sel=1,dac2_sel=1,dac3_sel=1, mon_vs_pulse_sel=0, inj_cal_pulse=0) 
        #reset all FEMBs on WIB
        self.femb_cd_rst()
        
        mon_dict = {}
        mons = ["VBGR", "VCMI", "VCMO", "VREFP", "VREFN", "VSSA"]
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


    def wib_acquire_rawdata(self, fembs,  num_samples=1, ignore_failure=False,trigger_command=0,trigger_rec_ticks=0,trigger_timeout_ms=0): 
        print (f"Data collection for FEMB {fembs}")
        data = []
        #when buf0 is True, there must be FEMB0 or 1 presented
        #when buf1 is True, there must be FEMB2 or 3 presented
        buf0 = True if 0 in fembs or 1 in fembs else False
        buf1 = True if 2 in fembs or 3 in fembs else False 
        if (buf0 == False) and (buf1 == False):
            print("Select which FEMBs you want to read out first!")
            exit()
        if trigger_command != 0:
            print ("Error! Please use fuction wib_acq_raw_extrig instead, exit anyway!")
            exit()
        for  i in range(num_samples):
            rawdata = self.wib.acquire_rawdata(buf0, buf1, ignore_failure,trigger_command,trigger_rec_ticks,trigger_timeout_ms)
            data.append(rawdata)
        return data
   
    def wib_acq_raw_extrig(self, wibips, fembs,  num_samples=1, ignore_failure=False, trigger_command=0x08, trigger_rec_ticks=0x3f000, trigger_timeout_ms=0): 
        print (f"Data collection for FEMB {fembs} with trigger operations")

        data = []
        buf0 = True if 0 in fembs or 1 in fembs else False
        buf1 = True if 2 in fembs or 3 in fembs else False 
        if (buf0 == False) or (buf1 == False):
            print("Error: currently only support 4 FEMBs per WIB")
            exit()
        for  i in range(num_samples):
            if trigger_command == 0:

                data_ip = []
                for ip in wibips:
                    wib_ip = ip
                    self.wib = WIB(ip)

                    #now = datetime.now()
                    #init_ts = int(datetime.timestamp(now) * 1e9)
                    init_ts = time.time_ns()
                    init_ts = init_ts//16 #WIB system clock is 62.5MHz

                    llc.wib_poke(self.wib, 0xA00C0018, init_ts&0xffffffff)
                    llc.wib_poke(self.wib, 0xA00C001c, (init_ts>>32)&0xffffffff)
                    rdreg = llc.wib_peek(self.wib, 0xA00C000C)
                    wrreg = rdreg&0xfffffffd
                    llc.wib_poke(self.wib, 0xA00C000C, wrreg) #disable fake timestamp
                    wrreg = rdreg|0x02
                    llc.wib_poke(self.wib, 0xA00C000C, wrreg) #enable fake timestamp and reload the init value

                    llc.wib_poke(self.wib, 0xA00C0024, trigger_rec_ticks) #spy rec time
                    rdreg = llc.wib_peek(self.wib, 0xA00C0004)
                    wrreg = (rdreg&0xffffff3f)|0xC0
                    llc.wib_poke(self.wib, 0xA00C0004, wrreg) #reset spy buffer
                    wrreg = (rdreg&0xffffff3f)|0x00
                    llc.wib_poke(self.wib, 0xA00C0004, wrreg) #reset spy buffer
                    time.sleep(0.01)
                    wrreg = (rdreg&0xffffff3f)|0xC0
                    llc.wib_poke(self.wib, 0xA00C0004, wrreg) #reset spy buffer
                    rawdata = self.wib.acquire_rawdata(buf0, buf1, ignore_failure,trigger_command,trigger_rec_ticks,trigger_timeout_ms)
                    data_ip.append((ip, rawdata, 0x00000000, trigger_rec_ticks, trigger_command))
            else:
                for ip in wibips:
                    self.wib = WIB(ip)

                    rdreg = llc.wib_peek(self.wib, 0xA00C0004)
                    wrreg = (rdreg&0xffffff3f)|0xC0
                    llc.wib_poke(self.wib, 0xA00C0004, wrreg) #reset spy buffer
                    wrreg = (rdreg&0xffffff3f)|0x00
                    llc.wib_poke(self.wib, 0xA00C0004, wrreg) #reset spy buffer
                    
                    llc.wib_poke(self.wib, 0xA00C0024, trigger_rec_ticks) #spy rec time
                    rdreg = llc.wib_peek(self.wib, 0xA00C0014)
                    wrreg = (rdreg&0xff00ffff)|(trigger_command<<16)
                    llc.wib_poke(self.wib, 0xA00C0014, wrreg) #program cmd_code_trigger

                while True:
                    spy_full_flgs = False
                    data_ip = []
                    for ip in wibips:
                        wib_ip = ip
                        self.wib = WIB(ip)
                        rdreg = llc.wib_peek(self.wib, 0xA00C0080)
                        if rdreg&0x03 == 0x03:
                            spy_full_flgs = True
                            buf0_end_addr = llc.wib_peek(self.wib, 0xA00C0094)
                            buf1_end_addr = llc.wib_peek(self.wib, 0xA00C0098)
                            if buf0_end_addr == buf1_end_addr:
                                spy_full_flgs = True
                            else:
                                spy_full_flgs = False
                            rawdata = self.wib.acquire_rawdata(buf0, buf1, ignore_failure,trigger_command)
                            data_ip.append((ip, rawdata, buf0_end_addr, trigger_rec_ticks, trigger_command))
                            #print (ip, len(rawdata), len(rawdata[0]))
                        else:
                            spy_full_flgs = False
                            wib_ip = ip
                            break
                    if spy_full_flgs:
                        print ("All WIBs got external trigger for spy buffer")
                        break
                    else:
                        print ("No external trigger received, Wait a second with WIB IP %s"%wib_ip)
                        time.sleep(1)

            data.append(data_ip)
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
