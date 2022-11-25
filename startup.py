from wib_cfgs import WIB_CFGS
from wib import WIB
import time
import sys
import time, datetime, random, statistics


ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]
#ips = [ "10.73.137.29", "10.73.137.31"]
#ips = [  "10.73.137.31"]
chk = WIB_CFGS()

pwr_info = []
for ip in ips:
    chk.wib = WIB(ip)
    chk.wib_init()
    chk.wib_timing(pll=True, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
    chk.wib_i2c_adj(n=300)
    ####################FEMBs powering################################
    #set FEMB voltages
    chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
    
print ("Done")

