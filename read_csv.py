# -*- coding: utf-8 -*-
"""
File Name: read_rtds.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: Thu Jan 18 14:35:04 2018
Last modified: 1/15/2023 8:55:52 AM
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

dp =  "D:/GitHub/WIB_SW_BNL/CRP5A/"
if (os.path.exists(dp)):
    for root, dirs, files in os.walk(dp):
        break

for fp in files:
    fpp = root + fp
    print (fpp)
    tindexs = []
    with open(fpp, 'r') as fn:
        for cl in fn:
            tmp = cl[:-1].split(",")
            tindexs.append ([tmp[1],tmp[3],tmp[6], tmp[8]] )
    print (tindexs)

    exit()
#index_f =
#tindexs = []
#with open(index_f, 'r') as fp:
#    for cl in fp:
#        tindexs.append ( cl.split(","))
#
#tindexs = tindexs[1:]
#run_rtds(rootpath = './', runtime = '2018-01-15 18:00') 
