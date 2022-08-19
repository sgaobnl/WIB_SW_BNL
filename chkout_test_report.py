import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import time
from data_organization import data_organization 
from fpdf import FPDF

class QC_report:
    def __init__(self, fname, save_dir=''):

        folder = fname
        fdir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/"   # data folder
        self.datafdir = fdir+folder+'/'
        self.save_dir = '/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/'+save_dir
        self.fname = fname
   
        self.sncs = ["900mVBL", "200mVBL"]
        self.sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        self.sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

        fp = self.datafdir + 'Raw_CALI_SE_200mVBL_14_0mVfC_2_0us_0x00.bin'
        with open(fp, 'rb') as fn:
             raw = pickle.load(fn)
        self.logs=raw[3]

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

    def CreateFD(self): 
        #save_dir='D:/debug_data/cleaned_data/'+fdir
        save_dir='/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/'+self.fname
    
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

        self.save_dir = save_dir   

    def Clean_data(self):
    
        fb = data_organization(self.save_dir)
    
        sncs = self.sncs
        sgs = self.sgs
        sts = self.sts
    
        for snci in sncs:
            for sgi in sgs:
                for sti in sts:
                    se_rms_file = "Raw_RMS_SE_{}_{}_{}.bin".format(snci, sgi, sti)
                    datafile = self.datafdir + se_rms_file
                    outfile = "SE_{}_{}_{}".format(snci, sgi, sti)
    
                    fb.GetRMS(datafile,outfile)
    
                    if sgi=="14_0mVfC":
                        diff_rms_file = "Raw_RMS_DIFF_{}_{}_{}.bin".format(snci, sgi, sti)
                        datafile = self.datafdir + diff_rms_file
                        outfile = "DIFF_{}_{}_{}".format(snci, sgi, sti)
                        fb.GetRMS(datafile,outfile)
    
                    if sti=="2_0us":
                        dac_file = "Raw_CALI_SE_{}_{}_{}.bin".format(snci, sgi, sti)
                        datafile = self.datafdir + diff_rms_file
                        outfile = "SE_{}_{}_{}".format(snci, sgi, sti)
                        fb.GetGain(self.datafdir,outfile)

    def GenPDF(self, fdir, femb_id, snci, sgi, sti):
        
        pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(False,0)
        pdf.set_font('Times', 'B', 20)
        pdf.cell(85)
        pdf.l_margin = pdf.l_margin*2
        pdf.cell(30, 5, 'FEMB#{:04d} Checkout Test Report'.format(int(femb_id)), 0, 1, 'C')
        pdf.ln(2)

        pdf.set_font('Times', '', 12)
        pdf.cell(30, 5, 'Tester: {}'.format(self.logs["tester"]), 0, 1)
    
#        pdf.cell(30, 5, 'WIB_TCP_Version: 0x{:02x}'.format(result_dict["WIB_TCP_FW_ver"]), 0, 0)
#        pdf.cell(80)
#        pdf.cell(30, 5, 'WIB_UDP_Version: 0x{:02x}'.format(result_dict["WIB_UDP_FW_ver"]), 0, 1)
    
        pdf.cell(30, 5, 'Temperature: {}'.format(self.logs["env"]), 0, 0)
        pdf.cell(80)
        pdf.cell(30, 5, 'Input Capacitor(Cd): {}'.format(self.logs["toytpc"]), 0, 1)
#        pdf.cell(30, 5, 'Note: {}'.format(self.logs["note"][0:80]), 0, 1)
        pdf.cell(30, 5, 'FEMB configuration: {}, {}, {}'.format(snci, sgi, sti), 0, 1)

        rms_image = self.save_dir + '/plots/' + 'rms_femb{}_SE_{}_{}_{}.png'.format(femb_id, snci, sgi, sti)
        gain_image = self.save_dir + '/plots/' + 'cali_gain_femb{}_SE_{}_{}_{}.png'.format(femb_id, snci, sgi, "2_0us")
        ENC_image = self.save_dir + '/plots/' + 'cali_ENC_femb{}_SE_{}_{}_{}.png'.format(femb_id, snci, sgi, sti)

        pdf.image(rms_image,3,35,200,80)
        pdf.image(gain_image,3,115,200,80)
        pdf.image(ENC_image,3,195,200,80)
        outfile = fdir+'femb{}_SE_{}_{}_{}.pdf'.format(femb_id, snci, sgi, sti)
        pdf.output(outfile, "F")
               
    def GenENC(self, fdir, femb_id, snci, sgi, sti):

        dac_v = self.dac_v[sgi]/1000.0
        CC=self.CC
        e=self.e
      
        datfdir = fdir+"/data/"
 
        fp1 = datfdir+"gain_femb{}_SE_{}_{}_{}.bin".format(femb_id, snci, sgi, "2_0us") 
        with open(fp1, 'rb') as fn:
             gain = pickle.load(fn)
                
        fp2 = datfdir+"rms_femb{}_SE_{}_{}_{}.bin".format(femb_id, snci, sgi, sti) 
        with open(fp2, 'rb') as fn:
             rms = pickle.load(fn)

        rms = rms['RMS']

        if len(rms)!=len(gain):
           print("RMS and Gain don't match !!!", len(rms), len(gain))
           sys.exit()

        enc=[]
        for i in range(128):
            tmp_enc = rms[i]/(gain[i]/dac_v)*CC/e
            enc.append(tmp_enc)
                
        fp3 = datfdir+"enc_femb{}_SE_{}_{}_{}.bin".format(femb_id, snci, sgi, sti) 
        with open(fp3, 'wb') as fn:
             pickle.dump(enc, fn)

        pltfdir = fdir+"/plots/"

        fig, ax =plt.subplots(figsize=(8,4))
        xx=range(128)
        ax.scatter(xx,enc,marker='.')
        ax.set_xlabel('chan')
        ax.set_ylabel('ENC')
        ax.set_title('FEMB{} SE_{}_{}_{}'.format(femb_id, snci, sgi, sti))
        ax.text(.8,.9,'gain@2us',transform=ax.transAxes,size=15)
        fig.savefig(pltfdir+"cali_ENC_femb{}_SE_{}_{}_{}.png".format(femb_id, snci, sgi, sti))
        plt.close()

    def Gen_Report(self):
        
        sncs = self.sncs
        sgs = self.sgs
        sts = self.sts

        save_dir = self.save_dir+'/reports/'
        if not os.path.exists(save_dir):
           try:
               os.makedirs(save_dir)
           except OSError:
               print ("Error to create folder %s"%save_dir)
               sys.exit()

        femb_no = []
        for key,value in self.logs['femb id'].items():
            femb_no.append(value) # assume the id is stored in increasing order

        for snci in sncs:
            for sgi in sgs:
                for sti in sts:
                    for femb_id in femb_no:
                        if sti=="2_0us":
                           self.GenPDF(save_dir, femb_id, snci, sgi, sti)
                        else:
                           self.GenENC(self.save_dir, femb_id, snci, sgi, sti)
                           self.GenPDF(save_dir, femb_id, snci, sgi, sti)
 

qc = QC_report("femb1_femb2_femb3_femb4_RT_0pF_R001", save_dir="femb1_femb2_femb3_femb4_RT_0pF_R001")
#qc = QC_report("femb1_femb2_femb3_femb4_RT_0pF_R001")
#qc.CreateFD() 
#qc.Clean_data()
qc.Gen_Report()
