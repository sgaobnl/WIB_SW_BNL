import zmq
import json
import numpy as np
import platform
import wib_pb2 as wibpb

#new:
import sys
import time, datetime, random, statistics
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
import numpy as np
import h5py
#from fpdf import FPDF

now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y %H-%M-%S")


class WIB:
    '''Encapsulates python methods for interacting with wib_server running on a WIB'''

    def __init__(self,wib_server='127.0.0.1'):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://%s:1234'%wib_server)

    def send_command(self,req,rep,print_gui=None):
        cmd = wibpb.Command()
        cmd.cmd.Pack(req)
        if (type(req) == type(wibpb.PowerWIB())):
            self.socket.setsockopt(zmq.RCVTIMEO, 60000) # milliseconds
        elif (type(req) == type(wibpb.Script())):
            self.socket.setsockopt(zmq.RCVTIMEO, 15000) # milliseconds
        elif (type(req) == type(wibpb.Calibrate())):
            self.socket.setsockopt(zmq.RCVTIMEO, 20000) # milliseconds
        elif (type(req) == type(wibpb.ResetTiming())):
            self.socket.setsockopt(zmq.RCVTIMEO, 20000) # milliseconds
        else:
            self.socket.setsockopt(zmq.RCVTIMEO, 5000) # milliseconds
        try:
            self.socket.send(cmd.SerializeToString())
        except:
            print("Socket timed out while sending. Please check to make sure the network cable is connected and restart the GUI!")
            return 1
        try:
            rep.ParseFromString(self.socket.recv())
        except:
            print("Socket timed out while receiving. Please check to make sure the network cable is connected and restart the GUI!")
            return 1
        
    def defaults(self):
        req = wibpb.ConfigureWIB()
        #see wib.proto for meanings
        req.pulser = False
        req.cold = False
        req.adc_test_pattern = False
        for i in range(4):
            femb_conf = req.fembs.add();
            femb_conf.enabled = False
            femb_conf.test_cap = False
            femb_conf.gain = 2
            femb_conf.peak_time = 3
            femb_conf.baseline = 0
            femb_conf.pulse_dac = 0
            femb_conf.leak = 0
            femb_conf.leak_10x = False
            femb_conf.ac_couple = False
            femb_conf.buffer = 0
            femb_conf.strobe_skip = 255
            femb_conf.strobe_delay = 255
            femb_conf.strobe_length = 255
        return req
        
    def configure(self,config):
        
        if config is None:
            print('Loading defaults')
            req = self.defaults()
        else:
            print('Loading config')
            try:
                with open(config,'rb') as fin:
                    config = json.load(fin)
            except Exception as e:
                print('Failed to load config:',e)
                return
                
            req = wibpb.ConfigureWIB()
            req.cold = config['cold']
            req.pulser = config['pulser']
            if 'adc_test_pattern' in config:
                req.adc_test_pattern = config['adc_test_pattern']
            if 'frame_dd' in config:
                req.frame_dd = config['frame_dd']
            
            for i in range(4):
                femb_conf = req.fembs.add();
                
                femb_conf.enabled = config['enabled_fembs'][i]
                
                fconfig = config['femb_configs'][i]
                
                #see wib.proto for meanings
                femb_conf.test_cap = fconfig['test_cap']
                femb_conf.gain = fconfig['gain']
                femb_conf.peak_time = fconfig['peak_time']
                femb_conf.baseline = fconfig['baseline']
                femb_conf.pulse_dac = fconfig['pulse_dac']

                femb_conf.leak = fconfig['leak']
                femb_conf.leak_10x = fconfig['leak_10x']
                femb_conf.ac_couple = fconfig['ac_couple']
                femb_conf.buffer = fconfig['buffer']

                femb_conf.strobe_skip = fconfig['strobe_skip']
                femb_conf.strobe_delay = fconfig['strobe_delay']
                femb_conf.strobe_length = fconfig['strobe_length']
        
        print('Sending ConfigureWIB command')
        rep = wibpb.Status()
        self.send_command(req,rep);
        print(rep.extra.decode('ascii'))
        print('Successful: ',rep.success)
        return rep.success
        
#    def acquire_data(self,buf0=True,buf1=True,deframe=True,channels=True,ignore_failure=False,trigger_command=0,trigger_rec_ticks=0,trigger_timeout_ms=0, print_gui=None):
#        print('Reading out WIB spy buffer')
#        req = wibpb.ReadDaqSpy()
#        req.buf0 = buf0
#        req.buf1 = buf1
#        req.deframe = deframe
#        req.channels = channels
#        req.trigger_command = trigger_command
#        req.trigger_rec_ticks = trigger_rec_ticks
#        req.trigger_timeout_ms = trigger_timeout_ms
#        rep = wibpb.ReadDaqSpy.DeframedDaqSpy()
#        self.send_command(req,rep,print_gui=print_gui)
#        print('Successful:',rep.success)
#        if not ignore_failure and not rep.success:
#            return None
#        num = rep.num_samples
#        print('Acquired %i samples'%num)
#        timestamps = np.frombuffer(rep.deframed_timestamps,dtype=np.uint64).reshape((2,num))
#        samples = np.frombuffer(rep.deframed_samples,dtype=np.uint16).reshape((4,128,num))
#        return timestamps,samples

    def acquire_rawdata(self,buf0=True,buf1=True,ignore_failure=False,trigger_command=0,trigger_rec_ticks=0,trigger_timeout_ms=0):
        print('Reading out WIB spy buffer')
        req = wibpb.ReadDaqSpy()
        req.buf0 = buf0
        req.buf1 = buf1
        req.trigger_command = trigger_command
        req.trigger_rec_ticks = trigger_rec_ticks
        req.trigger_timeout_ms = trigger_timeout_ms
        rep = wibpb.ReadDaqSpy.DaqSpy()
        self.send_command(req,rep)
        print('Successful:',rep.success)
        if not ignore_failure and not rep.success:
            return None
        return rep.buf0, rep.buf1
   
    def print_timing_status(self,timing_status):
        print('--- PLL INFO ---')
        print('LOS:         0x%x'%(timing_status.los_val & 0x0f))
        print('OOF:         0x%x'%(timing_status.los_val >> 4))
        print('LOS FLG:     0x%x'%(timing_status.los_flg_val & 0x0f))
        print('OOF FLG:     0x%x'%(timing_status.los_flg_val >> 4))
        print('HOLD:        0x%x'%( (timing_status.los_val >> 5) & 0x1 ))
        print('LOL:         0x%x'%( (timing_status.los_val >> 1) & 0x1 ))
        print('HOLD FLG:    0x%x'%( (timing_status.lol_flg_val >> 5) & 0x1 ))
        print('LOL FLG:     0x%x'%( (timing_status.lol_flg_val >> 1) & 0x1 ))
        print('--- EPT INFO ---')
        print('EPT CDR LOS: 0x%x'%( (timing_status.ept_status >> 17) & 0x1 )) # bit 17 is CDR LOS as seen by endpoint
        print('EPT CDR LOL: 0x%x'%( (timing_status.ept_status >> 16) & 0x1 )) # bit 16 is CDR LOL as seen by endpoint
        print('EPT TS RDY:  0x%x'%( (timing_status.ept_status >> 8 ) & 0x1 )) # bit 8 is ts ready
        print('EPT STATE:   0x%x'%(  timing_status.ept_status & 0x0f )) # bits 3:0 are the endpoint state

#addt'l functions

def dc2dc(s,idx):
    if idx == 0:
        return s.femb0_dc2dc_ltc2991_voltages
    elif idx == 1:
        return s.femb1_dc2dc_ltc2991_voltages
    elif idx == 2:
        return s.femb2_dc2dc_ltc2991_voltages
    elif idx == 3:
        return s.femb3_dc2dc_ltc2991_voltages    

    
def mainfunc():
    
    
    all_channels_good = True
    if len(sys.argv) < 2:
        print('Please specify at least one FEMB # to test')
        print('Usage: python wib.py 0')
        exit()
    
    print("Experimental command line testing for FEMB checkout test")
    wib = WIB("192.168.121.1")
        
    print("Configuring power")
    req = wibpb.ConfigurePower()
    rep = wibpb.Status()
    req.dc2dc_o1 = 3.0 #LArASIC
    req.dc2dc_o2 = 3.5 #COLDATA
    req.dc2dc_o3 = 2.8 #ColdADC
    #req.dc2dc_o4 = self.dc4_box.value()
    #req.ldo_a0 = self.ldo1_box.value()
    #req.ldo_a1 = self.ldo2_box.value()
    
    tries = 5
    for i in range(tries):
        try:
            if not wib.send_command(req,rep,print_gui=print):
                print(f"Success:{rep.success}\n")    
            break
        except Exception as e:
            del wib
            wib = WIB("192.168.121.1")
            

            
    #add register peek & poke
    def wib_peek(reg):
        req = wibpb.Peek()
        rep = wibpb.RegValue()
        req.addr = reg
        if not wib.send_command(req,rep,print_gui=print):
            print(f"Register 0x{rep.addr:016X} was read as 0x{rep.value:08X}")
        return rep.value
        
    def wib_poke(reg, val):
        req = wibpb.Poke()
        rep = wibpb.RegValue()
        req.addr = reg
        req.value = val
        if not wib.send_command(req,rep,print_gui=print):
            print(f"Register 0x{rep.addr:016X} was set to 0x{rep.value:08X}")    
    
    #Selects correct timing source
    reg_read = wib_peek(0xA00C0004)
    val = reg_read | 0x10000
    wib_poke(0xA00C0004, val)
    
    
    # print("Powering off all FEMBs")
    # wib.configure(None)
    # req = wib.defaults()    
    # print('Sending ConfigureWIB command')
    # rep = wibpb.Status()
    # wib.send_command(req,rep,print_gui=print);
    # print(rep.extra.decode('ascii'))
    # print('Successful: ',rep.success)
        
    print("Powering FEMB(s)")
    req = wibpb.PowerWIB()
    
    #use: python wib.py 0 3 1 2
    fembs = [int(a) for a in sys.argv[1:]]    
    req.femb0 = False
    req.femb1 = False
    req.femb2 = False
    req.femb3 = False
    if 0 in fembs:
        req.femb0 = True
    if 1 in fembs:
        req.femb1 = True
    if 2 in fembs:
        req.femb2 = True
    if 3 in fembs:
        req.femb3 = True   
    
    req.cold = False
    req.stage = 0
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
    #sys.stdout.flush()
    if not wib.send_command(req,rep,print_gui=print):
        #print(rep.extra.decode('ascii')) #Uncomment to see debug messages
        print(f"Successful:{rep.success}\n")


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

    print("Configuring FEMBs")
    #wib.configure(None) #assuming this is ok for now
    req = wibpb.ConfigureWIB()
    #see wib.proto for meanings
    req.pulser = False
    req.cold = False
    req.adc_test_pattern = False
    
    for i in range(4):
        femb_conf = req.fembs.add();
        femb_conf.enabled = True if i in fembs else False
        femb_conf.test_cap = True if i in fembs else False    
        femb_conf.gain = 0 #14mv/fc
        femb_conf.peak_time = 3
        femb_conf.baseline = 0
        femb_conf.pulse_dac = 0
        femb_conf.leak = 0
        femb_conf.leak_10x = False
        femb_conf.ac_couple = False
        femb_conf.buffer = 0
        femb_conf.strobe_skip = 255
        femb_conf.strobe_delay = 255
        femb_conf.strobe_length = 255        
      
        
    print('Sending ConfigureWIB command')
    rep = wibpb.Status()
    wib.send_command(req,rep,print_gui=print);
    print(rep.extra.decode('ascii'))
    print('Successful: ',rep.success)

    buf0 = True if 0 in fembs or 1 in fembs else False
    buf1 = True if 2 in fembs or 3 in fembs else False
    print("Collecting RMS Data")    
    try:
        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, print_gui=print)
        samples_shape = np.shape(samples)
        #now = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        #with h5py.File("testfile_rms.hdf5", "a") as f:
            #dset = f.create_dataset(datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")+'rms', samples_shape, dtype='u2', chunks=True)
            #dset[::] = samples
        #print("Saved to hdf5 file")
    except Exception as e:
        raise e
        # #print out glog
  
            
    #print(timestamps)
    #print(np.shape(samples))
    #print(samples)
    #femb = 0
    data = []
    rms_mean = []
    rms_std = []
    for femb in fembs:
        for adc in range(8):
            for ch in range(16):
                #times = np.arange(timestamps.shape[-1])
                sampletemp = samples[femb][adc*16+ch]
                #print(sampletemp)
                rms_mean_temp = np.mean(sampletemp)
                rms_std_temp = np.std(sampletemp)
                rms_mean.append(rms_mean_temp)
                rms_std.append(rms_std_temp)
                #print("ch %d std: %0.2f ADC counts"%(adc*16+ch,rms_std_temp))
                data.append(sampletemp)
                
                fig, ax = plt.subplots()
                ax.plot(sampletemp)
                ax.set(xlabel='Sample index', ylabel='ADC counts', title='RMS noise')  
                plt.grid()        
                #ax.legend(loc='upper right', bbox_to_anchor=(0.35, 0.35))
                # if rms_std_temp > 100:
                    # print("Showing")
                    # plt.show()
                plt.close()                
                
                
        fig, ax = plt.subplots()
        ax.plot(rms_std, marker='.')
        ax.set(xlabel='Channel number', ylabel='ADC counts', title='FEMB%d: RMS noise (1 standard deviation)'%(femb))  
        plt.grid()        
        ax.legend(loc='upper right', bbox_to_anchor=(0.35, 0.35))
        #plt.title('rms '+now)
        # canvas = FigureCanvas(fig)
        # canvas.get_default_filename = lambda: ('rms '+now)
        plt.show()
        plt.close()    
    
    #Toggle pulse
    
    # command_bytes = bytearray("delay 5\n", 'utf-8')
    # #command_bytes.extend(f"cd-i2c {0} {1} {2} {0} {20} {1}\n".encode())
    # for i in range(4):
        # for j in range(2, 4, 1):
            # command_bytes.extend(f"cd-i2c {i} {0} {j} {0} {20} {1}\n".encode())
    
    # req = wibpb.Script()
    # req.script = bytes(command_bytes)
    # return_string = bytes(command_bytes).decode('utf-8')
    # #self.gui_print(f"Sending command\n{return_string}")
    # rep = wibpb.Status()
    # if not wib.send_command(req,rep):
        # req = wibpb.CDFastCmd()
        # req.cmd = 2
        # rep = wibpb.Empty()
        # wib.send_command(req,rep)
        # #self.change_pulser_status()
        # print(f"Pulser toggled")
    # else:
        # print(f"Toggle write:{rep.success}")
        
    req = wibpb.ConfigureWIB()
    #see wib.proto for meanings
    req.pulser = True
    req.cold = False
    req.adc_test_pattern = False
    
    for i in range(4):
        femb_conf = req.fembs.add();
        femb_conf.enabled = True if i in fembs else False
        femb_conf.test_cap = True if i in fembs else False
        femb_conf.gain = 0 #14mv/fc
        femb_conf.peak_time = 3
        femb_conf.baseline = 0
        femb_conf.pulse_dac = 10 
        femb_conf.leak = 0
        femb_conf.leak_10x = False
        femb_conf.ac_couple = False
        femb_conf.buffer = 0
        femb_conf.strobe_skip = 255
        femb_conf.strobe_delay = 255
        femb_conf.strobe_length = 255      
    
    print('Sending ConfigureWIB command')
    rep = wibpb.Status()
    wib.send_command(req,rep,print_gui=print);
    print(rep.extra.decode('ascii'))
    print('Successful: ',rep.success)      
    

    timestamps_all = []
    samples_all = []
    
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
    
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    #with h5py.File("testfile_pulser.hdf5", "a") as f:
    for i in range(100):
        timestamps,samples = wib.acquire_data(buf0 = buf0, buf1 = buf1, print_gui=print)
        timestamps_all.append(timestamps[0])
        samples_all.append(samples)
        samples_shape = np.shape(samples)
            #dset = f.create_dataset(timestamp+'pulse_samp'+str(i), samples_shape, dtype='u2', chunks=True)
            #dset[::] = samples            
        # time_intervals = []
        # for k in range(5):
            # print(timestamps[0][k])
        # for j in range(len(timestamps[0]) - 1):
            # time_intervals.append(timestamps[0][j+1]-timestamps[0][j])
            
        # intv_mean = np.mean(time_intervals)
        # intv_std = np.std(time_intervals)
        # print("Mean interval %0.2f, std dev %0.2f"%(intv_mean, intv_std))
            

    #print(np.shape(samples_all))
    #femb = 0
    #data = []
    for femb in fembs:
    
        rms_mean = []
        data_max = []
        data_min = []

        # peak_loc = []
        # trough_loc = []
        
        ch_slices_averaged = []
        ch_slices_singlesamp = []
        
        ch_pedestal_means = []
        ch_avg_peaks = []
        ch_avg_troughs = []
        valid_channel_numbers = []
        valid_samps_per_ch = []
        
        single_samp_index = random.randint(0, 99)
        
        for adc in range(8):
            for ch in range(16): 
                samples_valid = []
                peak_loc = []
                trough_loc = []            
                for i in range(100):
                    #for each individual sample, find the peak and make sure they match
                    #times = np.arange(timestamps_all[i].shape[-1])
                    # if (adc*16+ch)==0 and i==0:
                        # print(timestamps_all[i])
                    ch_samples = samples_all[i][femb][adc*16+ch]
                    
                    rms_mean_temp = np.mean(sampletemp)
                    # max_temp = np.max(sampletemp)
                    # min_temp = np.min(sampletemp)
                    # std_temp = np.std(sampletemp)     
                    
                    peak_thresh = rms_mean_temp + 2000
                    trough_thresh = rms_mean_temp - 2000
                    peaks, _ = find_peaks(ch_samples, height=peak_thresh)
                    troughs, _ = find_peaks(-1*ch_samples, height=-1*trough_thresh)       

                    #print("ch %d %d peaks, %d troughs"%(adc*16+ch,len(peaks),len(troughs)))
                    
                    if (len(peaks) == 1 and len(troughs) == 1) and (peaks[0] < troughs[0]):
                       
                                      
                        
                        if peaks[0] >= 50 and (len(ch_samples) - troughs[0]) >= 50:                                            
                            #print("Ch %d Sample %d peak loc %d, trough loc %d"%(adc*16+ch,i,peaks[0], troughs[0]))
                            peak_loc.append(peaks[0])
                            trough_loc.append(troughs[0])
                            samples_valid.append(ch_samples)
                            
                            
                
                # overlap_index_first = min(peaks_loc) - 50
                # overlap_index_last =  max(troughs_loc) + 50
                # overlap_len = overlap_index_last - overlap_index_first
                if len(peak_loc) == 0:
                    #print("No good samples for channel %d"%(adc*16+ch))
                    
                    #pick random sample to plot
                    # chsel = random.randint(0, 99)
                    # chsample = samples_all[chsel][femb][adc*16+ch]
                    # rms_mean_temp = np.mean(chsample)
                    
                    # peak_thresh = rms_mean_temp + 2000
                    # trough_thresh = rms_mean_temp - 2000
                    # peaks, _ = find_peaks(chsample, height=peak_thresh)
                    # troughs, _ = find_peaks(-1*chsample, height=-1*trough_thresh)                    
                    
                    # fig, ax = plt.subplots()
                    # ax.plot(chsample)
                    # ax.plot(peaks, chsample[peaks], 'x')
                    # ax.plot(troughs, chsample[troughs], 'x')                
                
                    # ax.sest(xlabel='Sample index', ylabel='ADC counts',
                    # title='ADC no peaks %d Ch%d sample%d %dpk%dtr'%(adc,ch,chsel,len(peaks),len(troughs)))
                    # # fig.savefig("ADC no peaks %d Ch%d sample%d.png"%(adc,ch,chsel))
                    # plt.show()                 
                    
                    pass 
           
                else:
                    
                    
                    peak_trough_dist = [a - b for a, b in zip(trough_loc, peak_loc)]
                    #print(peak_trough_dist)
                    peak_trough_dist = int(max(peak_trough_dist))
                    #print("ch %d peak_trough_dist=%d"%(adc*16+ch,peak_trough_dist))
                    
                    ch_slice_sum = [0] * (peak_trough_dist+100)
                    
                    valid_samps_per_ch.append(len(samples_valid))
                    print("%d: %d valid samples"%(adc*16+ch,valid_samps_per_ch[-1]))
                                  
                    #print("Plotting first valid sample")
                    #print(samples_valid[0])
                    
                    # fig, ax = plt.subplots()
                    # ax.plot(samples_valid[0])
                
                    # ax.set(xlabel='Sample index', ylabel='ADC counts',
                    # title='ADC %d Ch%d sample%d'%(adc,ch,0))
                    # fig.savefig("ADC%d Ch%d sample%d.png"%(adc,ch,0))
                    # plt.close()
                    
                    ch_sel = single_samp_index
                    if len(peak_loc) - 1 < single_samp_index:
                        ch_sel = len(peak_loc) - 1
                    
                    for j in range(len(peak_loc)):
                              
                        ch_samples = samples_valid[j]
                        
                        # fig, ax = plt.subplots()
                        # ax.plot(ch_samples)
                    
                        # ax.set(xlabel='Sample index', ylabel='ADC counts',
                        # title='ADC %d Ch%d sample%d'%(adc,ch,j))
                        # fig.savefig("ADC%d Ch%d sample%d.png"%(adc,ch,j))
                        # plt.close() 
                        

                        pulse_slice = ch_samples[(peak_loc[j] - 50):(peak_loc[j]+peak_trough_dist+50)]
                        
                        ch_slice_sum = [a + b for a, b in zip(ch_slice_sum, pulse_slice)]
                    
                        if j == ch_sel:
                            ch_slices_singlesamp.append(pulse_slice) 
                    
                    ch_slice_avg = [a / len(peak_loc) for a in ch_slice_sum]
                    ch_slices_averaged.append(ch_slice_avg)
                    
                    #Getting positive peak, negative peak, and pedestal
                    pedestal = np.mean(ch_slice_avg[0:25])
                    
                    ch_pedestal_means.append(pedestal)                
                    ch_avg_peaks.append(max(ch_slice_avg))
                    ch_avg_troughs.append(min(ch_slice_avg)) 
                    
                    valid_channel_numbers.append(adc*16+ch)
                    

        chs_valid = len(valid_channel_numbers)
        if chs_valid < 128:
            print("FEMB%d: Not all channels valid"%(femb))
            all_channels_good = False
            
        else:
        
        
            fig, ax = plt.subplots()
            min_slice_length = min([len(a) for a in ch_slices_averaged])
            x = [a * 0.5 for a in list(range(min_slice_length))]
            for ch in ch_slices_averaged:
                ax.plot(x, ch[:min_slice_length])
            
            min_valid_samps = min(valid_samps_per_ch)
            max_valid_samps = max(valid_samps_per_ch)
            if min_valid_samps == max_valid_samps:
                cycles_str = '%d'%(min_valid_samps)
            else:
                cycles_str = '%d-%d'%(min_valid_samps,max_valid_samps)
            
            ax.set(xlabel='Time (us)', ylabel='ADC counts',
            title='FEMB%d: Averaged (%s cycles) Waveform Overlap of %d channels'%(femb,cycles_str,chs_valid))
            plt.grid()
            # canvas = FigureCanvas(fig)
            # canvas.get_default_filename = lambda: ('averaged '+now)
            #fig.savefig("ADC%d Ch%d averaged.png"%(adc,ch))              
            plt.show()
            plt.close()

            fig, ax = plt.subplots()
            min_slice_length = min([len(a) for a in ch_slices_singlesamp])
            x = [a * 0.5 for a in list(range(min_slice_length))]
            for ch in ch_slices_singlesamp:
                ax.plot(x, ch[:min_slice_length])
            
            if max_valid_samps < single_samp_index:
                single_samp_index = max_valid_samps
                
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            
            ax.set(xlabel='Time (us)', ylabel='ADC counts',
            title="FEMB%d: Waveform Overlap of %d channels' %s or last valid sample"%(femb,chs_valid, ordinal(single_samp_index)))
            plt.grid()
            #plt.title('raw '+now)
            # canvas = FigureCanvas(fig)
            # canvas.get_default_filename = lambda: ('raw '+now)        
            #fig.savefig("ADC%d Ch%d averaged.png"%(adc,ch))              
            plt.show()
            plt.close()

            fig, ax = plt.subplots()
            ax.plot(valid_channel_numbers, ch_avg_peaks, label='Positive Peak', ls='None', marker='.')
            ax.plot(valid_channel_numbers, ch_pedestal_means, label='Pedestal', ls='None', marker='.')        
            ax.plot(valid_channel_numbers, ch_avg_troughs, label='Negative Peak', ls='None', marker='.')
            ax.set(xlabel='Channel number', ylabel='ADC counts', title='FEMB%d: Averaged channel stats'%(femb))  
            plt.grid()        
            ax.legend(loc='upper right', bbox_to_anchor=(0.35, 0.35))
            # canvas = FigureCanvas(fig)
            # canvas.get_default_filename = lambda: ('s '+now)         
            plt.show()
            plt.close()
    if all_channels_good == False:
        print("Not all channels valid for all FEMBs, trying again")
        #mainfunc()
    req = wibpb.LogControl()
    req.return_log = False
    req.boot_log = False
    req.clear_log = True
    print("Clearing Log...") 
    rep = wibpb.LogControl.Log()
    if not wib.send_command(req,rep,print_gui=print):
        print(rep.contents.decode('utf8'))   

if __name__ == "__main__":
    mainfunc()
