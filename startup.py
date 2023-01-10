from wib_cfgs import WIB_CFGS
from wib import WIB
import time
import sys

ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]
chk = WIB_CFGS()
localclk_cs = (int(sys.argv[1]) == 1)
print (localclk_cs)

pwr_info = []
for ip in ips:
    chk.wib = WIB(ip)
    chk.wib_init()
    chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)

    chk.wib_timing(localclk_cs=True, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
    time.sleep(1)
    chk.wib_timing(localclk_cs=localclk_cs, fp1_ptc0_sel=0, cmd_stamp_sync = 0x0)
print ("Done")

