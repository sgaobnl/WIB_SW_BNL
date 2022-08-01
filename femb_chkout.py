import chkout_util as chkout
from wib import WIB

import sys, time, random

if __name__ == "__main__":   
    #parse cmd line args
#    if len(sys.argv) < 2:
#        print('Please specify at least one FEMB # to test')
#        print('Usage: python wib.py 0')
#        exit()    
#
#    if 'save' in sys.argv:
#        save = True
#        sys.argv.remove('save')
#    else:
#        save = False
#
#    fembs = [int(a) for a in sys.argv[1:]] 
#    
#    pulse_num_samples = 100
#
############################WIB initialization begins##########################################
#    #initialize ethernet connection & test connection   
#    print("Experimental command line testing for FEMB checkout test")
    wib = WIB("192.168.121.1")
    wib = chkout.test_connection(wib)
    if wib==1: #Connection failed
        sys.exit() 
    chkout.system_clock_select(wib, pll=True)    
    time.sleep(0.1)
    fembs=[0]
    print ("444", hex(chkout.wib_peek(wib, 0xA00c0004)), hex(chkout.wib_peek(wib, 0xA00c0008)), hex(chkout.wib_peek(wib, 0xA00c000C)))
############################WIB initialization ends##########################################
#   
#
############################Powering begins##########################################
#    #configure power
##    chkout.power_config(wib, v1=3.0, v2=2.8, v3=3.5)    
##    time.sleep(0.1)
#    
##    #power off fembs
##    chkout.power_fembs(wib, [0], seq=0)
##    time.sleep(0.1)  
###
##    chkout.get_sensors(wib)    
#    
##    #power on fembs
#    fembs = [0]
    chkout.power_fembs(wib, fembs, seq=0)
    print ("444", hex(chkout.wib_peek(wib, 0xA00c0004)), hex(chkout.wib_peek(wib, 0xA00c0008)), hex(chkout.wib_peek(wib, 0xA00c000C)))

    time.sleep(0.1)
##    
##    chkout.get_sensors(wib)
##
##    print ("debug")
##    #cmd = bytearray("i2c pwr 0x22 0xc 0\n", 'utf-8')
##    #cmd.extend("i2c pwr 0x22 0xd 0\ni2c pwr 0x22 0xe 0\n".encode())
##    with open(".\scripts\coldata_power_off",'rb') as fin:
##        script = fin.read()
##    chkout.wib_script(wib, script )
##    print ("debug")
##    time.sleep(3)
##    with open(".\scripts\coldata_power_on",'rb') as fin:
##        script = fin.read()
##    chkout.wib_script(wib, script )
##
#############################Powering ends##########################################
##
############################FEMB initilazation begins##########################################
#    #Reset COLDATA
#    #This fixes the problem where some COLDATAs don't toggle the pulse when they're told to
#    chkout.fast_command(wib, 'reset')
#
############################FEMB initilazation ends##########################################
#
#
#
#    
#    #configure FEMBs for RMS noise sampling
#    print (wib)
#    for i in range(2):    
#        chkout.configure_fembs(wib, fembs, pulse=False)
#        time.sleep(0.1)
    
    chkout.configure_fembs(wib, fembs, pulse=False)
    print ("444", hex(chkout.wib_peek(wib, 0xA00c0004)), hex(chkout.wib_peek(wib, 0xA00c0008)), hex(chkout.wib_peek(wib, 0xA00c000C)))
#    chkout.configure_fembs(wib, fembs, pulse=False)

    print (wib)
    fembs=[0]
    N = 1
    timestamps, rms_samples = chkout.acquire_data(wib, fembs, num_samples=N)
    print ("444", hex(chkout.wib_peek(wib, 0xA00c0004)), hex(chkout.wib_peek(wib, 0xA00c0008)), hex(chkout.wib_peek(wib, 0xA00c000C)))
    exit()
    print (wib)
#    filename = "test_rms.hdf5"
#    if save:
#        chkout.save_data(rms_samples, filename)
#    exit()
#    tmp = chkout.peek(wib,0xA00C0014)
   
#    rms_samples = rms_samples[0]    
#    rms_means = []
#    rms_stds = []
#    for femb in fembs:
#        rmsplot_filename = "test_rms_femb%d.png"%(femb) if save else None        
#        rms_means_femb, rms_stds_femb = chkout.plot_rms_analysis(rms_samples[femb], filename=rmsplot_filename)
#        rms_means.append(rms_means_femb)
#        rms_stds.append(rms_stds_femb)
    

#    print ("XXXXXXXXXXXXXXXXXXXXXX")
#    tmp = chkout.cdpeek(wib,0,0,2,1,7)
#    print (tmp)
#    tmp = chkout.cdpeek(wib,0,0,2,1,6)
#    print (tmp)
#    tmp = chkout.cdpeek(wib,0,0,4,1,0x89)
#    print (tmp)
#    tmp = chkout.cdpeek(wib,0,0,3,1,7)
#    print (tmp)
#    tmp = chkout.cdpeek(wib,0,0,3,1,6)
#    print (tmp)
#    tmp = chkout.cdpeek(wib,0,0,0x0A,1,0x98)
#    print (tmp)
#    #configure FEMBs for pulse analysis
#    for i in range(2):  
#        chkout.configure_fembs(wib, fembs, pulse=True)
#        time.sleep(0.1)
#    
    #take and save data to hdf5 file 100 (or however many) times
#    pulse_num_samples = 1
#    timestamps, pulse_samples = chkout.acquire_data(wib, fembs, num_samples=pulse_num_samples)
#    filename = "test_pulse.hdf5"
#    if save:
#        chkout.save_data(pulse_samples, filename, fembs)
#        
#    success = True #success flag
#    for femb in fembs:        
#        single_samp_index = random.randint(0, pulse_num_samples-1)
#        pulse_slices_all = []
#        valid_channel_numbers = []
#        for adc in range(8):
#            for ch in range(16):
#                ch_samples = [a[:][femb][adc*16+ch] for a in pulse_samples]
#                samples_valid, peak_loc, trough_loc = chkout.pulse_analysis(ch_samples,rms_means[femb][adc*16+ch])
#                # print("%d valid samples found for femb %d ch %d"%(len(samples_valid),femb,adc*16+ch))
#                if not samples_valid: #empty list
#                    success = False
#                    print("%d valid samples found for %d:%d"%(len(samples_valid),femb,adc*16+ch))
#                    # #pick random sample to plot
#                    # chsel = random.randint(0, 99)
#                    # chsample = ch_samples[chsel]
#                    # chkout.display_single_sample(chsample)
#                else:
#                    valid_channel_numbers.append(adc*16+ch)
#                    pulse_slices = chkout.overlay_pulses(samples_valid, peak_loc, trough_loc)
#                    pulse_slices_all.append(pulse_slices)
#        #Average channel's samples and plot them overlapped
#        filename = "test_pulse_avgs_femb%d.png"%(femb) if save else None
#        ch_pulses_averaged = chkout.plot_averaged_channels(filename, pulse_slices_all)
#        
#        #Overlay a single random sample from each channel so you can see the 
#        #raw data & noise
#        filename = "test_pulse_single_femb%d.png"%(femb) if save else None
#        chkout.plot_channel_sample(filename, pulse_slices_all, single_samp_index)
#
#        #Plot stats for averaged 
#        filename = "test_pulse_stats_femb%d.png"%(femb) if save else None
#        chkout.plot_stats(filename, valid_channel_numbers, ch_pulses_averaged)
#    print("Success" if success else "Fail")
