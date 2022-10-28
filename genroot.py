import pickle
from spymemory_decode import wib_spy_dec_syn
import ROOT
from ROOT import TFile, TTree, addressof
from array import array
import numpy as np
import uproot
import matplotlib.pyplot as plt
from tools import Tools

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
    
    #tree.Branch('femb0', addressof(femb0), 'femb0[128][2111]/D')
    tree.Branch('femb0', femb0, 'femb0[128][2111]/D')
    tree.Branch('femb1', femb1, 'femb1[128][2111]/D')
    tree.Branch('femb2', femb2, 'femb2[128][2111]/D')
    tree.Branch('femb3', femb3, 'femb3[128][2111]/D')
    tree.Branch('femb4', femb4, 'femb4[128][2111]/D')
    tree.Branch('femb5', femb5, 'femb5[128][2111]/D')
    tree.Branch('femb6', femb6, 'femb6[128][2111]/D')
    tree.Branch('femb7', femb7, 'femb7[128][2111]/D')

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

          ff0 = list(zip(*ff0))
          ff1 = list(zip(*ff1))
          ff2 = list(zip(*ff2))
          ff3 = list(zip(*ff3))

          if iwib==0:
            for ich in range(128):
                femb0[ich] = ff0[ich]
                femb1[ich] = ff1[ich]
                femb2[ich] = ff2[ich]
                femb3[ich] = ff3[ich]
          if iwib==1:
            for ich in range(128):
                femb4[ich] = ff0[ich]
                femb5[ich] = ff1[ich]
                femb6[ich] = ff2[ich]
                femb7[ich] = ff3[ich]

        tree.Fill()

    f.Write()
    f.Close()

def Loadroot(rootfile):
    rf = uproot.open(rootfile)
    tree = rf["T"]
    nfemb = len(tree.keys())
    print("nfemb:  ",nfemb)

    femb=[]
    for i in range(nfemb):
       arr = tree["femb%d"%i].array(library="np")
       femb.append(arr)
      
    femb = np.array(femb)   # femb_no, event_no, chan, tick
    return femb

def MapStrips(data):

    nfemb = len(data)
    uplane=[[]]*476
    vplane=[[]]*476
    xplane=[[]]*584

    smap = Tools()
    for i in range(nfemb):
        df=smap.LoadMap(i+1)
        for ich in range(128):
            plane,strip = smap.FindStrips(df, i+1, ich) 
            if plane==1:
               uplane[strip-1]=data[i,:,ich,:]
            if plane==2:
               vplane[strip-1]=data[i,:,ich,:]
            if plane==3:
               xplane[strip-1]=data[i,:,ich,:]
   
def exampleplot(data):
    nticks = len(data[0][0][0])
    plt.plot(range(nticks),data[0][0][0])
    plt.show()
    

if __name__=='__main__':    
   
  f = "../new_qc_data/Raw_29_09_2022_12_37_40.bin"
  #genroot(f)
  data = Loadroot("output.root")
  #exampleplot(data)
  MapStrips(data)
