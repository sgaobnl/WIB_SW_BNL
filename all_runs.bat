cd "D:\GitHub\WIB_SW_BNL\"
python .\top_femb_powering.py off off off off
python .\top_femb_powering.py on on on on
python .\crp5a_chk.py 0 1 2 3 DebugRUN
python .\chkout_wibs.py 0 1 2 3 save 1 DebugRUN

::cd "D:\GitHub\WIB_SW_BNL\"
::call test_runs.bat
::cd "D:\GitHub\WIB_SW_BNL\"
::call test_runs_diff.bat
::cd "D:\GitHub\WIB_SW_BNL\"
::call test_runs_adc_sdcen.bat
::cd "D:\GitHub\WIB_SW_BNL\"
::call test_runs_adc_dben.bat
