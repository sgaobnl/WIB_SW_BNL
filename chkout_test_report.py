import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import time


def Clean_data(fname):

    fdir = "D:/debug_data/"
    folder = fname
    datafdir = fdir+folder+'/'
    fb = data_organization(folder)

    sncs = ["900mVBL", "200mVBL"]
    sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
    sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

    for snci in sncs:
        for sgi in sgs:
            for sti in sts:
                se_rms_file = "Raw_RMS_SE_{}_{}_{}.bin".format(snci, sgi, sti)
                datafile = datafdir + se_rms_file
                outfile = "SE_{}_{}_{}".format(snci, sgi, sti)

                fb.GetRMS(datafile,outfile)

                if sgi=="14_0mVfC":
                    diff_rms_file = "Raw_RMS_DIFF_{}_{}_{}.bin".format(snci, sgi, sti)
                    datafile = datafdir + diff_rms_file
                    outfile = "DIFF_{}_{}_{}".format(snci, sgi, sti)
                    fb.GetRMS(datafile,outfile)

                if sti=="2_0us":
                    dac_file = "Raw_CALI_SE_{}_{}_{}.bin".format(snci, sgi, sti)
                    datafile = datafdir + diff_rms_file
                    outfile = "SE_{}_{}_{}".format(snci, sgi, sti)
                    fb.GetGain(datafdir,outfile)


