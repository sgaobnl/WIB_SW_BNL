python .\top_femb_powering.py on on on on LN2_BIASOFF_40V
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_40V

echo noise study
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_40V

echo noise study
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_40V

python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0   LN2_BIASOFF_40V

::                                                     
echo sdf = 1                                        
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 1 0 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 1 0 0   LN2_BIASOFF_40V
                                                   
echo leak currents                                
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 0   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 1   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 1   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 1   LN2_BIASOFF_40V
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 1   LN2_BIASOFF_40V
::                                                        
::echo pulse response
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_40V
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_40V

python .\top_femb_powering.py off off off off  LN2_BIASOFF_40V
