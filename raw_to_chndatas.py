import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
import os
from rawdata_dec import rawdata_dec 

fp = sys.argv[1] 
chn = int(sys.argv[2] )
runs = int(sys.argv[3])

with open(fp, 'rb') as fn:
    rawinfo = pickle.load(fn)

lruns = len(rawinfo[0])
if lruns < runs:
    runs = lruns
rawdata = rawdata_dec(raw=rawinfo, runs=runs, plot_show_en = True, plot_fn = "", rms_flg=False, chdat_flg=True )
print (len(rawdata), len(rawdata[0]))
pwr_meas = rawinfo[1]
print (pwr_meas)
set_feparas = rawinfo[3]
#[sts, snc, sg0, sg1, st0, st1, sdf, slk0, slk1] = rawinfo[3]

fp = fp[0:-4] + ".dat" 
with open(fp, 'wb') as fn:
    pickle.dump(rawdata, fn)

fp = fp[0:-4] + ".set" 
with open(fp, 'wb') as fn:
    pickle.dump(set_feparas, fn)
