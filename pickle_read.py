import pickle
import sys

fp = sys.argv[1]
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)
print (logs)
#for log in logs:
#    print (log)
    #print(logs[log])

#print(len(logs['D:/IO_1826_1B/QC/FEMB346_LN_150pF/PWR/power_cycle2_CHK_response_SE.h5'][4][0]))
