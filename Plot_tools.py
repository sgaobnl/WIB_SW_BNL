import pickle
import matplotlib.pyplot as plt
import numpy as np


def ENC_sts(fdir,savedir):
  
    sncs = ["900mVBL", "200mVBL"]
    sgs = "14_0mVfC"
    sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]

    xx = range(len(sts))
    fig,ax = plt.subplots(figsize=(6,4))
    for snci in sncs:
        fp1 = fdir+"CALI/Gain_{}_{}_2_0us.bin".format(snci, sgs)
        with open(fp1, 'rb') as fn:
             raw = pickle.load(fn)
        gain_list = np.array(raw[0])

        avg_enc=[]
        avg_err=[]
        for sti in sts:
            fp2 = fdir+"RMS/RMS_{}_{}_{}.bin".format(snci, sgs, sti)
            with open(fp2, 'rb') as fn:
                 raw = pickle.load(fn)
            rms_list=np.array(raw[1])

            enc_list = rms_list*gain_list
            tmp_avg = np.mean(enc_list)
            tmp_err = np.std(enc_list)
 
            avg_enc.append(tmp_avg)
            avg_err.append(tmp_err)

        ax.errorbar(xx, avg_enc, yerr=avg_err, label="{}".format(snci))


    plt.setp(ax, xticks=xx, xticklabels=sts)
    ax.set_ylabel('ENC')
    #ax.set_title('SE@{}'.format(femb_id, sgs))
    ax.text(.2,.9,'gain@2us',transform=ax.transAxes,size=13)
    ax.set_ylim([500,1200])
    ax.legend(loc="upper right")
    fig.savefig(savedir+"ENC_SE_shaping_time_RT.png")
    plt.close()
        

datadir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/FEMB104_RT_150pF/" 
savedir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/" 
ENC_sts(datadir, savedir)
