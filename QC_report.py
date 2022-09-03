import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import time
import glob
from QC_tools import QC_tools
from fpdf import FPDF


class QC_reports:

      def __init__(self, fdir):

          savedir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/"
          self.datadir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/"+fdir+"/"

          fp = self.datadir+"logs_env.bin"
          with open(fp, 'rb') as fn:
               logs = pickle.load(fn)
         
          logs["datadir"]=self.datadir
          self.logs=logs

          self.fembs = logs['femb id']
          self.savedir={}

          ##### create results dir for each FEMB #####
          for key,value in self.fembs.items():
              one_savedir = savedir+"FEMB{}_{}_{}".format(value, logs["env"], logs["toytpc"])

              n=1
              while (os.path.exists(one_savedir)):
                  if n==1:
                      one_savedir = one_savedir + "_R{:03d}".format(n)
                  else:
                      one_savedir = one_savedir[:-3] + "{:03d}".format(n)
                  n=n+1
                  if n>20:
                      raise Exception("There are more than 20 folders...")

              try:
                  os.makedirs(one_savedir)
              except OSError:
                  print ("Error to create folder %s"%one_savedir)
                  sys.exit()

              self.savedir[key]=one_savedir+"/"

              fp = self.savedir[key] + "logs_env.bin"
              with open(fp, 'wb') as fn:
                   pickle.dump(self.logs, fn)

      def CreateDIR(self, fdir):

          for key,value in self.fembs.items():
              fp = self.savedir[key] + fdir + "/"
              if not os.path.exists(fp):
                 try:
                     os.makedirs(fp)
                 except OSError:
                     print ("Error to create folder %s"%fp)
                     sys.exit()

      def GEN_PWR_PDF(self,fdir,femb_id):

          pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
          pdf.alias_nb_pages()
          pdf.add_page()
          pdf.set_auto_page_break(False,0)
          pdf.set_font('Times', 'B', 20)
          pdf.cell(85)
          pdf.l_margin = pdf.l_margin*2
          pdf.cell(30, 5, 'FEMB#{:04d} Checkout Test Report'.format(femb_id), 0, 1, 'C')
          pdf.ln(2)
          
          pdf.set_font('Times', '', 12)
          pdf.cell(30, 5, 'Tester: {}'.format(self.logs["tester"]), 0, 1)
          
          pdf.cell(30, 5, 'Temperature: {}'.format(self.logs["env"]), 0, 0)
          pdf.cell(80)
          pdf.cell(30, 5, 'Input Capacitor(Cd): {}'.format(self.logs["toytpc"]), 0, 1)
          pdf.cell(30, 5, 'Note: {}'.format(self.logs["note"][0:80]), 0, 1)
          pdf.cell(30, 5, 'FEMB configuration: {}, {}, {}, {}, DAC=0x{:02x}'.format("200mVBL","14_0mVfC","2_0us","500pA",0x20), 0, 1)
         
          pwr_images = sorted(glob.glob(fdir+"*_pwr_meas.png"), key=os.path.getmtime)
          nn=0
          for im in pwr_images:
              im_name = im.split("/")[-1][4:-13]
              pdf.set_font('Times', 'B', 14)
              if nn<3:
                 pdf.text(55, 45+45*nn, im_name)  
                 pdf.image(im,0,47+nn*45,200, 40)
              else:
                 if nn%3==0:
                    pdf.add_page()
                 pdf.text(55, 10+45*(nn-3), im_name)  
                 pdf.image(im,0,12+(nn-3)*45,200, 40)
              nn=nn+1
          
          pdf.alias_nb_pages()
          pdf.add_page()
          
          chk_images = sorted(glob.glob(fdir+"*_pulse_response.png"), key=os.path.getmtime)
          nn=0
          for im in chk_images:
              im_name = im.split("/")[-1][4:-19]
              pdf.set_font('Times', 'B', 14)
              if nn<3:
                 pdf.text(55, 10+nn*80, im_name)  
                 pdf.image(im,0,12+nn*80,200,80)
              else:
                 if nn%3==0:
                    pdf.alias_nb_pages()
                    pdf.add_page()
                 pdf.text(55, 10+(nn-3)*80, im_name)  
                 pdf.image(im,0,12+(nn-3)*80,200,80)
              nn=nn+1
          
          outfile = fdir+'report.pdf'
          pdf.output(outfile, "F")
         
      def PWR_consumption_report(self):
          
          self.CreateDIR("PWR_Meas")
          datadir = self.datadir+"PWR_Meas/"

          qc=QC_tools()
          files = sorted(glob.glob(datadir+"*.bin"), key=os.path.getmtime)  # list of data files in the dir
          for afile in files:
              with open(afile, 'rb') as fn:
                   raw = pickle.load(fn)

              rawdata = raw[0]
              pwr_meas = raw[1]

              pldata = qc.data_decode(rawdata)
              pldata = np.array(pldata)

              fname = afile.split("/")[-1][:-4]
              for key,value in self.fembs.items():
                  fp = self.savedir[key] + "PWR_Meas/" + fname + "_pwr_meas"
                  qc.PrintPWR(pwr_meas[key], fp)

                  ana = qc.data_ana(pldata,int(key[-1]))
                  fp_data = self.savedir[key] + "PWR_Meas/" + fname + "_pulse_response"
                  qc.FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5], fp_data)
 
          for key,value in self.fembs.items():
              fdir = self.savedir[key] + "PWR_Meas/"
              self.GEN_PWR_PDF(fdir, int(value))

      def PWR_cycle_report(self):

          self.CreateDIR("PWR_Cycle")
          datadir = self.datadir+"PWR_Cycle/"

          qc=QC_tools()
          files = sorted(glob.glob(datadir+"*.bin"), key=os.path.getmtime)  # list of data files in the dir
          for afile in files:
              with open(afile, 'rb') as fn:
                   raw = pickle.load(fn)

              rawdata = raw[0]
              pwr_meas = raw[1]

              pldata = qc.data_decode(rawdata)
              pldata = np.array(pldata)

              fname = afile.split("/")[-1][:-4]
              for key,value in self.fembs.items():
                  fp = self.savedir[key] + "PWR_Cycle/" + fname + "_pwr_meas"
                  qc.PrintPWR(pwr_meas[key], fp)

                  ana = qc.data_ana(pldata,int(key[-1]))
                  fp_data = self.savedir[key] + "PWR_Cycle/" + fname + "_pulse_response"
                  qc.FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5], fp_data)
 
          for key,value in self.fembs.items():
              fdir = self.savedir[key] + "PWR_Cycle/"
              self.GEN_PWR_PDF(fdir, int(value))

      def CHKPULSE(self):

          self.CreateDIR("CHK")
          datadir = self.datadir+"CHK/"

          qc=QC_tools()
          files = sorted(glob.glob(datadir+"*.bin"), key=os.path.getmtime)  # list of data files in the dir
          for afile in files:
              with open(afile, 'rb') as fn:
                   raw = pickle.load(fn)

              rawdata = raw[0]
              pwr_meas = raw[1]

              pldata = qc.data_decode(rawdata)
              pldata = np.array(pldata)

              fname = afile.split("/")[-1][:-4]
              for key,value in self.fembs.items():
                  ana = qc.data_ana(pldata,int(key[-1]))
                  fp_data = self.savedir[key] + "CHK/" + fname + "_pulse_response"
                  qc.FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5], fp_data)
         
      def FE_MON_report(self):

          self.CreateDIR("MON_FE")
          datadir = self.datadir+"MON_FE/"

          qc=QC_tools()
          fp = datadir+"LArASIC_mon.bin"
          with open(fp, 'rb') as fn:
               raw = pickle.load(fn)

          mon_BDG=raw[0]
          mon_TEMP=raw[1]
          mon_200bls=raw[2]
          mon_900bls=raw[3]

          qc=QC_tools()
          qc.PlotMon(self.fembs, mon_BDG, self.savedir, "MON_FE", "bandgap")
          qc.PlotMon(self.fembs, mon_TEMP, self.savedir, "MON_FE", "temperature")

         
         

if __name__=='__main__':
   rp = QC_reports("femb1_femb2_femb3_femb4_LN_0pF_R003")
   #rp.PWR_consumption_report()
   #rp.PWR_cycle_report()
   #rp.CHKPULSE()
   rp.FE_MON_report()

                   
               
              
