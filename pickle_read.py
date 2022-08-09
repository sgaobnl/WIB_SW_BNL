import pickle

fp = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/new_qc_data/results/FEMB_femb0_femb1_femb2_femb3_RT__R001_03/rms_femb3_200mVBL_14_0mVfC_0_5us.bin"
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)

for log in logs:
    print (log)
    print(logs[log])

#print(len(logs['D:/IO_1826_1B/QC/FEMB346_LN_150pF/PWR/power_cycle2_CHK_response_SE.h5'][4][0]))
