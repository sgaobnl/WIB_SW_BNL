import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
from scipy.signal import find_peaks

class FEMB_Basics():
    def __init__(self,folder, outfile):
        self.folder=folder
        self.outfile=outfile[:-4]  # assume is a *.bin file

    def data_valid(self, raw):
        sss  = []
        for rawi in raw:
            ts = rawi[0]
            ss = rawi[1]
            chns = []
            for link in range(2):
                tv = [0]
                for i in range(len(ts[link])-1):
                    t0 = int(ts[link][i])>>32>>21
                    t1 = int(ts[link][i+1])>>32>>21
                    if (abs(t1-t0) > 2) and (t1 != 0x000) and (t0 !=0x3ff):
                        tv.append(i)
                tv.append(len(ts[link])-1)
                tg = []
                for tvi in range(len(tv)-1):
                    tg.append(tv[tvi+1]-tv[tvi])
                pos = np.where(tg == np.max(tg))[0][0]
    
                for chi in range(len(ss[0+link*2])):
                    chns.append(ss[0+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
                for chi in range(len(ss[1+link*2])):
                    chns.append(ss[1+link*2][chi][(tv[pos]+1):(tv[pos+1]-1)])
            sss.append(chns)
        return sss

    def PrintPWR(self, pwr_meas):

        pwr_names=['BIAS','LArASIC','ColdDATA','ColdADC']
        for key,values in pwr_meas.items():
            pwr_dic={'name':[],'V_meas/V':[],'I_meas/A':[],'P_meas/W':[]}
            i=0
            for ilist in values:
                #pwr_dic['name'].append(ilist[0])
                pwr_dic['name'].append(pwr_names[i])
                i=i+1
                pwr_dic['V_meas/V'].append(round(ilist[1],3))
                pwr_dic['I_meas/A'].append(round(ilist[2],3))
                pwr_dic['P_meas/W'].append(round(ilist[3],3))

            df=pd.DataFrame(data=pwr_dic)

            fig, ax =plt.subplots(figsize=(8,2.5))
            ax.axis('off')
            table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
            ax.set_title(key)
            table.set_fontsize(14)
            table.scale(1,2)
            fig.savefig(self.folder+"pwr_meas_{}_{}.png".format(key,self.outfile))
           

    def GetRMS(self,datafile):

        fp = datafile
        with open(fp, 'rb') as fn:
             raw = pickle.load(fn)

        rawdata = raw[0]
        pwr_meas = raw[1]

        #self.PrintPWR(pwr_meas)

        rms_data = np.array(self.data_valid(rawdata),dtype=object)
        nfemb=len(rms_data[0])//128
       
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

            fig, ax =plt.subplots(figsize=(6,4))
            xx=range(128)
            ax.scatter(xx,a_rms,marker='.')
            ax.set_xlabel('chan')
            ax.set_ylabel('rms')
            ax.set_title('FEMB{}'.format(i))
            fig.savefig(self.folder+"rms_femb{}_{}.png".format(i, self.outfile))
            plt.close()
            pd.DataFrame(a_rms,columns=['femb{}'.format(i)]).to_csv(self.folder+"rms_femb{}_{}.csv".format(i,self.outfile))
            rms_dic['femb{}'.format(i)]=[a_ped,a_rms]
        return rms_dic

    def GetPeak(self,datafile):

        fp = datafile
        with open(fp, 'rb') as fn:
             raw = pickle.load(fn)

        rawdata = raw[0]

        pl_data = np.array(self.data_valid(rawdata),dtype=object)
        nfemb = len(pl_data[0])//128
        nevent = len(pl_data)

        dic={}
        for i in range(nfemb):
            peaks = np.empty(0)
            fig, ax =plt.subplots(figsize=(6,4))
            for ch in range(128):
                global_ch = i*128+ch
                pmax = np.amax(pl_data[0][global_ch])
                
                pos = np.argmax(pl_data[0][global_ch])
                waveforms=pl_data[0][global_ch][pos-100:pos+100]
                ax.plot(range(len(waveforms)),waveforms)

                p_val=np.empty(0)
                for itr in range(nevent):
                    pos_peaks, _ = find_peaks(pl_data[itr][global_ch],height=pmax-100)
                    p_val = np.hstack([p_val,pl_data[itr][global_ch][pos_peaks]])

                peaks=np.append(peaks,np.mean(p_val))

            ax.set_xlabel('tick')
            ax.set_ylabel('ADC')
            ax.set_title('FEMB{}'.format(i))
            fig.savefig(self.folder+"cali_pulse_femb{}_{}.png".format(i, self.outfile))
            plt.close()

#            print('pk: ', len(peaks))
            dic['femb{}'.format(i)]=peaks

        return dic

    def GetGain(self,datafolder,outfile):
        
        datafile = datafolder+"Raw_CALI_200mVBL_14_0mVfC_2_0us_0x00_03_08_2022.bin"
        rms_dic=self.GetRMS(datafile)

        pk_list=[]
        for dac in range(4,64,4):
            datafile = datafolder+"Raw_CALI_200mVBL_14_0mVfC_2_0us_0x{:02x}_03_08_2022.bin".format(dac)
            
            pk_dic = self.GetPeak(datafile)
            pk_list.append(pk_dic)
       
        xx=range(0,64,4)
        nfemb=len(rms_dic)

        gain={}
        for i in range(nfemb):
            fig, ax =plt.subplots(figsize=(6,4))
            gain_list=[]
            enc_list=[]
            for ch in range(128):
                pk_val=[]
                for j in range(len(xx)):
                    if j==0:
                        pk_val.append(rms_dic['femb{}'.format(i)][0][ch])
                    else:
                        pk_val.append(pk_list[j-1]['femb{}'.format(i)][ch])
                ax.plot(xx, pk_val)
                slope,intercept=np.polyfit(xx[:10],pk_val[:10],1)
                gain_list.append(slope)
                a_rms = rms_dic['femb{}'.format(i)][1][ch]
                enc_list.append(slope*a_rms)
            gain['femb{}'.format(i)]=gain_list

            ax.set_xlabel('DAC')
            ax.set_ylabel('Peak value')
            ax.set_title('FEMB{}'.format(i))
            fig.savefig(self.folder+"cali_peak_dac_femb{}_{}.png".format(i, outfile))
            plt.close()

            fig1, ax1 =plt.subplots(figsize=(6,4))
            ax1.scatter(range(128),gain_list,marker='.')
            ax1.set_xlabel('chan')
            ax1.set_ylabel('gain')
            ax1.set_title('FEMB{}'.format(i))
            fig1.savefig(self.folder+"cali_gain_femb{}_{}.png".format(i, outfile))
            plt.close()

            fig2, ax2 =plt.subplots(figsize=(6,4))
            ax2.scatter(range(128),enc_list,marker='.')
            ax2.set_xlabel('chan')
            ax2.set_ylabel('ENC')
            ax2.set_title('FEMB{}'.format(i))
            fig2.savefig(self.folder+"cali_ENC_femb{}_{}.png".format(i, outfile))
            plt.close()


if __name__=='__main__':

    datafolder = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/"
    filename = "Raw_CALI_200mVBL_14_0mVfC_2_0us_0x00_03_08_2022.bin"
    results_folder="/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/WIB_SW_BNL/analysis/results/"
    datafile = datafolder+filename
    fembs = FEMB_Basics(results_folder,filename)
    #fembs.GetRMS(datafile)
    fembs.GetGain(datafolder,'Raw_CALI_200mVBL_14_0mVfC_2_0us_03_08_2022')
    
#    fp = datafile
#    with open(fp, 'rb') as fn:
#         raw = pickle.load(fn)
#
#    rawdata = raw[0]
#    pwr_meas = raw[1]
#    fembs.PrintPWR(pwr_meas)
#
