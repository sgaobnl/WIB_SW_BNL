echo noise study
python .\crp5a_run10.py 0 1 2 3 RTTEST

echo noise study
python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 RTTEST
python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 RTTEST
python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 RTTEST
python .\crp5a_run11.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0 RTTEST

echo calibration
python .\crp5a_run10.py 0 1 2 3 RTTEST
python .\crp5a_run12.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0 RTTEST
python .\crp5a_run12.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 RTTEST

