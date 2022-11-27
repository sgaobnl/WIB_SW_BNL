import sys
sys.path.insert(1, '../')
import pandas as pd
import numpy as np
from spymemory_decode import wib_spy_dec_syn


class Tools:
   def LoadMap(self, femb_no):
   
       if femb_no in [1,2,3]:
          filename = "femb_1_2_3_map.csv"
   
       if femb_no==4:
          filename = "femb_4_map.csv"
   
       if femb_no in range(5,9):
          filename = "femb_5_8_map.csv"
   
       if femb_no==9:
          filename = "femb_9_map.csv"
   
       if femb_no in range(10,13):
          filename = "femb_10_11_12_map.csv"
   
       df = pd.read_csv(r'./channel_maps/'+filename)
       return df
   
   def FindStrips(self, mapdf, femb_no, chan):
     
       startstrip_1=0
       startstrip_2=0
       startstrip_3=0
   
       if femb_no in [2,3]:
          startstrip_2 = (femb_no-1)*32 
          startstrip_3 = (femb_no-1)*96
   
       if femb_no in range(6,9):
          startstrip_1 = (femb_no-5)*64 
          startstrip_2 = (femb_no-5)*64
   
       if femb_no in [11,12]:
          startstrip_1 = (femb_no-10)*32 
          startstrip_3 = (femb_no-10)*96
   
       plane = mapdf["Plane"][chan] 
       if plane==1:
          strip = mapdf["Strip"][chan] + startstrip_1
       if plane==2:
          strip = mapdf["Strip"][chan] + startstrip_2
       if plane==3:
          strip = mapdf["Strip"][chan] + startstrip_3
   
       return plane,strip

   def data_ana(self, rawdata, nevent=-1, nwibs=3):
       ntotal = len(rawdata)
       if nevent==-1:
          nevent = ntotal

       ch_data = []
       for iev in range(nevent):
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
   
             for iword in range(nwords):
                 ff0.append(dec_data[0][iword]["FEMB0_2"])
                 ff1.append(dec_data[0][iword]["FEMB1_3"])
                 ff2.append(dec_data[1][iword]["FEMB0_2"])
                 ff3.append(dec_data[1][iword]["FEMB1_3"])
   
             ff0 = np.array(list(zip(*ff0)))
             ff1 = np.array(list(zip(*ff1)))
             ff2 = np.array(list(zip(*ff2)))
             ff3 = np.array(list(zip(*ff3)))
   
             awib_data = np.concatenate((ff0, ff1, ff2, ff3), axis=0) 

             if iwib==0: 
                ev_data = awib_data 
             else:
                ev_data = np.concatenate((ev_data, awib_data), axis=0)
     
           ch_data.append(ev_data)

       ch_data = np.array(ch_data)
       return ch_data
 
