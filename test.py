import sys
import numpy as np
import pickle
import time, datetime, random, statistics
import matplotlib.pyplot as plt
from QC_tools import QC_tools
from fpdf import FPDF
from spymemory_decode import wib_spy_dec_syn

#fp1 = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/CHK_femb1_femb2_femb3_femb4_RT_0pF_R001/data/Raw_SE_200mVBL_14_0mVfC_2_0us_0x20.bin"
#fp1 = "D:/debug_data/CHK_femb1_femb2_femb3_femb4_RT_0pF_R007/data/Raw_SE_200mVBL_14_0mVfC_2_0us_0x20.bin"
fp2 = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/data/femb1_femb2_femb3_femb4_LN_0pF_R003/MON_ADC/LArASIC_ColdADC_mon.bin"
#fp2 = "D:/debug_data/CHK_femb1_femb2_femb3_femb4_RT_0pF_R007/data/Mon_200mVBL_14_0mVfC.bin"
#save_dir = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/test/"
#save_dir = "D:/debug_data/CHK_femb1_femb2_femb3_femb4_RT_0pF_R007/plot/"
    
#with open(fp1, 'rb') as fn:
#    rawdata = pickle.load(fn)
#
#logs=rawdata[3]
#pwr_meas=rawdata[1]

with open(fp2, 'rb') as fn:
    raw = pickle.load(fn)

#print(len(raw[0]["chip0"]))
print(raw[0])
#for key,value in raw[0].items():
#    total=list(map(sum, zip(*value)))
#    avg=np.array(total)/5
#    print(key, avg)

#qc_tools = QC_tools()
##pldata = qc_tools.data_valid(rawdata)
#pldata = qc_tools.data_decode(rawdata[0])
#pldata = np.array(pldata)
#
#
#fembs=[0,1,2,3]    
#fembNo={'femb0':1,'femb1':2,'femb2':3,'femb3':4}
#fp_pwr = save_dir
#qc_tools.PrintMON(fembs, fembNo,[0,4], raw[0], raw[1], raw[2], fp_pwr)
#
#for i in fembs:
#    i=int(i)
#
#    femb_id = fembNo['femb{}'.format(i)]
#    ana = qc_tools.data_ana(pldata,i)
#    fp_data = save_dir+"FEMB{}_SE_response".format(femb_id)
#    qc_tools.FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5], fp_data)
#
#    fp_pwr = save_dir+"FEMB{}_pwr_meas".format(femb_id)
#    qc_tools.PrintPWR( pwr_meas['femb{}'.format(i)], fp_pwr)
#
#    pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
#    pdf.alias_nb_pages()
#    pdf.add_page()
#    pdf.set_auto_page_break(False,0)
#    pdf.set_font('Times', 'B', 20)
#    pdf.cell(85)
#    pdf.l_margin = pdf.l_margin*2
#    pdf.cell(30, 5, 'FEMB#{:04d} Checkout Test Report'.format(int(femb_id)), 0, 1, 'C')
#    pdf.ln(2)
#
#    pdf.set_font('Times', '', 12)
#    pdf.cell(30, 5, 'Tester: {}'.format(logs["tester"]), 0, 1)
#
#
#    pdf.cell(30, 5, 'Temperature: {}'.format(logs["env"]), 0, 0)
#    pdf.cell(80)
#    pdf.cell(30, 5, 'Input Capacitor(Cd): {}'.format(logs["toytpc"]), 0, 1)
#    pdf.cell(30, 5, 'Note: {}'.format(logs["note"][0:80]), 0, 1)
#    pdf.cell(30, 5, 'FEMB configuration: {}, {}, {}, {}, DAC=0x{:02x}'.format("200mVBL","14_0mVfC","2_0us","500pA",0x20), 0, 1)
#
#    pwr_image = fp_pwr+".png"
#    pdf.image(pwr_image,0,40,200,40)
#
#    mon_image = save_dir+"FEMB{}_mon_meas.png".format(femb_id)
#    pdf.image(mon_image,0,80,200,40)
#
#    chk_image = fp_data+".png"
#    pdf.image(chk_image,3,120,200,120)
#
#    outfile = save_dir+'CHK_femb{}.pdf'.format(femb_id)
#    pdf.output(outfile, "F")
#

