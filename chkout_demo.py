
import low_level_commands as llc
from wib_cfgs import WIB_CFGS
import time
import sys


chk = WIB_CFGS()

#check if WIB is in position
chk.wib_init()

#import chkout_util as chkout
#fembs=[0]
#chkout.power_fembs(chk.wib, fembs, cold=False, seq=0)
#
#set FEMB voltages
chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
print ("BBB", hex(llc.wib_peek(chk.wib, 0xA00c0004)), hex(llc.wib_peek(chk.wib, 0xA00c0008)), hex(llc.wib_peek(chk.wib, 0xA00c000C)))

#turn on 4 FEMBs
femb0=True
femb1=True
femb2=False
femb3=False
fembs=[]
if femb0:
    fembs.append(0)
if femb1:
    fembs.append(1)
if femb2:
    fembs.append(2)
if femb3:
    fembs.append(3)
    
#chk.femb_powering(femb0=True, femb1=True, femb2=True, femb3=True)
chk.femb_powering(femb0=femb0, femb1=femb1, femb2=femb2, femb3=femb3)
print ("BBB", hex(llc.wib_peek(chk.wib, 0xA00c0004)), hex(llc.wib_peek(chk.wib, 0xA00c0008)), hex(llc.wib_peek(chk.wib, 0xA00c000C)))
#llc.wib_poke(chk.wib, 0xA00c0008, 0x0000FFF0)
#sys.stdout.flush() 
#measure power rails
#import chkout_util as chkout
#chkout.power_fembs(chk.wib, fembs, seq=0)
#pwr_meas = chk.get_sensors()

#Configuration
#step 1
#Configur Coldata, ColdADC, and LArASIC parameters. 
#Here Coldata, ColdADC use default setting in the script (not the ASIC default register values)
#Take LArASIC register configuration for example
chk.set_fe_board(sts=1, snc=1, st0=1, st1=1, swdac=1, dac=0x20 )
adac_pls_en = 1 #enable LArASIC interal calibraiton pulser

#step 2
#chk.cfg_a_wib(adac_pls_en)
chk.femb_cfg(femb_id=0)
print ("BBB", hex(llc.wib_peek(chk.wib, 0xA00c0004)), hex(llc.wib_peek(chk.wib, 0xA00c0008)), hex(llc.wib_peek(chk.wib, 0xA00c000C)))
#chk.femb_cfg(femb_id=0)
#chk.femb_cfg(femb_id=1)
#chk.femb_cfg(femb_id=2)
#chk.femb_cfg(femb_id=3)
time.sleep(0.5)

N = 1 #take a spy data
rawdata = chk.wib_acquire_data(num_samples=N) #returns list of size 1

#import chkout_util as chkout
#pulse_num_samples = 1
##print (chk.wib)
##print (fembs)
#timestamps, pulse_samples = chkout.acquire_data(chk.wib, fembs, num_samples=pulse_num_samples)
##exit()
##data collection 
#print (chk.wib)
#print ("BBB", hex(llc.wib_peek(chk.wib, 0xA00c0004)), hex(llc.wib_peek(chk.wib, 0xA00c0008)), hex(llc.wib_peek(chk.wib, 0xA00c000C)))
#
#timestamps = rawdata[0][0]
#samples = rawdata[0][1]
#
#print (timestamps)
#print (type(timestamps), type(samples))
#print (len(timestamps[0]), len(timestamps[1]))
#print ( len(samples[0]))
#print ( type(samples[0]))
#print ( len(samples[0][0]))

#making plots
#rms_samples = rms_samples[0]    

#a = WIB_CFGS()
#a.wib_init()
##a.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
####a.femb_powering(femb0=False, femb1=False)
###a.femb_powering(femb0=True, femb1=False)
###a.femb_powering(femb0=True)
###time.sleep(2)
###a.femb_powering(femb0=True, femb1=True, femb2=True)
###a.femb_powering(femb0=True, femb1=True, femb2=True, femb3=True)
###a.femb_powering(femb0=True, femb1=True, femb2=True, femb3=True)
##a.femb_powering(femb0=True)
##time.sleep(2)
###a.get_sensors()
###a.femb_cd_cfg(femb_id=0)
##print ("XXXXXXX")
##a.femb_cfg()
#a.femb_cd_cfg(femb_id=0)
#a.femb_adc_cfg(femb_id=0)
#a.set_fe_board(sts=1,snc=1,swdac=1, dac=0x20)
#a.femb_fe_cfg(femb_id=0)
#a.femb_adac_cali(femb_id=0)
#print (a.adac_cali_quo)
#time.sleep(10)
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#print (a.adac_cali_quo)
##a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#
#time.sleep(10)
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#print (a.adac_cali_quo)
#time.sleep(10)
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")

#fembs = [0]
#timestamps, rms_samples = llc.acquire_data(a.wib, fembs, num_samples=1) #returns list of size 1
#timestamps, rms_samples = llc.acquire_data(a.wib, fembs, num_samples=1) #returns list of size 1
#timestamps, rms_samples = llc.acquire_data(a.wib, fembs, num_samples=1) #returns list of size 1
#timestamps, rms_samples = llc.acquire_data(a.wib, fembs, num_samples=1) #returns list of size 1
#rms_samples = rms_samples[0]    
#rms_means = []
#rms_stds = []
#import chkout_util as chkout
#for femb in fembs:
#    rms_means_femb, rms_stds_femb, rms_amps_femb = chkout.plot_rms_analysis(rms_samples[femb])
#    rms_means.append(rms_means_femb)
#    rms_stds.append(rms_stds_femb)
#    #print (rms_means_femb)
#    #print (rms_amps_femb)
#    print (int(rms_means_femb[0]), int(rms_amps_femb[0]))

#a.femb_adac_cali(femb_id=0)
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#print (a.regs_int8)
#print ("AAAAAAAAAAA")
#time.sleep(5)
#a.set_fe_reset()
#a.set_fe_board(sts=1,snc=0,swdac=1, dac=0x20)
#a.femb_fe_cfg(femb_id=0)
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#a.femb_cd_fc_act(femb_id=0, act_cmd="larasic_pls")
#a.femb_fe_cfg(femb_id=0)
##a.femb_adac_cali(femb_id=0)

#llc.get_sensors(a.wib)
#llc.cdpeek(a.wib, femb_id = 0, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 1, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 2, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 3, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#print ("XXXXXXX")
#llc.cdpoke(a.wib, femb_id = 1, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89, data = 0x08)
#llc.cdpeek(a.wib, femb_id = 1, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpoke(a.wib, femb_id = 2, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89, data = 0x08)
#llc.cdpeek(a.wib, femb_id = 2, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#a.femb_adc_cfg(femb_id=2)
#print ("XXXXXXX")
#llc.cdpeek(a.wib, femb_id = 0, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 1, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 2, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)
#llc.cdpeek(a.wib, femb_id = 3, chip_addr = 0x04, reg_page = 1, reg_addr = 0x89)




#if __name__ == "__main__":   
#    #parse cmd line args
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
#    wib = 
#    wib = chkout.test_connection(wib)
#    if wib==1: #Connection failed
#        sys.exit() 
#    chkout.system_clock_select(wib, pll=True)    
#    time.sleep(0.1)
############################WIB initialization ends##########################################
#   
#
############################Powering begins##########################################
#    #configure power
#    chkout.power_config(wib, v1=3.0, v2=2.8, v3=3.5)    
#    time.sleep(0.1)
#    
#    #power off fembs
#    chkout.power_fembs(wib, [], seq=0)
#    time.sleep(0.1)  
#
#    chkout.get_sensors(wib)    
#    
#    #power on fembs
#    chkout.power_fembs(wib, fembs, seq=0)
#    time.sleep(0.1)
#    
#    chkout.get_sensors(wib)
#
#    print ("debug")
#    #cmd = bytearray("i2c pwr 0x22 0xc 0\n", 'utf-8')
#    #cmd.extend("i2c pwr 0x22 0xd 0\ni2c pwr 0x22 0xe 0\n".encode())
#    with open(".\scripts\coldata_power_off",'rb') as fin:
#        script = fin.read()
#    chkout.wib_script(wib, script )
#    print ("debug")
#    time.sleep(3)
#    with open(".\scripts\coldata_power_on",'rb') as fin:
#        script = fin.read()
#    chkout.wib_script(wib, script )
#
#    exit()
############################Powering ends##########################################
#
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
#    for i in range(2):    
#        chkout.configure_fembs(wib, fembs, pulse=False)
#        time.sleep(0.1)
#    
#    N = 1
#    timestamps, rms_samples = chkout.acquire_data(wib, fembs, num_samples=N)
#    filename = "test_rms.hdf5"
#    if save:
#        chkout.save_data(rms_samples, filename)
#    
#    rms_samples = rms_samples[0]    
#    rms_means = []
#    rms_stds = []
#    for femb in fembs:
#        rmsplot_filename = "test_rms_femb%d.png"%(femb) if save else None        
#        rms_means_femb, rms_stds_femb = chkout.plot_rms_analysis(rms_samples[femb], filename=rmsplot_filename)
#        rms_means.append(rms_means_femb)
#        rms_stds.append(rms_stds_femb)
#    
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
#    exit()
#    #configure FEMBs for pulse analysis
#    for i in range(2):  
#        chkout.configure_fembs(wib, fembs, pulse=True)
#        time.sleep(0.1)
#    
#    #take and save data to hdf5 file 100 (or however many) times
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
