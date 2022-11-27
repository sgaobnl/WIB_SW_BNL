::cd "D:\GitHub\WIB_SW_BNL\"
::python .\chkout_wibs.py 0 1 2 3 save 1
::
::cd "D:\GitHub\WIB_SW_BNL\"
::call test_runs.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_diff.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_sdcen.bat
cd "D:\GitHub\WIB_SW_BNL\"
call test_runs_adc_dben.bat
