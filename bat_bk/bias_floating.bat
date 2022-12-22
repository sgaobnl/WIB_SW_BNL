echo noise study
python .\crp5a_run01.py 0 1 2 3 BIAS_FLOATING

::echo noise study
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   BIAS_FLOATING
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   BIAS_FLOATING
::                                                     

