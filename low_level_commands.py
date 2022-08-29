import zmq
import json
import numpy as np
import platform
import wib_pb2 as wibpb

import sys
import time, datetime, random, statistics
import numpy as np
#from fpdf import FPDF

def test_connection(wib, tries=10): 
    ##ref: wib_buttons2.py: sw_status 
    req = wibpb.GetSWVersion()
    rep = wibpb.GetSWVersion.Version()    
    for i in range(tries):
        if not wib.send_command(req,rep,print_gui=print):
            print(f"Software Version: {rep.version}")  
            return wib
        else:
            del wib
            wib = WIB("192.168.121.1")
        time.sleep(0.5)
    print("Failed")
    return 1
    
def system_clock_select(wib, pll=False, fp1_ptc0_sel=0, cmd_stamp_sync = 0x7fff): #select correct timing source with peek/poke
    #See WIB_firmware.docx table 4.9.1 ts_clk_sel
    # 0[pll=False]  = CDR recovered clock(default)
    # 1[pll=True]   = PLL clock synchronized with CDR or running independently if CDR clock is 
    # missing. PLL clock should only be used on test stand when timing master 
    # is not available.            
    reg_read = wib_peek(wib, 0xA00C0004)
    val = (reg_read&0xFFFEFFFF) | (int(pll) << 16)
    wib_poke(wib, 0xA00C0004, val)    
    if pll == True:
        print ("PLL clock synchronized with CDR or running independently if CDR clock is missing")
        print ("PLL clock should only be used on test stand when timing master is not available.")
        print ("Enable fake timing system")
        rdreg = wib_peek(wib, 0xA00c000C)
        #disable fake time stamp
        wib_poke(wib, 0xA00c000C, (rdreg&0xFFFFFFF1))
        #set the init time stamp
        wib_poke(wib, 0xA00c0018, 0x00000000)
        wib_poke(wib, 0xA00c001C, 0x00000000)
        #enable fake time stamp
        wib_poke(wib, 0xA00c000C, (rdreg|0x0e))
    else:
        rdreg = wib_peek(wib, 0xA00c0004)
        if fp1_ptc0_sel == 0:
            print ("timing master is available through backplane (PTC)")
            wib_poke(wib, 0xA00c0004, (rdreg&0xFFFFFFDF)) #backplane
        else:
            print ("timing master is available through front_panel")
            wib_poke(wib, 0xA00c0004, (rdreg&0xFFFFFFFF)|0x20) #front_panel
        time.sleep(1)
        rdreg = wib_peek(wib, 0xA00c0090)
        print ("External timing is selected")

        rdreg = wib_peek(wib, 0xA00c000C)
        #disable fake time stamp
        wib_poke(wib, 0xA00c000C, (rdreg&0xFFFFFFF1))
        #set the init time stamp
        #align_en = 1, cmd_stamp_sync_en = 1
        wib_poke(wib, 0xA00c000C, (rdreg|0x0C))
        rdreg = wib_peek(wib, 0xA00c000C)
        #send SYNC_FAST command when cmd_stamp_syn match the DTS time stamp
        wib_poke(wib, 0xA00c000C, (cmd_stamp_sync<<16) + ((rdreg&0x8000FFFF)|0x0C) )
    return wib_peek(wib, 0xA00C0004)

#def config_wib(wib ): 
#    req = wibpb.ConfigureWIB()
#    rep = wibpb.Status()    
#    print (rep)
#    
#    if not wib.send_command(req,rep,print_gui=print):
#        print(f"Success:{rep.success}")
##    sys.stdout.flush() 
#    return rep.success
def power_config(wib, v1=3.0, v2=2.8, v3=3.5, v4=0.0, ldo0=0.0, ldo1=0.0): 
    ##ref: wib_buttons5.py: send_power_config
    req = wibpb.ConfigurePower()
    rep = wibpb.Status()    
    req.dc2dc_o1 = v1
    req.dc2dc_o2 = v2
    req.dc2dc_o3 = v3
    req.dc2dc_o4 = v4
    req.ldo_a0 = ldo0
    req.ldo_a1 = ldo1
    
    if not wib.send_command(req,rep,print_gui=print):
        print(f"Success:{rep.success}")
#    sys.stdout.flush() 
    return rep.success   

def get_sensors(wib): #request and print sensor data
    ##ref: wib_mon.py: WibMon.get_sensors, IVSensor.load_data
    print("Requesting sensor data")
    req = wibpb.GetSensors()
    rep = wibpb.GetSensors.Sensors()    
    if not wib.send_command(req,rep,print_gui=print): #if success  
        print("Successfully sent command")
        pwr_meas = {"femb0":[],"femb1":[],"femb2":[],"femb3":[],}
        for idx in range(4):
            # print('\nLDO A0')
            # before, after = rep.femb_ldo_a0_ltc2991_voltages[idx*2:(idx+1)*2]
            # print_VI(before, after)
            
            # print('\nLDO A1')
            # before, after = rep.femb_ldo_a1_ltc2991_voltages[idx*2:(idx+1)*2]
            # print_VI(before, after)
            power_consumption = 0
            
            #print('\n5V Bias')
            before, after = rep.femb_bias_ltc2991_voltages[idx*2:(idx+1)*2]
            #print('Vset: 5V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            #print('%0.3f V'%before)
            #print('%0.3f A'%current)
            #print('%0.3f W'%power)
            pwr_meas[f"femb{idx}"].append(["Bias5V", before, current, power])
            
            #print('\nDC/DC V1 = PWR_LArASIC')
            before, after = dc2dc(rep,idx)[0:2]
            #print('Vset: 3V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            #print('%0.3f V'%before)
            #print('%0.3f A'%current)
            #print('%0.3f W'%power)
            pwr_meas[f"femb{idx}"].append(["PWR_FE", before, current, power])
            
            #print('\nDC/DC V2 = PWR_COLDATA')
            before, after = dc2dc(rep,idx)[2:4]
            #print('Vset: 3.5V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            #print('%0.3f V'%before)
            #print('%0.3f A'%current)
            #print('%0.3f W'%power)
            pwr_meas[f"femb{idx}"].append(["PWR_CD", before, current, power])
            
            #print('\nDC/DC V3 = PWR_ColdADC')
            before, after = dc2dc(rep,idx)[4:6]
            #print('Vset: 2.8V')
            sense_ohms=0.01
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            #print('%0.3f V'%before)
            #print('%0.3f A'%current)
            #print('%0.3f W'%power)
            pwr_meas[f"femb{idx}"].append(["PWR_ADC", before, current, power])
            
            #print('Power Consumption (including cable dissipation) = %0.3f W\n'%power_consumption)
        #print (pwr_meas)
        return pwr_meas
    
def llc_acquire_data(wib, buf0=True,buf1=True,deframe=True,channels=True,ignore_failure=False,trigger_command=0,trigger_rec_ticks=0,trigger_timeout_ms=0, print_gui=None ): 
    timestamps,samples = wib.acquire_data(buf0,buf1,deframe,channels,ignore_failure,trigger_command,trigger_rec_ticks,trigger_timeout_ms, print_gui)
    return timestamps,samples
   
def wib_peek(wib, reg, print_flg=False):
    req = wibpb.Peek()
    rep = wibpb.RegValue()
    req.addr = reg
    if not wib.send_command(req,rep,print_gui=print):
        if print_flg:
            print(f"Register 0x{rep.addr:016X} was read as 0x{rep.value:08X}")
    return rep.value
    
def wib_poke(wib, reg, val, print_flg=False):
    req = wibpb.Poke()
    rep = wibpb.RegValue()
    req.addr = reg
    req.value = val
    if not wib.send_command(req,rep,print_gui=print):
        if print_flg:
            print(f"Register 0x{rep.addr:016X} was set to 0x{rep.value:08X}") 
        
def dc2dc(s,idx): #for use in get_sensors
    if idx == 0:
        return s.femb0_dc2dc_ltc2991_voltages
    elif idx == 1:
        return s.femb1_dc2dc_ltc2991_voltages
    elif idx == 2:
        return s.femb2_dc2dc_ltc2991_voltages
    elif idx == 3:
        return s.femb3_dc2dc_ltc2991_voltages    
        
#def print_and_clear_glog(wib):
#    req = wibpb.LogControl()
#    req.return_log = True
#    req.boot_log = False
#    req.clear_log = False       
#    print("Getting Log...")    
#    rep = wibpb.LogControl.Log()
#    if not wib.send_command(req,rep,print_gui=print):
#        print(rep.contents.decode('utf8'))        
#        
#    req = wibpb.LogControl()
#    req.return_log = False
#    req.boot_log = False
#    req.clear_log = True
#    print("Clearing Log...") 
#    rep = wibpb.LogControl.Log()
#    if not wib.send_command(req,rep,print_gui=print):
#        print(rep.contents.decode('utf8'))   

def fast_command(wib, cmd, print_flg=False): #use: fast_command(wib,'reset')
    #ref: wib_buttons6.py: WIBFast.fast_command    
    fast_cmds = { 'reset':1, 'act':2, 'sync':4, 'edge':8, 'idle':16, 'edge_act':32 }
    req = wibpb.CDFastCmd()
    req.cmd = fast_cmds[cmd]
    rep = wibpb.Empty()
    wib.send_command(req,rep,print_gui=print)
    if print_flg:
        print(f"Fast command {req.cmd} sent")    
    if "reset" in cmd:
        time.sleep(1)

def cdpeek(wib,femb_id, chip_addr, reg_page, reg_addr, print_flg=False):
    req = wibpb.CDPeek()
    rep = wibpb.CDRegValue()
    req.femb_idx = femb_id #0, 1, 2, 3
    req.coldata_idx = 0 
    req.chip_addr = chip_addr #CD3 ADC89AB, CD2 ADC4567
    req.reg_page = reg_page
    req.reg_addr = reg_addr
    wib.send_command(req,rep)
    if print_flg:
        print('femb:%i coldata:%i chip:0x%02X page:0x%02X reg:0x%02X -> 0x%02X'%(rep.femb_idx,rep.coldata_idx,rep.chip_addr,rep.reg_page,rep.reg_addr,rep.data))
    return rep.data

def cdpoke(wib,femb_id, chip_addr, reg_page, reg_addr, data, print_flg=False):
    req = wibpb.CDPoke()
    rep = wibpb.CDRegValue()
    req.femb_idx = femb_id
    req.coldata_idx = 0
    req.chip_addr = chip_addr
    req.reg_page = reg_page
    req.reg_addr = reg_addr
    wib.send_command(req,rep)
    req.data = data
    wib.send_command(req,rep)
    if print_flg:
        print('femb:%i coldata:%i chip:0x%02X page:0x%02X reg:0x%02X <- 0x%02X'%(rep.femb_idx,rep.coldata_idx,rep.chip_addr,rep.reg_page,rep.reg_addr,rep.data))

def wib_script(wib,script):
    req = wibpb.Script()
    req.script = bytes(script)
    rep = wibpb.Status()
    wib.send_command(req,rep)
    print('Successful:',rep.success)

def spi_read():
    pass 
    #cdpoke(0, 0, 2, 0, 0x20, 8)
    #req = wibpb.CDFastCmd()
    #req.cmd = 2
    #rep = wibpb.Empty()
    #wib.send_command(req,rep)
    #self.coldata_poke(0, 0, 2, 0, 0x20, 3)
    #req = wibpb.CDFastCmd()
    #req.cmd = 2
    #rep = wibpb.Empty()
    #wib.send_command(req,rep)
    #self.coldata_peek(0, 0, 2, 0, 0x24)
        
#def acquire_data(wib, fembs, num_samples=1): #take rms or pulse data
    ##ref: wib_scope.py: WibScope.acquire_data, SignalView.load_data
#when buf0 is True, there must be FEMB0 or 1 presented
#when buf1 is True, there must be FEMB2 or 3 presented
#    buf0 = True if 0 in fembs or 1 in fembs else False
#    buf1 = True if 2 in fembs or 3 in fembs else False 
#    print (buf0, buf1, fembs)
#    if (buf0 == False) and (buf1 == False):
#        print("Select which FEMBs you want to read out first!")
#        exit()
#    data = []
#    for  i in range(num_samples):
#        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, ignore_failure=True, print_gui = print)
#        data.append((timestamps,samples))
#    return data




    


#def acquire_data(wib, fembs, num_samples=1): #take rms or pulse data
#    ##ref: wib_scope.py: WibScope.acquire_data, SignalView.load_data
#    buf0 = True if 0 in fembs or 1 in fembs else False
#    buf1 = True if 2 in fembs or 3 in fembs else False 
#    if (buf0 == False) and (buf1 == False):
#        print("Select which FEMBs you want to read out first!")
#        return    
#    timestamps_all = []
#    samples_all = []
#    for i in range(num_samples):
#        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, ignore_failure=True, print_gui = print)
#        timestamps_all.append(timestamps)
#        samples_all.append(samples)
#    return timestamps_all,samples_all

#def acquire_data(wib, fembs, num_samples=1): #take rms or pulse data
#    ##ref: wib_scope.py: WibScope.acquire_data, SignalView.load_data
#    buf0 = True if 0 in fembs or 1 in fembs else False
#    buf1 = True if 2 in fembs or 3 in fembs else False 
#    if (buf0 == False) and (buf1 == False):
#        print("Select which FEMBs you want to read out first!")
#        return    
#    timestamps_all = []
#    samples_all = []
#    for i in range(num_samples):
#        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, ignore_failure=True, print_gui = print)
#        timestamps_all.append(timestamps)
#        samples_all.append(samples)
#    return timestamps_all,samples_all
    
#def save_data(samples, filename): #save data to hdf5 file
#    timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
#    with h5py.File(filename, "a") as f:
##        print("Saving data with dimensions "+str(np.shape(samples)))
#        for i in range(len(samples)):
#            samples_inst = samples[i]                                          
#            dset = f.create_dataset('samp'+str(i)+"_"+timestamp, np.shape(samples_inst), dtype='u2', chunks=True)
#            dset[::] = samples_inst
#            #Note: This saves "data" from all 4 FEMBs regardless of whether they are on or not. FEMBs that are
#            #not on/enabled correctly will have all 0s as data. They are still included in the data because 
#            #there is nothing else identifying which FEMB the data came from other than their order within
#            #the dataset. If we end up testing often with less than 4 FEMBs, some labeling solution will need 
#            #to be devised or the samples can be split up by FEMB before putting into datasets.
#    return f
#    
##miscellaneous utility functions:
    

