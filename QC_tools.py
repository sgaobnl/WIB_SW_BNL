import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import sys
from spymemory_decode import wib_spy_dec_syn
import time

class QC_tools:
    def __init__(self):
        x='hello'

    def data_valid(self,raw):
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

    def data_decode(self,raw):

        nevent = len(raw) 
        sss=[]
     
        for i in range(nevent):
            buf0 = raw[i][0]
            buf1 = raw[i][1]
            
            wib_data = wib_spy_dec_syn(buf0, buf1)
            nsamples = len(wib_data[0])

            chns=[]
            for j in range(nsamples):
                a0 = wib_data[0][j]["FEMB0_2"]
                a1 = wib_data[0][j]["FEMB1_3"]
                a2 = wib_data[1][j]["FEMB0_2"]
                a3 = wib_data[1][j]["FEMB1_3"]
                aa=a0+a1+a2+a3
                chns.append(aa)

            chns = list(zip(*chns))    
            sss.append(chns) 
               
        return sss        

    def data_ana(self, data, nfemb):
        
        nevent = len(data)

        if nevent>100:
           nevent=100

        rms=[]
        ped=[]
        pkp=[]
        pkn=[]
        onewf=[]
        avgwf=[] 

        for ich in range(128):
            global_ch = nfemb*128+ich
            peddata=np.empty(0)
            pkpdata=np.empty(0)
            pkndata=np.empty(0)
            wfdata = np.zeros(500)

            npulse=0
            first = True
            for itr in range(nevent):
                evtdata = data[itr][global_ch] 
                pmax = np.amax(evtdata)
                pos = np.argmax(evtdata)

                pos_peaks, _ = find_peaks(evtdata,height=pmax-100)

                for ipos in pos_peaks:
                    startpos=ipos-50
                    if startpos<0:
                       continue

                    if startpos+500>=len(evtdata):
                       break

                    tmp_wf = evtdata[startpos:startpos+500]     # one wave
                    if first:
                       onewf.append(tmp_wf)
                       first=False
 
                    npulse=npulse+1
                    wfdata = wfdata + tmp_wf
                    peddata = np.hstack([peddata,tmp_wf[200:450]])
                    pkpdata = np.hstack([pkpdata,np.max(tmp_wf)])
                    pkndata = np.hstack([pkndata,np.min(tmp_wf)])

            ch_ped = np.mean(peddata)
            ch_rms = np.std(peddata)
            ch_pkp = np.mean(pkpdata)
            ch_pkn = np.mean(pkndata)

            ped.append(ch_ped)
            rms.append(ch_rms)
            pkp.append(ch_pkp)
            pkn.append(ch_pkn)
 
            if npulse>0:
                avgwf.append(wfdata/npulse)
            else:
                print("femb {} ch{} doesn't have pulse!".format(nfemb,ich))
                sys.exit()

        return rms,ped,pkp,pkn,onewf,avgwf 

    def FEMB_SUB_PLOT(self, ax, x, y, title, xlabel, ylabel, color='b', marker='.', atwinx=False, ylabel_twx = "", e=None):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        if (atwinx):
            ax.errorbar(x,y,e, marker=marker, color=color)
            y_min = int(np.min(y))-1000
            y_max = int(np.max(y))+1000
            ax.set_ylim([y_min, y_max])
            ax2 = ax.twinx()
            ax2.set_ylabel(ylabel_twx)
            ax2.set_ylim([int((y_min/16384.0)*2048), int((y_max/16384.0)*2048)])
        else:
            ax.plot(x,y, marker=marker, color=color)

    def FEMB_CHK_PLOT(self, chn_rmss,chn_peds, chn_pkps, chn_pkns, chn_onewfs, chn_avgwfs, fp):
        fig = plt.figure(figsize=(10,5))
        fn = fp.split("/")[-1]
        print (fn)
        ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
        ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
        ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
        ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
        chns = range(128)
        self.FEMB_SUB_PLOT(ax1, chns, chn_rmss, title="RMS Noise", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_peds, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_pkps, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='b', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_pkns, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='g', marker='.')
        for chni in chns:
            ts = 100
            x = (np.arange(ts)) * 0.5
            y3 = chn_onewfs[chni][25:ts+25]
            y4 = chn_avgwfs[chni][25:ts+25]
            self.FEMB_SUB_PLOT(ax3, x, y3, title="Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))
            self.FEMB_SUB_PLOT(ax4, x, y4, title="Averaging(100 Cycles) Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))

        #fig.suptitle(fn)
        plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
        fn = fp + ".png"
        plt.savefig(fn)
        plt.close()

    def PrintPWR(self, pwr_data, fp):

        pwr_names=['BIAS','LArASIC','ColdDATA','ColdADC']
        pwr_set=[5,3,3,3.5]
        pwr_dic={'name':[],'V_set/V':[],'V_meas/V':[],'I_meas/A':[],'P_meas/W':[]}
        i=0
        total_p = 0
        for ilist in pwr_data:
            pwr_dic['name'].append(pwr_names[i])
            pwr_dic['V_set/V'].append(pwr_set[i])
            i=i+1
            pwr_dic['V_meas/V'].append(round(ilist[1],3))
            pwr_dic['I_meas/A'].append(round(ilist[2],3))
            pwr_dic['P_meas/W'].append(round(ilist[3],3))
            total_p = total_p + ilist[3]

        df=pd.DataFrame(data=pwr_dic)

        fig, ax =plt.subplots(figsize=(10,2))
        ax.axis('off')
        table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
        ax.set_title("Power Consumption = {} W".format(round(total_p,3)))
        table.set_fontsize(14)
        table.scale(1,2)
        fig.savefig(fp+".png")

    def PrintMON(self, fembs, fembs_no, nchips, mon_bgp, mon_t, mon_adcs, fp):
        f=1/(2**14)*2048 # mV
       
        for femb in fembs: 
            mon_dic={'ASIC#':[],'FE T':[],'FE BGP':[],'ADC VCMI':[],'ADC VCMO':[], 'ADC VREFP':[], 'ADC VREFN':[]}

            for i in nchips: # 8 chips per board
                
                mon_dic['ASIC#'].append(i)
                mon_dic['FE T'].append(mon_t[f'chip{i}'][0][femb])
                mon_dic['FE BGP'].append(mon_bgp[f'chip{i}'][0][femb])

                vcmi = round(mon_adcs[f'chip{i}']["VCMI"][1][0][femb]*f,1)
                vcmo = round(mon_adcs[f'chip{i}']["VCMO"][1][0][femb]*f,1)
                vrefp = round(mon_adcs[f'chip{i}']["VREFP"][1][0][femb]*f,1)
                vrefn = round(mon_adcs[f'chip{i}']["VREFN"][1][0][femb]*f,1)

                mon_dic['ADC VCMI'].append(vcmi)
                mon_dic['ADC VCMO'].append(vcmo)
                mon_dic['ADC VREFP'].append(vrefp)
                mon_dic['ADC VREFN'].append(vrefn)

            df=pd.DataFrame(data=mon_dic)

            fig, ax =plt.subplots(figsize=(10,2))
            ax.axis('off')
            table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
            ax.set_title("Monitoring path for FE-ADC (#mV)")
            table.set_fontsize(14)
            table.scale(1,2.2)
            newfp=fp+"FEMB{}_mon_meas.png".format(fembs_no[f'femb{femb}'])
            fig.savefig(newfp)

