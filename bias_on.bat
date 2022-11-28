echo noise study
python .\crp5a_run01.py 0 1 2 3 BIAS_ON

::echo noise study
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   BIAS_ON
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   BIAS_ON
::                                                     

