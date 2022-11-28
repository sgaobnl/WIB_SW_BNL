cd "D:\GitHub\WIB_SW_BNL\"
python .\top_femb_powering.py off off off off RTRUN2
python .\top_femb_powering.py on on on on RTRUN2
python .\crp5a_chk_femon.py 0 1 2 3 RTRUN2
python .\chkout_wibs.py 0 1 2 3 save 1 RTRUN2
python .\crp5a_chk_femon.py 0 1 2 3 RTRUN2

cd "D:\GitHub\WIB_SW_BNL\"
call test_runs.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_diff.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_sdcen.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_dben.bat
