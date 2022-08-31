import sys
from QC_runs import QC_Runs
import argparse
import time

ag = argparse.ArgumentParser()
ag.add_argument("fembs", help="a list of femb slots number", type=int, nargs='+')
ag.add_argument("-s", "--save", help="number of pulses to be saved", type=int, default=1)
ag.add_argument("-t", "--task", help="which QC tasks to be performed", type=int, choices=range(1,13),  nargs='+', default=1)
args = ag.parse_args()

fembs = args.fembs
sampleN = args.save
tasks = args.task

qc=QC_Runs(fembs, sampleN)
qc.pwr_fembs('on')

for tm in tasks:
    print("start tm=",tm)
    if tm==1:
       qc.pwr_consumption()

    if tm==2:
       qc.pwr_cycle()
       
    if tm==3:
       qc.femb_leakage_cur()
       
    if tm==4:
       qc.femb_chk_pulse()

    if tm==5:
       qc.femb_rms()

    if tm==6:
       qc.femb_CALI_1()

    if tm==7:
       qc.femb_CALI_2()

    if tm==8:
       qc.femb_CALI_3()

    if tm==9:
       qc.femb_CALI_4()

    if tm==10:
       qc.femb_MON_1()

    if tm==11:
       qc.femb_MON_2()

    if tm==12:
       qc.femb_MON_3()

    time.sleep(1)

qc.pwr_fembs('off')
