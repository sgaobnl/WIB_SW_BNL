echo pulse response
python .\crp5a_run04.py 0 1 2 3 RTRUN2

echo noise study
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0 RTRUN2
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 0 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 1 0 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 0 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 0 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 0 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 1 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 1 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 0 1 1 1 1 0 0 0 RTRUN2 
python .\crp5a_run05.py 0 1 2 3 100 0 1 1 1 1 1 0 0 0 RTRUN2 


echo calibration
python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 0 0 0 0 0 0 RTRUN2 
python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 0 0 0 0 0 0 RTRUN2 
python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 0 RTRUN2  
python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 RTRUN2 
python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 0 1 0 0 0 0 RTRUN2  
python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 0 1 0 0 0 0 RTRUN2 

python .\crp5a_run06.py 0 1 2 3 30 1 0 0 0 1 1 0 0 0 1 RTRUN2  
python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 1 RTRUN2 

python .\crp5a_run06.py 0 1 2 3 30 1 1 0 0 1 1 0 0 0 0 RTRUN2
python .\crp5a_run06.py 0 1 2 3 30 1 1 0 1 1 1 0 0 0 0 RTRUN2
python .\crp5a_run06.py 0 1 2 3 30 1 1 1 0 1 1 0 0 0 0 RTRUN2  
python .\crp5a_run06.py 0 1 2 3 30 1 1 1 1 1 1 0 0 0 0 RTRUN2  

