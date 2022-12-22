python .\top_femb_pwr_set.py on on on on "3.0" "3.0" "3.5" LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V5

echo noise study
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5

python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V5

python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE3V0_CD3V0_ADC3V5



python .\top_femb_pwr_set.py on on on on "4.0" "4.0" "4.0" LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC4V0

echo noise study
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0

python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC4V0

python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE4V0_CD4V0_ADC4V0


python .\top_femb_pwr_set.py on on on on "3.0" "3.0" "3.2" LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V2

echo noise study
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2

python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD3V0_ADC3V2

python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE3V0_CD3V0_ADC3V2



python .\top_femb_pwr_set.py on on on on "2.8" "2.8" "3.0" LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V8_CD2V8_ADC3V0
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE2V8_CD2V8_ADC3V0


python .\top_femb_pwr_set.py on on on on "2.5" "2.5" "2.8" LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V8
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE2V5_CD2V5_ADC2V8


python .\top_femb_pwr_set.py on on on on "2.4" "2.4" "2.6" LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V4_CD2V4_ADC2V6
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE2V4_CD2V4_ADC2V6


python .\top_femb_pwr_set.py on on on on "2.5" "2.5" "2.5" LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V5_CD2V5_ADC2V5
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE2V5_CD2V5_ADC2V5


python .\top_femb_pwr_set.py on on on on "3.0" "4.0" "4.0" LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE3V0_CD4V0_ADC4V0
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE3V0_CD4V0_ADC4V0


python .\top_femb_pwr_set.py on on on on "4.0" "4.0" "3.0" LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD4V0_ADC3V0
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE4V0_CD4V0_ADC3V0


python .\top_femb_pwr_set.py on on on on "4.0" "3.2" "4.0" LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE4V0_CD3V2_ADC4V0
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE4V0_CD3V2_ADC4V0


python .\top_femb_pwr_set.py on on on on "2.2" "2.5" "2.5" LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_chk_femon.py 0 1 2 3 LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run01.py 0 1 2 3 LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run02.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run04.py 0 1 2 3 LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 0 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 0 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 0 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\crp5a_run05.py 0 1 2 3 100 0 1 0 0 1 1 0 0 0   LN2_BIASOFF_FE2V2_CD2V5_ADC2V5
python .\top_femb_powering.py off off off off  LN2_BIASOFF_FE2V2_CD2V5_ADC2V5


