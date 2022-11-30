from wib_cfgs import WIB_CFGS
from wib import WIB
import time
import sys
import time, datetime, random, statistics


ips = ["10.73.137.27", "10.73.137.29", "10.73.137.31"]
chk = WIB_CFGS()
n = int(sys.argv[1])

pwr_info = []
for ip in ips:
    chk.wib = WIB(ip)
    chk.wib_i2c_adj(n=n)
print ("Done")

