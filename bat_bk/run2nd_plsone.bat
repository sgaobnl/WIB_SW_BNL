::python .\top_femb_powering.py on on on on LN2_BIASON_Copper_Floating2

python .\crp5a_run01_plsone.py 0 1 2 3 LN2_FEMB1_CHIP7_CH15
::python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::python .\chkout_wibs.py 0 1 2 3 save 1 LN2_BIASON_Copper_CHOKE
::python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASON_Copper_CHOKE

::echo noise study
::python .\crp5a_run01.py 0 1 2 3 LN2_BIASON_Copper_Floating2
::
::echo noise study
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASON_Copper_Floating2
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASON_Copper_Floating2

::echo sdf = 1                                        
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::                                                   
::echo leak currents                                
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::
::echo pulse response
::python .\crp5a_run04.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::
::echo noise study
::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE
::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE
::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::
::python .\top_femb_powering.py off off off off  LN2_BIASON_Copper_CHOKE
::::::
::::
::::
::::
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::                                                     
::::::echo sdf = 1                                        
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::                                                   
::::::echo leak currents                                
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::::::                                                        
::::::
::::::echo pulse response
::::::python .\crp5a_run04.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::
::::::echo noise study
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 0 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 1 1 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::
::::::
::::::echo noise study
::::::python .\crp5a_run07.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::
::::::echo noise study
::::::python .\crp5a_run08.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run08.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run08.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run08.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  LN2_BIASON_Copper_CHOKE
::::::
::::::
::::::
::::::echo noise study
::::::python .\crp5a_run10.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::
::::::echo noise study
::::::python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run11.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run11.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0 LN2_BIASON_Copper_CHOKE
::::::
::::::echo noise study
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 0 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 1 0 0 0   LN2_BIASON_Copper_CHOKE
::::::                                                     
::::::echo sdf = 1                                        
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 1 0 0   LN2_BIASON_Copper_CHOKE
::::::                                                   
::::::echo leak currents                                
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 0   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 1   LN2_BIASON_Copper_CHOKE
::::::
::::::
::::::
::::::echo calibration                                       
::::::python .\crp5a_run01.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run03.py 0 1 2 3 30 1 0 0 0 0 0 0 0 0 0  LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 0 0 0 0 0 0  LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run03.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run03.py 0 1 2 3 30 1 0 0 0 0 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 0 1 0 0 0 0  LN2_BIASON_Copper_CHOKE 
::::::                                                        
::::::python .\crp5a_run03.py 0 1 2 3 30 1 0 0 0 1 1 1 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 1 1 1 0 0 0  LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run03.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 1  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 1  LN2_BIASON_Copper_CHOKE 
::::::                                                        
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 0 1 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 1 0 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run03.py 0 1 2 3 30 1 1 1 1 1 1 0 0 0 0  LN2_BIASON_Copper_CHOKE  
::::
::::::echo calibration
::::::python .\crp5a_run04.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 0 0 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 0 1 0 0 0 0 LN2_BIASON_Copper_CHOKE 
::::::
::::::python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 1 LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 1 LN2_BIASON_Copper_CHOKE 
::::::
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 0 1 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 1 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE  
::::::python .\crp5a_run06.py 0 1 2 3 30 1 1 1 1 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE  
::::::
::::::
::::::::echo calibration
::::::::python .\crp5a_run07.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::::python .\crp5a_run09.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::::python .\crp5a_run09.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::::
::::::::
::::::::
::::::::echo calibration
::::::::python .\crp5a_run10.py 0 1 2 3 LN2_BIASON_Copper_CHOKE
::::::::python .\crp5a_run12.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::::::python .\crp5a_run12.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 LN2_BIASON_Copper_CHOKE
::::