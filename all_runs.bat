cd "D:\GitHub\WIB_SW_BNL\"
python .\top_femb_powering.py off off off off RTTEST
python .\top_femb_powering.py on on on on RTTEST
python .\crp5a_chk_femon.py 0 1 2 3 RTTEST
python .\chkout_wibs.py 0 1 2 3 save 1 RTTEST
python .\crp5a_chk_femon.py 0 1 2 3 RTTEST

cd "D:\GitHub\WIB_SW_BNL\"
call test_runs.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_diff.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_sdcen.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_dben.bat
python .\top_femb_powering.py off off off off RTTEST
