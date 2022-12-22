cd "D:\GitHub\WIB_SW_BNL\"
python .\top_femb_powering.py off off off off PreRUN
python .\top_femb_powering.py on on on on PreRUN
python .\crp5a_chk_femon.py 0 1 2 3 PreRUN
python .\chkout_wibs.py 0 1 2 3 save 1 PreRUN
python .\crp5a_chk_femon.py 0 1 2 3 PreRUN

