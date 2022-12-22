echo noise study
python .\crp5a_run01.py 0 1 2 3 SERMS

echo noise study
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 0 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 0 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 0 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 1 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 1 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 1 1 1 1 0 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 1 1 1 1 0 0 0   SERMS
::                                                     
echo sdf = 1                                        
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 1 0 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 1 0 0   SERMS
                                                   
echo leak currents                                
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 0   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 1   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 1   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 1 1   SERMS
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 1 1   SERMS
                                                        

