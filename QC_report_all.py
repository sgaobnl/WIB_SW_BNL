import sys
from QC_report import QC_reports
import argparse
import time

ag = argparse.ArgumentParser()
ag.add_argument("folder", help="data folder", type=str)
ag.add_argument("task", help="a list of tasks to be analyzed", type=int, choices=range(1,13), nargs='+')
ag.add_argument("-n", "--fembs", help="a list of fembs to be analyzed", type=int, choices=range(0,4), nargs='+')
args = ag.parse_args()

fdir = args.folder
tasks = args.task
fembs = args.fembs

rp = QC_reports(fdir, fembs)

tt={}

for tm in tasks:
    t1=time.time()
    print("start tm=",tm)
    if tm==1:
       rp.PWR_consumption_report()

    if tm==2:
       rp.PWR_cycle_report()
       
    if tm==3:
       rp.CHKPULSE("Leakage_Current")
       
    if tm==4:
       rp.CHKPULSE("CHK")

    if tm==5:
       rp.RMS_report()

    if tm==6:
       rp.CALI_report()

    if tm==10:
       rp.FE_MON_report()

    if tm==11:
       rp.FE_DAC_MON_report()

    if tm==12:
       rp.ColdADC_DAC_MON_report()

    t2=time.time()
    tt[tm]=t2-t1
    time.sleep(1)

print(tt)
