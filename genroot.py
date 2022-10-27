import pickle
from spymemory_decode import wib_spy_dec_syn
import ROOT
from ROOT import TFile, TTree, addressof
from array import array
import numpy as np

def genroot(fp):

    with open(fp, 'rb') as fn:
        raw = pickle.load(fn)
    
    rawdata = raw[0]
    pwr_meas = raw[1]
  
    f = TFile('output.root', 'RECREATE' )
    tree = TTree('T', 'FEMBs')

    nevents = len(rawdata)
    nwibs = len(rawdata[0])
    print("nevent: ", nevents)
    print("nwibs:  ", nwibs)

    femb0 = np.zeros((128,2111))
    femb1 = np.zeros((128,2111))
    femb2 = np.zeros((128,2111))
    femb3 = np.zeros((128,2111))
    femb4 = np.zeros((128,2111))
    femb5 = np.zeros((128,2111))
    femb6 = np.zeros((128,2111))
    femb7 = np.zeros((128,2111))
    
    tree.Branch('femb0', addressof(femb0), 'femb0[128][2111]/D')
    tree.Branch('femb1', addressof(femb1), 'femb1[128][2111]/D')
    tree.Branch('femb2', addressof(femb2), 'femb2[128][2111]/D')
    tree.Branch('femb3', addressof(femb3), 'femb3[128][2111]/D')
    tree.Branch('femb4', addressof(femb4), 'femb4[128][2111]/D')
    tree.Branch('femb5', addressof(femb5), 'femb5[128][2111]/D')
    tree.Branch('femb6', addressof(femb6), 'femb6[128][2111]/D')
    tree.Branch('femb7', addressof(femb7), 'femb7[128][2111]/D')

    maxwords=0
    for iev in range(nevents):
        for iwib in range(nwibs):
          wibdata = rawdata[iev][iwib]
          ip = wibdata[0]
          buf0 = wibdata[1][0]
          buf1 = wibdata[1][1]
          trigmode = "HW"
          buf_end_addr = wibdata[2]
          trigger_rec_ticks = wibdata[3]
          dec_data = wib_spy_dec_syn(buf0, buf1, trigmode, buf_end_addr, trigger_rec_ticks)

          nwords = len(dec_data[0])
          ff0=[]
          ff1=[]
          ff2=[]
          ff3=[]
          if nwords>maxwords:
             maxwords=nwords
       
          for iword in range(nwords):       
              ff0.append(dec_data[0][iword]["FEMB0_2"])
              ff1.append(dec_data[0][iword]["FEMB1_3"])
              ff2.append(dec_data[1][iword]["FEMB0_2"])
              ff3.append(dec_data[1][iword]["FEMB1_3"])    

          if iwib==0:
            femb0 = list(zip(*ff0))
            femb1 = list(zip(*ff1))
            femb2 = list(zip(*ff2))
            femb3 = list(zip(*ff3))

            femb0 = np.array(femb0,dtype=int)
            femb1 = np.array(femb1,dtype=int)
            femb2 = np.array(femb2,dtype=int)
            femb3 = np.array(femb3,dtype=int)
          else:
            femb4 = list(zip(*ff0))
            femb5 = list(zip(*ff1))
            femb6 = list(zip(*ff2))
            femb7 = list(zip(*ff3))
          
            femb4 = np.array(femb4,dtype=int)
            femb5 = np.array(femb5,dtype=int)
            femb6 = np.array(femb6,dtype=int)
            femb7 = np.array(femb7,dtype=int)
        tree.Fill()

    f.Write()
    f.Close()
   
    print(femb0[0]) 
file = "data/Raw_29_09_2022_12_37_40.bin"
genroot(file)
