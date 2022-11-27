import time
import sys
import numpy as np
import pickle
import copy
import time, datetime, random, statistics
from wib import WIB
import os
from rawdata_dec import rawdata_dec 

if True:
    save_dir = "D:/CRP5A/Warm_runs_done/Run02_R004/"
    fp ="D:/CRP5A/Warm_runs_done/Run02_R004/Raw_SW_Trig27_11_2022_01_09_05.bin" 

    with open(fp, 'rb') as fn:
        rawinfo = pickle.load(fn)

    rawdata_dec(raw=rawinfo, runi=0, plot_show_en = False, plot_fn = save_dir + "pulse_respons.png", rms_flg=True)
    print ("Done!")
