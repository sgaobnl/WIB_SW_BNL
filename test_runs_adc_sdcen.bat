echo noise study
python .\crp5a_run07.py 0 1 2 3 DebugRUN

echo noise study
python .\crp5a_run08.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0  DebugRUN
::python .\crp5a_run08.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0  DebugRUN
::
::echo calibration
python .\crp5a_run09.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0   DebugRUN
::python .\crp5a_run09.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0  DebugRUN

