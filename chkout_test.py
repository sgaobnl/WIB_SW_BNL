from wib_cfgs import WIB_CFGS
import time
import sys
import numpy as np
import pickle
import copy
import os
import time, datetime, random, statistics
from QC_tools import QC_tools
from fpdf import FPDF


####### Input FEMB slots #######


if len(sys.argv) < 2:
    print('Please specify at least one FEMB # to test')
    print('Usage: python wib.py 0')
    exit()

if 'save' in sys.argv:
    save = True
    for i in range(len(sys.argv)):
        if sys.argv[i] == 'save':
            pos = i
            break
    sample_N = int(sys.argv[pos+1] )
    sys.argv.remove('save')
else:
    save = False
    sample_N = 1

fembs = [int(a) for a in sys.argv[1:pos]]

####### Input test information #######

tester=input("please input your name:  ")
logs['tester']=tester

env_cs = input("Test is performed at cold(LN2) (Y/N)? : ")
if ("Y" in env_cs) or ("y" in env_cs):
    env = "LN"
else:
    env = "RT"
logs['env']=env

ToyTPC_en = input("ToyTPC at FE inputs (Y/N) : ")
if ("Y" in ToyTPC_en) or ("y" in ToyTPC_en):
    toytpc = "150pF"
else:
    toytpc = "0pF"
logs['toytpc']=toytpc

note = input("A short note (<200 letters):")
logs['note']=note

fembNo={}
for i in fembs:
    fembNo['femb{}'.format(i)]=input("FEMB{} ID: ".format(i))

logs['femb id']=fembNo

####### Create data save directory #######

save_dir = "D:/debug_data/"
for key,femb_no in fembNo.items():
    save_dir = save_dir + "femb{}_".format(femb_no)

save_dir = save_dir+"{}_{}".format(env,toytpc)

n=1
while (os.path.exists(save_dir)):
    if n==1:
        save_dir = save_dir + "_R{:03d}".format(n)
    else:
        save_dir = save_dir[:-3] + "{:03d}".format(n)
    n=n+1
    if n>20:
        raise Exception("There are more than 20 folders...")

try:
    os.makedirs(save_dir)
except OSError:
    print ("Error to create folder %s"%save_dir)
    sys.exit()

save_dir = save_dir+"/"

fp = save_dir + "logs_env.bin"
with open(fp, 'wb') as fn:
     pickle.dump(logs, fn)

datadir = save_dir+"data/"
try:
    os.makedirs(datadir)
except OSError:
    print ("Error to create folder %s"%datadir)
    sys.exit()

plotdir = save_dir+"plot/"
try:
    os.makedirs(plotdir)
except OSError:
    print ("Error to create folder %s"%plotdir)
    sys.exit()


####### Power and configue FEMBs #######

chk = WIB_CFGS()

chk.wib_init()

chk.femb_vol_set(vfe=3.0, vcd=3.0, vadc=3.5)
chk.femb_powering(fembs)
pwr_meas = chk.get_sensors()

chk.femb_cd_rst()

snc = 1 # 200 mV
sg0 = 0
sg1 = 0 # 14mV/fC
st0 = 1 
st1 = 1 # 2us 

cfg_paras_rec = []
for femb_id in fembs:
    chk.adcs_paras = [ # c_id, data_fmt(0x89), diff_en(0x84), sdc_en(0x80), vrefp, vrefn, vcmo, vcmi, autocali
                        [0x4, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x5, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x6, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x7, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x8, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0x9, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0xA, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                        [0xB, 0x08, 0, 0, 0xDF, 0x33, 0x89, 0x67, 1],
                      ]
    chk.set_fe_board(sts=1, snc=snc, sg0=sg0, sg1=sg1, st0=st0, st1=st1, swdac=1, dac=0x20 )
    adac_pls_en = 1 
    cfg_paras_rec.append( (femb_id, copy.deepcopy(chk.adcs_paras), copy.deepcopy(chk.regs_int8), adac_pls_en) )
    chk.femb_cfg(femb_id, adac_pls_en )

####### Take data #######
time.sleep(0.5)
pwr_meas = chk.get_sensors()
rawdata = chk.wib_acquire_data(fembs=fembs, num_samples=sample_N) #returns lsti of size 1

####### Save data #######
if save:
    fp = datadir + "Raw_SE_{}_{}_{}_0x{:02x}.bin".format("200mVBL","14_0mVfC","2_0us",0x20)

    with open(fp, 'wb') as fn:
        pickle.dump( [rawdata, pwr_meas, cfg_paras_rec, logs], fn)

####### Power off FEMBs #######
print("Turning off FEMBs")
chk.femb_powering([])

####### Generate report #######
pldata = QC_tools.data_valid(rawdata)

pldata = np.array(pldata,dtype=object)
nfemb = len(pldata[0])//128

if nfemb != len(logs['femb id']):
    print("The number of FEMBs in data is not equal to that in the logs! Exiting...")
    sys.exit()

for i in range(nfemb):

    femb_id = fembNo['femb{}'.format(i)]
    ana = QC_tools.data_ana(pldata,i)
    fp = plotdir+"FEMB{}_SE_response".format(femb_id)
    QC_tools.FEMB_CHK_PLOT(ana[0], ana[1], ana[2], ana[3], ana[4], ana[5], fp):

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
    pdf.cell(30, 5, 'Tester: {}'.format(logs["tester"]), 0, 1)


    pdf.cell(30, 5, 'Temperature: {}'.format(logs["env"]), 0, 0)
    pdf.cell(80)
    pdf.cell(30, 5, 'Input Capacitor(Cd): {}'.format(logs["toytpc"]), 0, 1)
    pdf.cell(30, 5, 'Note: {}'.format(logs["note"][0:80]), 0, 1)
    pdf.cell(30, 5, 'FEMB configuration: {}, {}, {}, {}, DAC=0x{:02x}'.format("200mVBL","14_0mVfC","2_0us","500pA",0x20), 0, 1)

    chk_image = fp+".png"

    pdf.image(chk_image,3,35,200,80)
    outfile = save_dir+'CHK_femb{}.pdf'.format(femb_id)
    pdf.output(outfile, "F")

     
    
     





