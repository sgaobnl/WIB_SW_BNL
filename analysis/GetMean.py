import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import sys


fp = "D:/IO-1865-1C/QC/reports/FEMB107_LN_150pF/CALI/Gain_200mVBL_14_0mVfC_2_0us.bin"

with open(fp, 'rb') as fn:
     raw = pickle.load(fn)

print(len(raw))

enc = np.array(raw[0])
mean = np.mean(enc)
std = np.std(enc)
print(mean)
print(std)
