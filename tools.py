import pandas as pd

def LoadMap(femb_no):

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

    df = pd.read_csv(r'channel_maps/'+filename)
    return df

def FindStrips(mapdf, femb_no, chan):
  
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


