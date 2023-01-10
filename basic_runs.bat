python .\top_femb_powering.py on on on on Tabel_2_BIASOFF_5nA_fixed
python .\crp5a_run01.py 0 1 2 3 Tabel_2_BIASOFF_5nA_fixed
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0  Tabel_2_BIASOFF_5nA_fixed
python .\top_femb_powering.py off off off off   Tabel_2_BIASOFF_5nA_fixed

::::python .\crp5a_chk_femon.py 0 1 2 3   Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_run01.py 0 1 2 3 Post_Warmup_fixed_off_BIASOFF
::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0  Post_Warmup_fixed_off_BIASOFF  
::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0  Post_Warmup_fixed_off_BIASOFF 
::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0  Post_Warmup_fixed_off_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0  Post_Warmup_fixed_off_BIASOFF
::python .\top_femb_powering.py off off off off   Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0  Post_Warmup_fixed_off_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0  Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0  Post_Warmup_fixed_off_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  Post_Warmup_fixed_off_BIASOFF
::python .\chkout_wibs.py 0 1 2 3 save 1   Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_chk_femon.py 0 1 2 3   Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_run01.py 0 1 2 3 Post_Warmup_fixed_off_BIASOFF
::::::python .\top_femb_powering.py off off off off   Post_Warmup_fixed_off_BIASOFF
::::::python .\top_femb_powering.py on on on on LN2_Trig_Bias_OFF
::python .\crp5a_run01_ext_trig.py 0 1 2 3   Post_Warmup_fixed_Trig_BIASOFF
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  Post_Warmup_fixed_Trig_BIASOFF  
::
::python .\crp5a_chk_femon.py 0 1 2 3   Post_Warmup_fixed_2_BIASOFF
::python .\crp5a_run01.py 0 1 2 3 Post_Warmup_fixed_off_BIASOFF
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0  Post_Warmup_fixed_2_BIASOFF  
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0  Post_Warmup_fixed_2_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0  Post_Warmup_fixed_2_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0  Post_Warmup_fixed_2_BIASOFF
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0  Post_Warmup_fixed_2_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0  Post_Warmup_fixed_2_BIASOFF
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0  Post_Warmup_fixed_2_BIASOFF 
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  Post_Warmup_fixed_2_BIASOFF
::python .\chkout_wibs.py 0 1 2 3 save 1   Post_Warmup_fixed_2_BIASOFF
::python .\crp5a_chk_femon.py 0 1 2 3   Post_Warmup_fixed_2_BIASOFF
::python .\crp5a_run01.py 0 1 2 3 Post_Warmup_fixed_2_BIASOFF
::
::python .\crp5a_run01_ext_trig.py 0 1 2 3   Post_Warmup_fixed_Trig2_BIASOFF
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::python .\crp5a_run02_ext_trig.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  Post_Warmup_fixed_Trig2_BIASOFF  
::
::python .\top_femb_powering.py off off off off   Post_Warmup_fixed_Trig2_BIASOFF

::python .\top_femb_powering.py off off off off  LN2_Trig_Bias_OFF  
