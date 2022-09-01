import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import time
from scipy.signal import find_peaks

class data_organization():
    def __init__(self,fdir, needfolder=False):

        if needfolder:
           #save_dir='D:/debug_data/cleaned_data/'+fdir
           save_dir='/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/'+fdir
   
           n=1
           while (os.path.exists(save_dir)):
               if n==1:
                   save_dir = save_dir + "_{:02d}".format(n)
               else:
                   save_dir = save_dir[:-2] + "{:02d}".format(n)
               n=n+1
               if n>20:
                   raise Exception("There are more than 20 folders...")
   
           try:
               os.makedirs(save_dir)
           except OSError:
               print ("Error to create folder %s"%save_dir)
               sys.exit()

           fdir = save_dir

        self.fdir_plots = fdir+'/plots/'
        try:
            os.makedirs(self.fdir_plots)
        except OSError:
            print ("Error to create folder %s"%self.fdir_plots)
            sys.exit()

        self.fdir_data = fdir+'/data/'
        try:
            os.makedirs(self.fdir_data)
        except OSError:
            print ("Error to create folder %s"%self.fdir_data)
            sys.exit()

        dac_v = {}  # mV/bit
        dac_v['4_7mVfC']=18.66
        dac_v['7_8mVfC']=14.33
        dac_v['14_0mVfC']=8.08
        dac_v['25_0mVfC']=4.61

        CC=1.85*pow(10,-13)
        e=1.602*pow(10,-19)

        self.dac_v = dac_v
        self.CC = CC
        self.e = e

    def GetRMS(self,datafile,outfile):

        fp = datafile
        with open(fp, 'rb') as fn:
             raw = pickle.load(fn)

        rawdata = raw[0]
        pwr_meas = raw[1]
        logs = raw[3]

        rms_data = np.array(self.data_valid(rawdata),dtype=object)
        nfemb=len(rms_data[0])//128

        if nfemb != len(logs['femb id']):
            print("The number of FEMBs in data is not equal to that in the logs! Exiting...")
            sys.exit()
       
        femb_no = []
        for key,value in logs['femb id'].items():
            femb_no.append(value) # assume the id is stored in increasing order

        rms_dic={}
        for i in range(nfemb):
            a_rms=np.empty(0)
            a_ped=np.empty(0)
            for ch in range(128):
                global_ch = i*128+ch 
                ch_arr = rms_data[:,global_ch]
                ch_np = np.empty(0)
                for j in ch_arr:
                    ch_np = np.hstack([ch_np,np.array(j)])
                a_rms=np.append(a_rms,np.std(ch_np))
                a_ped=np.append(a_ped,np.mean(ch_np))

            fig, ax =plt.subplots(figsize=(8,4))
            xx=range(128)
            ax.scatter(xx,a_rms,marker='.')
            ax.set_xlabel('chan')
            ax.set_ylabel('rms')
            ax.set_title('FEMB{} {}'.format(femb_no[i],outfile))
            fig.savefig(self.fdir_plots+"rms_femb{}_{}.png".format(femb_no[i], outfile))
            plt.close()
            rms_dic['femb{}'.format(femb_no[i])]=[a_ped,a_rms]

            fp = self.fdir_data+"rms_femb{}_{}.bin".format(femb_no[i], outfile)
            with open(fp, 'wb') as fn:
                pickle.dump( {'Ped':a_ped,'RMS':a_rms}, fn)

        return rms_dic

    def GetPeak(self,datafile):

        fp = datafile
        with open(fp, 'rb') as fn:
             raw = pickle.load(fn)

        rawdata = raw[0]
        logs = raw[3]

        pl_data = np.array(self.data_valid(rawdata),dtype=object)
        nfemb = len(pl_data[0])//128
        nevent = len(pl_data)

        if nfemb != len(logs['femb id']):
            print("The number of FEMBs in data is not equal to that in the logs! Exiting...")
            sys.exit()
       
        femb_no = []
        for key,value in logs['femb id'].items():
            femb_no.append(value) # assume the id is stored in increasing order

        dic={}
        for i in range(nfemb):
            peaks = np.empty(0)
            for ch in range(128):
                global_ch = i*128+ch
                pmax = np.amax(pl_data[0][global_ch])
                
                pos = np.argmax(pl_data[0][global_ch])

                p_val=np.empty(0)
                for itr in range(nevent):
                    pos_peaks, _ = find_peaks(pl_data[itr][global_ch],height=pmax-100)
                    p_val = np.hstack([p_val,pl_data[itr][global_ch][pos_peaks]])

                peaks=np.append(peaks,np.mean(p_val))

            dic['femb{}'.format(femb_no[i])]=peaks

        return dic

    def ChkLinearty(self, pkval, dac, steps):
       
        slope,intercept=np.polyfit(dac[:4],pkval[:4],1)   # ask shanshan what is a good number to use for initial fitting

        y_min = pkval[0]
        y_max = pkval[-1]
        linear_dac_max=len(dac)-1

        delta_y=[]
        first = True
        for i in range(len(dac)):
            y_r = pkval[i]
            y_p = dac[i]*slope + intercept
            inl = abs(y_r-y_p)/(y_max-y_min)
            delta_y.append(inl)
            if inl>0.02 and first:
               first=False
               linear_dac_max = i-1
              

        slope_final,intercept_final = np.polyfit(dac[:(linear_dac_max+1)],pkval[:(linear_dac_max+1)],1)

        INL=[]
        y_min = pkval[0]
        y_max = pkval[linear_dac_max]
        for i in range(linear_dac_max+1):
            y_r = pkval[i]
            y_p = dac[i]*slope_final + intercept_final
            inl = abs(y_r-y_p)/(y_max-y_min)
            INL.append(inl)

        INL_final = max(INL)

        debug=False
        if debug:
           fig,axes = plt.subplots(1,3)
           axes[0].plot(dac, pkval)
           axes[1].plot(dac[:(linear_dac_max+1)],INL[:(linear_dac_max+1)])
           axes[2].plot(dac, delta_y)
           plt.show()
 
        return [linear_dac_max, INL_final, slope_final]

    def GetGain(self,datafdir,outfile):

        if '4_7mVfC' in outfile:  # mV/bit
            dac_v = self.dac_v['4_7mVfC']

        if '7_8mVfC' in outfile:  # mV/bit
            dac_v = self.dac_v['7_8mVfC']

        if '14_0mVfC' in outfile:  # mV/bit
            dac_v = self.dac_v['14_0mVfC']

        if '25_0mVfC' in outfile:  # mV/bit
            dac_v = self.dac_v['25_0mVfC']

        dac_v = dac_v/1000 # V/bit

        CC=self.CC
        e=self.e

        datafile = datafdir+"Raw_CALI_{}_0x00.bin".format(outfile)
        rms_dic=self.GetRMS(datafile, "CALI_{}".format(outfile))

        pk_list=[]
        for dac in range(4,64,4):
            datafile = datafdir+"Raw_CALI_{}_0x{:02x}.bin".format(outfile,dac)
            
            pk_dic = self.GetPeak(datafile)
            pk_list.append(pk_dic)
       
        xx=range(0,64,4)

        if len(rms_dic) != len(pk_list[0]):
           print("Something wrong here!!! Not have the same number of FEMBs. Exiting...")
           sys.exit()

        nfemb=len(rms_dic)

        for key,values in rms_dic.items():
            fig, ax =plt.subplots(figsize=(8,4))
            gain_list=[]
            enc_list=[]
            linear_range_list=[]
            inl_list=[]
            for ch in range(128):
                pk_val=[]
                for j in range(len(xx)):
                    if j==0:
                        pk_val.append(rms_dic[key][0][ch])
                    else:
                        pk_val.append(pk_list[j-1][key][ch])
                linearty = self.ChkLinearty(pk_val, xx, 4)
                tmp_gain = linearty[2]
                
                ax.plot(xx, pk_val)
                linear_range_list.append(xx[linearty[0]])
                inl_list.append(linearty[1])
                gain_list.append(tmp_gain)

                a_rms = rms_dic[key][1][ch]
                enc_list.append(a_rms/(tmp_gain/dac_v)*CC/e)

            fp_1 = self.fdir_data+"gain_{}_{}.bin".format(key, outfile)
            with open(fp_1, 'wb') as fn_1:
                pickle.dump( gain_list, fn_1)

            fp_2 = self.fdir_data+"enc_{}_{}.bin".format(key, outfile)
            with open(fp_2, 'wb') as fn_2:
                pickle.dump( enc_list, fn_2)

            ax.set_xlabel('DAC')
            ax.set_ylabel('Peak value')
            ax.set_title('{} {}'.format(key,outfile))
            fig.savefig(self.fdir_plots+"cali_peak_dac_{}_{}.png".format(key, outfile))
            plt.close()

            fig1, ax1 =plt.subplots(figsize=(8,4))
            ax1.scatter(range(128),gain_list,marker='.')
            ax1.set_xlabel('chan')
            ax1.set_ylabel('gain')
            ax1.set_title('{} {}'.format(key,outfile))
            fig1.savefig(self.fdir_plots+"cali_gain_{}_{}.png".format(key, outfile))
            plt.close()

            fig2, ax2 =plt.subplots(figsize=(8,4))
            ax2.scatter(range(128),enc_list,marker='.')
            ax2.set_xlabel('chan')
            ax2.set_ylabel('ENC')
            ax2.set_title('{} {}'.format(key, outfile))
            fig2.savefig(self.fdir_plots+"cali_ENC_{}_{}.png".format(key, outfile))
            plt.close()

            fig3, ax3 =plt.subplots(figsize=(8,4))
            ax3.scatter(range(128), linear_range_list)
            ax3.set_xlabel('chan')
            ax3.set_ylabel('DAC')
            ax3.set_title('{} {} Linear range'.format(key, outfile))
            fig3.savefig(self.fdir_plots+"cali_linear_range_{}_{}.png".format(key, outfile))
            plt.close()

            fig4, ax4 =plt.subplots(figsize=(8,4))
            ax4.scatter(range(128),inl_list)
            ax4.set_xlabel('chan')
            ax4.set_ylabel('INL')
            ax4.set_title('{} {} INL (within linear range)'.format(key, outfile))
            fig4.savefig(self.fdir_plots+"cali_INL_{}_{}.png".format(key, outfile))
            plt.close()

if __name__=='__main__':

#    fdir = "D:/debug_data/"
#    folder = "FEMB_femb0_femb1_femb2_femb3_RT_0pF_R002"
#    datafdir = fdir+folder+'/'
#
#    filename = "Raw_RMS_SE_200mVBL_14_0mVfC_0_5us.bin"
#    datafile = datafdir+filename
#    fb = data_organization(folder, True)
#
#    fb.GetRMS(datafile,'SE_200mVBL_14_0mVfC_0_5us')
#    fb.GetGain(datafdir,'SE_200mVBL_14_0mVfC_2_0us')
    
    fdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/"
    folder = "femb1_femb2_femb3_femb4_RT_0pF_R001"
    datafdir = fdir+folder+'/'

    filename = "Raw_RMS_SE_200mVBL_14_0mVfC_0_5us.bin"
    datafile = datafdir+filename
    fb = data_organization(folder, needfolder=True)

    #fb.GetRMS(datafile,'SE_200mVBL_14_0mVfC_0_5us')
    fb.GetGain(datafdir,'SE_200mVBL_7_8mVfC_2_0us')
