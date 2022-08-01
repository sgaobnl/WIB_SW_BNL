import zmq
import json
import numpy as np
import platform
import wib_pb2 as wibpb

import sys
import time, datetime, random, statistics
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
import numpy as np
import h5py
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
    return rep.success
    
def system_clock_select(wib, pll=False): #select correct timing source with peek/poke
    #See WIB_firmware.docx table 4.9.1 ts_clk_sel
    # 0[pll=False]  = CDR recovered clock(default)
    # 1[pll=True]   = PLL clock synchronized with CDR or running independently if CDR clock is 
    # missing. PLL clock should only be used on test stand when timing master 
    # is not available.            
    reg_read = wib_peek(wib, 0xA00C0004)
    val = reg_read | (int(pll) << 16)
    wib_poke(wib, 0xA00C0004, val)    
    return wib_peek(wib, 0xA00C0004)
    
def power_fembs(wib, fembs, cold=False, seq=0): 
    ##ref: wib_buttons1.py: power_on
    req = wibpb.PowerWIB()
    req.femb0 = 0 in fembs
    req.femb1 = 1 in fembs
    req.femb2 = 2 in fembs
    req.femb3 = 3 in fembs
    req.cold = cold
    req.stage = seq
    rep = wibpb.Status()
    if (req.stage == 0):
        print("Powering on WIB with full power sequence...")
    elif (req.stage == 1):
        print("Powering on WIB, leaving VDDD and VDDA off, "
                              "COLDATA needing reset, will wait for a global ACT signal")
    elif (req.stage == 2):
        print("Resuming power ON after external COLDADC reset and synchronization")
    else:
        print("Error: Somehow an impossible choice was made in the power stage box")
        return 0
 #   sys.stdout.flush() 
    if not wib.send_command(req,rep,print_gui=print):
        print(rep.extra.decode('ascii'))
        print(f"Successful:{rep.success}")
    return rep.success
    
def get_sensors(wib): #request and print sensor data
    ##ref: wib_mon.py: WibMon.get_sensors, IVSensor.load_data
    print("Requesting sensor data")
    req = wibpb.GetSensors()
    rep = wibpb.GetSensors.Sensors()    
    if not wib.send_command(req,rep,print_gui=print): #if success  
        print("Successfully sent command")
        for idx in range(4):
            print('\n#####FEMB %d####'%idx)
            
            # print('\nLDO A0')
            # before, after = rep.femb_ldo_a0_ltc2991_voltages[idx*2:(idx+1)*2]
            # print_VI(before, after)
            
            # print('\nLDO A1')
            # before, after = rep.femb_ldo_a1_ltc2991_voltages[idx*2:(idx+1)*2]
            # print_VI(before, after)
            power_consumption = 0
            
            print('\n5V Bias')
            before, after = rep.femb_bias_ltc2991_voltages[idx*2:(idx+1)*2]
            print('Vset: 5V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            print('%0.3f V'%before)
            print('%0.3f A'%current)
            print('%0.3f W'%power)
            
            print('\nDC/DC V1 = PWR_LArASIC')
            before, after = dc2dc(rep,idx)[0:2]
            print('Vset: 3V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            print('%0.3f V'%before)
            print('%0.3f A'%current)
            print('%0.3f W'%power)
            
            print('\nDC/DC V2 = PWR_COLDATA')
            before, after = dc2dc(rep,idx)[2:4]
            print('Vset: 3.5V')
            sense_ohms=0.1
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            print('%0.3f V'%before)
            print('%0.3f A'%current)
            print('%0.3f W'%power)
            
            print('\nDC/DC V3 = PWR_ColdADC')
            before, after = dc2dc(rep,idx)[4:6]
            print('Vset: 2.8V')
            sense_ohms=0.01
            current = (before-after)/sense_ohms #A
            power = before * current
            power_consumption = power_consumption + power
            print('%0.3f V'%before)
            print('%0.3f A'%current)
            print('%0.3f W'%power)
            
            print('Power Consumption (including cable dissipation) = %0.3f W\n'%power_consumption)
    
def configure_fembs(wib, fembs, pulse): #configure FEMBs for RMS data
    #add other arguments
    ##ref: wib_buttons4.py: sendFEMB
    
    print("Configuring FEMBs")
    req = wibpb.ConfigureWIB() #see wib.proto for meanings    
#    input ("DDDDDDDDDDDDDDDDDDDDDDD")
    req.pulser = pulse
    req.cold = False
    req.adc_test_pattern = False
    
    for i in range(4):
        femb_conf = req.fembs.add();
        femb_conf.enabled = True if i in fembs else False
        femb_conf.test_cap = True if i in fembs else False    
        femb_conf.gain = 0 #14mv/fc
        femb_conf.peak_time = 3
        femb_conf.baseline = 0
        femb_conf.pulse_dac = 20 if pulse else 0
        femb_conf.leak = 0
        femb_conf.leak_10x = False
        femb_conf.ac_couple = False
        femb_conf.buffer = 0
        femb_conf.strobe_skip = 0x30
        femb_conf.strobe_delay = 0x00
        femb_conf.strobe_length =0x38 
        
    print('Sending ConfigureWIB command')
    rep = wibpb.Status()
    wib.send_command(req,rep,print_gui=print);
    print(rep.extra.decode('ascii'))
    print('Successful: ',rep.success)    
    return rep.success
    
def acquire_data(wib, fembs, num_samples=1): #take rms or pulse data
    ##ref: wib_scope.py: WibScope.acquire_data, SignalView.load_data
    buf0 = True if 0 in fembs or 1 in fembs else False
    buf1 = True if 2 in fembs or 3 in fembs else False 
    if (buf0 == False) and (buf1 == False):
        print("Select which FEMBs you want to read out first!")
        return    
    timestamps_all = []
    samples_all = []
    print (buf0, buf1, fembs)
    for i in range(num_samples):
        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, ignore_failure=True, print_gui = print)
        timestamps_all.append(timestamps)
        samples_all.append(samples)
    return timestamps_all,samples_all
    
def save_data(samples, filename): #save data to hdf5 file
    timestamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    with h5py.File(filename, "a") as f:
#        print("Saving data with dimensions "+str(np.shape(samples)))
        for i in range(len(samples)):
            samples_inst = samples[i]                                          
            dset = f.create_dataset('samp'+str(i)+"_"+timestamp, np.shape(samples_inst), dtype='u2', chunks=True)
            dset[::] = samples_inst
            #Note: This saves "data" from all 4 FEMBs regardless of whether they are on or not. FEMBs that are
            #not on/enabled correctly will have all 0s as data. They are still included in the data because 
            #there is nothing else identifying which FEMB the data came from other than their order within
            #the dataset. If we end up testing often with less than 4 FEMBs, some labeling solution will need 
            #to be devised or the samples can be split up by FEMB before putting into datasets.
    return f
    
def plot_rms_analysis(femb_samples, filename=None): #Plot rms_std
    rms_means = []
    rms_amps = []
    rms_stds = [] 
    for adc in range(8):
        for ch in range(16):        
            ch_samples = femb_samples[adc*16+ch]
            rms_mean = np.mean(ch_samples)
            rms_amp = np.max(ch_samples) - rms_mean
            rms_std = np.std(ch_samples)
            rms_means.append(rms_mean)
            rms_amps.append(rms_amp)
            rms_stds.append(rms_std)            
    fig, ax = plt.subplots()
    ax.plot(rms_stds, marker='.')
    ax.set(xlabel='Channel number', ylabel='ADC counts', title='FEMB RMS noise (1 standard deviation)')  
    plt.grid() 
    if filename is not None:
        fig.savefig(filename)
    else:
#        plt.show()
        pass
    plt.close()      
    return rms_means, rms_stds, rms_amps
    
def pulse_analysis(ch_samples, ch_mean): #loook for valid pulses in samples (one peak followed by one trough)
    samples_valid = []
    peak_loc = []
    trough_loc = []   
    peak_thresh = ch_mean + 2000
    trough_thresh = ch_mean - 2000
    buffer_outside_pulse = 50
    i=0
    for sample in ch_samples:            
        peaks, _ = find_peaks(sample, height=peak_thresh)
        troughs, _ = find_peaks(-1*sample, height=-1*trough_thresh) 
        #print("sample %d: %d peaks, %d troughs"%(i,len(peaks),len(troughs)))        
        if (len(peaks) == 1 and len(troughs) == 1) and (peaks[0] < troughs[0]):
            #print("Ch Sample peak loc %d, trough loc %d"%(peaks[0], troughs[0]))
            if peaks[0] >= buffer_outside_pulse and (len(sample) - troughs[0]) >= buffer_outside_pulse:                                            
                peak_loc.append(peaks[0])
                trough_loc.append(troughs[0])
                samples_valid.append(sample)  
        i=i+1
    
    return samples_valid, peak_loc, trough_loc
    
def overlay_pulses(samples_valid, peak_loc, trough_loc): 
    buffer_outside_pulse = 50    
    peak_trough_dist = [a - b for a, b in zip(trough_loc, peak_loc)]
    peak_trough_dist = int(max(peak_trough_dist))
    ch_slice_sum = [0] * (peak_trough_dist+2*buffer_outside_pulse)   
    pulse_slices = []
    
    for j in range(len(samples_valid)):
        sample = samples_valid[j]
        pulse_slice = sample[(peak_loc[j] - buffer_outside_pulse):(peak_loc[j]+peak_trough_dist+buffer_outside_pulse)]
        ch_slice_sum = [a + b for a, b in zip(ch_slice_sum, pulse_slice)]
        pulse_slices.append(pulse_slice)        
    return pulse_slices
        
def plot_averaged_channels(filename, pulse_slices_all): #average the overlays together & plot them
    ch_pulses_averaged = []
    for pulse_slices in pulse_slices_all:  
        slice_len = len(pulse_slices[0])
        ch_slice_sum = [0] * slice_len
        for pulse_slice in pulse_slices:
            ch_slice_sum = [a + b for a, b in zip(ch_slice_sum, pulse_slice)]    
        ch_slice_avgd = [a / len(pulse_slices) for a in ch_slice_sum]
        ch_pulses_averaged.append(ch_slice_avgd)
    
    fig, ax = plt.subplots()
    
    for ch in ch_pulses_averaged:
        x = [a * 0.5 for a in list(range(len(ch)))]
        ax.plot(x, ch)    
    chs_valid = len(pulse_slices_all)
    ax.set(xlabel='Time (us)', ylabel='ADC counts',
    title='FEMB: Averaged Waveform Overlap of %d channels'%(chs_valid))
    plt.grid() 
    
    if filename is not None:
        fig.savefig(filename)
    else:
        plt.show()
    plt.close()      
    return ch_pulses_averaged

def plot_channel_sample(filename, pulse_slices_all, index): #Overlay a single sample from each channel
    ch_pulses_singlesamp = []
    for pulse_slices in pulse_slices_all: 
        index_temp = index
        if len(pulse_slices) <= index:
            index_temp = len(pulse_slices) - 1
        single_slice = pulse_slices[index_temp]
        ch_pulses_singlesamp.append(single_slice)
    fig, ax = plt.subplots()    
    
    for ch in ch_pulses_singlesamp:
        x = [a * 0.5 for a in list(range(len(ch)))]
        ax.plot(x, ch)    
    chs_valid = len(pulse_slices_all)
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    ax.set(xlabel='Time (us)', ylabel='ADC counts',
    title="FEMB: Waveform Overlap of %d channels' %s or last valid sample"%(chs_valid, ordinal(index)))
    plt.grid() 
    
    if filename is not None:
        fig.savefig(filename)
    else:
        plt.show()
    plt.close()         
    

def plot_stats(filename, valid_channel_numbers, ch_pulses_averaged): #Plot stats for averaged channel
    ch_avg_peaks = []
    ch_pedestal_means = []
    ch_avg_troughs = []
    for ch_avg in ch_pulses_averaged:                        
        ch_avg_peaks.append(np.max(ch_avg))
        ch_pedestal_means.append(np.mean(ch_avg[0:25]))
        ch_avg_troughs.append(np.min(ch_avg))     
    fig, ax = plt.subplots()
    ax.plot(valid_channel_numbers, ch_avg_peaks, 'r.', label='Positive Peak', ls='None')
    ax.plot(valid_channel_numbers, ch_pedestal_means, 'g.', label='Pedestal', ls='None')        
    ax.plot(valid_channel_numbers, ch_avg_troughs, 'b.', label='Negative Peak', ls='None')
    ax.set(xlabel='Channel number', ylabel='ADC counts', title='FEMB: Averaged channel stats')  
    plt.grid()        
    ax.legend(loc='upper right', bbox_to_anchor=(0.35, 0.35))   
    
    if filename is not None:
        fig.savefig(filename)
    else:
        plt.show()
    plt.close()      
    
##miscellaneous utility functions:
    
def wib_peek(wib, reg):
    req = wibpb.Peek()
    rep = wibpb.RegValue()
    req.addr = reg
    if not wib.send_command(req,rep,print_gui=print):
        print(f"Register 0x{rep.addr:016X} was read as 0x{rep.value:08X}")
    return rep.value
    
def wib_poke(wib, reg, val):
    req = wibpb.Poke()
    rep = wibpb.RegValue()
    req.addr = reg
    req.value = val
    if not wib.send_command(req,rep,print_gui=print):
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
        
def print_and_clear_glog(wib):
    req = wibpb.LogControl()
    req.return_log = True
    req.boot_log = False
    req.clear_log = False       
    print("Getting Log...")    
    rep = wibpb.LogControl.Log()
    if not wib.send_command(req,rep,print_gui=print):
        print(rep.contents.decode('utf8'))        
        
    req = wibpb.LogControl()
    req.return_log = False
    req.boot_log = False
    req.clear_log = True
    print("Clearing Log...") 
    rep = wibpb.LogControl.Log()
    if not wib.send_command(req,rep,print_gui=print):
        print(rep.contents.decode('utf8'))   

def display_single_sample(chsample, filename=None):
    rms_mean_temp = np.mean(chsample)
    
    peak_thresh = rms_mean_temp + 2000
    trough_thresh = rms_mean_temp - 2000
    peaks, _ = find_peaks(chsample, height=peak_thresh)
    troughs, _ = find_peaks(-1*chsample, height=-1*trough_thresh)                    
    
    fig, ax = plt.subplots()
    ax.plot(chsample)
    ax.plot(peaks, chsample[peaks], 'x')
    ax.plot(troughs, chsample[troughs], 'x')                
    ax.set(xlabel='Sample index', ylabel='ADC counts',
    title='Single sample')
    
    if filename is not None:
        fig.savefig(filename)
    else:
        plt.show()
    plt.close()   
    
def fast_command(wib, cmd): #use: fast_command(wib,'reset')
    #ref: wib_buttons6.py: WIBFast.fast_command    
    fast_cmds = { 'reset':1, 'act':2, 'sync':4, 'edge':8, 'idle':16, 'edge_act':32 }
    req = wibpb.CDFastCmd()
    req.cmd = fast_cmds[cmd]
    rep = wibpb.Empty()
    wib.send_command(req,rep,print_gui=print)
    print(f"Fast command {req.cmd} sent")    

def cdpeek(wib,femb_id, chip_addr, reg_page, reg_addr):
    req = wibpb.CDPeek()
    rep = wibpb.CDRegValue()
    req.femb_idx = femb_id #0, 1, 2, 3
    req.coldata_idx = 0 
    req.chip_addr = chip_addr #CD3 ADC89AB, CD2 ADC4567
    req.reg_page = reg_page
    req.reg_addr = reg_addr
    wib.send_command(req,rep)
    print('femb:%i coldata:%i chip:0x%02X page:0x%02X reg:0x%02X -> 0x%02X'%(rep.femb_idx,rep.coldata_idx,rep.chip_addr,rep.reg_page,rep.reg_addr,rep.data))
    return rep.data

def cdpoke(wib,femb_id, cd_id, chip_addr, reg_page, reg_addr, data):
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
    print('femb:%i coldata:%i chip:0x%02X page:0x%02X reg:0x%02X <- 0x%02X'%(rep.femb_idx,rep.coldata_idx,rep.chip_addr,rep.reg_page,rep.reg_addr,rep.data))

def wib_script(wib,script):
    req = wibpb.Script()
    req.script = bytes(script)
    rep = wibpb.Status()
    wib.send_command(req,rep)
    print('Successful:',rep.success)


