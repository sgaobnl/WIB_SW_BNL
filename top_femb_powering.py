from wib_cfgs import WIB_CFGS
import low_level_commands as llc
from wib import WIB
import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics

print ("Powering FEMB")
print ("help: python chkout_powering on on on on") 

if len(sys.argv) !=5 :
    print('Please specify 4 FEMBs power operation (on or off)')
    exit()    

fembs = []
if 'on' in sys.argv[1]:
    fembs.append(0)
if 'on' in sys.argv[2]:
    fembs.append(1)
if 'on' in sys.argv[3]:
    fembs.append(2)
if 'on' in sys.argv[4]:
    fembs.append(3)
ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]
#ips = [ "10.73.137.29", "10.73.137.31"]
ips = ["10.73.137.27"]
chk = WIB_CFGS()

pwr_info = []
for ip in ips:
    chk.wib = WIB(ip)
    
    chk.wib_init()
#    chk.wib_i2c_adj(n=500)
    chk.wib_timing(pll=True, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
    
    ####################FEMBs powering################################
    #set FEMB voltages
    chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
    
    #power on FEMBs
    chk.femb_powering(fembs)
    if len(fembs) != 0:
        print (f"Turn FEMB {fembs} on")
        chk.femb_cd_rst()
    else:
        print (f"Turn All FEMB off")
    #Measure powers on FEMB
    pwr_meas = chk.get_sensors()

    for key in pwr_meas:
        print (pwr_meas[key])
    
    pwr_info.append([ip, pwr_meas])

fdir = "D:/debug_data/"
ts = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
fp = fdir + "Power_" + ts  + ".bin"
with open(fp, 'wb') as fn:
    pickle.dump(pwr_info, fn)

print ("Done")

