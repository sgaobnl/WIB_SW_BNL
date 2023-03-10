# -*- coding: utf-8 -*-
"""
File Name: read_rtds.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: Thu Jan 18 14:35:04 2018
Last modified: 1/15/2023 4:52:47 PM
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl


import numpy as np
import struct
import os
from sys import exit
import sys
import os.path
import time
import datetime
import pickle

dp =  "D:/GitHub/WIB_SW_BNL/CRP5A/"
if (os.path.exists(dp)):
    for root, dirs, files in os.walk(dp):
        break

fembchns = []
crp_fembmapping = []
chns_c = []
for i in range(12):
    for j in range(128):
        chns_c.append(0)
for fp in files:
    fpp = root + fp
    print (fpp)
    if "chn_mapping" in fp:
        with open(fpp, 'r') as fn:
            for cl in fn:
                tmp = cl[:-1].split(",")
                fembchns.append ([int(tmp[0]),int(tmp[1]),int(tmp[2]), int(tmp[3])] )

        print (fembchns)
        continue

    pos0 = fpp.find("FEMB")
    pos1 = fpp.find("_CE")
    fembno = int(fpp[pos0+4:pos1])
    femb_c = []
    with open(fpp, 'r') as fn:
        for cl in fn:
            if "GND" in cl:
                cl = cl.replace("GND", "500")
            if "gnd" in cl:
                cl = cl.replace("gnd", "500")
            if cl[-1] == "\n":
                tmp = cl[:-1].split(",")
            else:
                tmp = cl.split(",")
#            print (cl)
            femb_c.append ([int(tmp[1]),int(tmp[3]),int(tmp[6]), int(tmp[8])] )
            if (int(tmp[1]) <50) or  (int(tmp[3]) <50) or  (int(tmp[6]) <50) or  (int(tmp[8]) <50):
                print (fembno, cl)
            

    for x in range(len(fembchns)):
        chns_c[fembchns[x][0] + (fembno-1)*128] = femb_c[x][0]
        chns_c[fembchns[x][1] + (fembno-1)*128] = femb_c[x][1]
        chns_c[fembchns[x][2] + (fembno-1)*128] = femb_c[x][2]
        chns_c[fembchns[x][3] + (fembno-1)*128] = femb_c[x][3]

fp = dp + "../CRP5A_CAP.bin"
with open(fp, 'wb') as fn:
    pickle.dump( chns_c, fn)    
#    print (tindexs)
#print (chns_c)
#    exit()
#index_f =
#tindexs = []
#with open(index_f, 'r') as fp:
#    for cl in fp:
#        tindexs.append ( cl.split(","))
#
#tindexs = tindexs[1:]
#run_rtds(rootpath = './', runtime = '2018-01-15 18:00') 
