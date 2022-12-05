import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
import os
import os.path
from rawdata_dec import rawdata_dec 

fdir = sys.argv[1] 
runs = int(sys.argv[2])

if (os.path.exists(fdir)):
    for root, dirs, files in os.walk(fdir):
        break

for fbin in files:
    if ".bin" in fbin:
        fp = fdir + fbin
        print (fp)
    else:
        continue

    with open(fp, 'rb') as fn:
        rawinfo = pickle.load(fn)
    pwr_meas = rawinfo[1]
    print (pwr_meas)
    set_feparas = rawinfo[3]
    print (set_feparas)
    
    lruns = len(rawinfo[0])
    if lruns < runs:
        runs = lruns
    rawdata = rawdata_dec(raw=rawinfo, runs=runs, plot_show_en = True, plot_fn = "", rms_flg=False, chdat_flg=True, ts_flg=True )
    
    fp = fp[0:-4] + ".dat" 
    with open(fp, 'wb') as fn:
        pickle.dump(rawdata, fn)
    
    fp = fp[0:-4] + ".set" 
    with open(fp, 'wb') as fn:
        pickle.dump(set_feparas, fn)
