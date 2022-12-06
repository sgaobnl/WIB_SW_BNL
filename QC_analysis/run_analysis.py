#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 11/28/2022
#----------------------------------------------------------------------

import os
from MON import MON_LARASIC, MON_ColdADC
# from QC_analysis import QC_analysis
# from ASICDAC import savegains, Gains_CALI1, Gains_CALI2, Gains_CALI3_or_CALI4
# from ASICDAC import get_ENC_CALI
# from ASICDAC import save_peakValues_to_csv
# from ASICDAC import separateCSV_foreachFEMB
# from ASICDAC import distribution_ENC_Gain
#
# for RMS, Pedestal and PWR
# from ASICDAC import removeFEMB_from_T, all_PWR_Meas_plots
if __name__ == '__main__':
    #------------------------------------------------------
    # savedir = '../results/analysis/minisas/from_DATA'
    # inputdir = '../data'
    inputdir = 'D:/IO-1865-1C/QC/data'
    savedir = 'D:/IO-1865-1C/QC/analysis/'
    #------------------------------------------------------
    # measured_info = ['P_meas', 'V_meas', 'I_meas']
    #temperatures = ['LN', 'RT']
    # temperatures = ['LN']
    # dataname_list = ['Bias5V', 'LArASIC', 'ColdDATA', 'ColdADC']
    #-----------This is a group ---------------------------
    # save data in csv file
    # save_allInfo_PWR_tocsv(data_input_dir='D:/IO-1865-1C/QC/data', output_dir='D:/IO-1865-1C/QC/analysis', temperature_list=temperatures, dataname_list=dataname_list)
    #
    # produce all the plots
    # all_PWR_Meas_plots(csv_source_dir='../data/analysis', measured_info_list=measured_info, temperature_list=temperatures, dataname_list=dataname_list)
    # all_plots(csv_source_dir='D:/IO-1865-1C/QC/analysis', measured_info_list=measured_info, temperature_list=temperatures, dataname_list=dataname_list)
    #-----------------------------------------------------
    #------Save RMS in csv files--------------------------
    # for T in temperatures:
    #     qc = QC_analysis(datadir=inputdir, output_dir=savedir, temperature=T, dataType='RMS')
    #     qc.save_rms_pedestal_to_csv()
    #-----------END saving--------------------------------
    ### Get power consumption ------- PWR_Meas------------
    # plot_PWR_Consumption(csv_source_dir='../data/analysis', temperatures=temperatures,
    #                     all_data_types=dataname_list, output_dir='../data/analysis', powerType='PWR_Meas')
    #-------------------------------END PWR_Meas----------
    ## -----------------save PWR_Cycle to csv files-------
    # save_allInfo_PWRCycle_tocsv(data_input_dir='../data', output_dir='../data/analysis', temperature_list=temperatures, dataname_list=dataname_list)
    # save_allInfo_PWRCycle_tocsv(data_input_dir='D:/IO-1865-1C/QC/data', output_dir='D:/IO-1865-1C/QC/analysis', temperature_list=temperatures, dataname_list=dataname_list)
    #
    # try to plot PWRCycle
    # for m_param in measured_info:
    #    plot_PWR_Cycle(csv_source_dir='../data/analysis/LN/PWR_Cycle', measured_param=m_param)
        # plot_PWR_Cycle(csv_source_dir='D:/IO-1865-1C/QC/analysis/LN/PWR_Cycle', measured_param=m_param)
    # power consumption for PWR_Cycle
    # plot_PWR_Consumption(csv_source_dir='../data/analysis/', all_data_types=dataname_list,
    #                    output_dir='../data/analysis', powerType='PWR_Cycle')
    # plot_PWR_Consumption(csv_source_dir='D:/IO-1865-1C/QC/analysis/', all_data_types=dataname_list,
    #                     output_dir='D:/IO-1865-1C/QC/analysis', powerType='PWR_Cycle')
    #--------------------------------------------------------------------------------------------------
    #=======================ASICDAC_CALI===============================================================
    # try to save and plot the gains for the data in inputdir
    # asic = ASICDAC_CALI(input_data_dir=inputdir, CALI_number=1, temperature='LN')
    # asic.save_gain_for_all_fembs(savedir=savedir, config=[200, 14.0, 2.0])
    # asic.save_gain_for_allData_oneConfig(savedir=savedir, config=[200, 14.0, 2.0], withLogs=True)
    # plot_gain_vs_CH(savedir=savedir, temperature='LN', CALI_number=1)
    # asic = ASICDAC_CALI(input_data_dir='D:/IO-1865-1C/QC/data/femb115_femb103_femb112_femb75_LN_150pF', CALI_number=1)
    # asic.plot_peakvalue_vs_DAC(savedir='D:/IO-1865-1C/QC/analysis/test', femb_number=3, ch_number=127)
    
    # temperature = 'LN'
    # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=3)
    # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=4)

    # temperature = 'RT' # RT or LN
    temperatures = ['LN', 'RT']
    # for temperature in temperatures:
    #     # Gains_CALI1(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True)
    #     # Gains_CALI2(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True)
    #     # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=3)
    #     # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=4)
    #     # for cali in [1, 3]:
    #     #     save_peakValues_to_csv(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature,
    #     #                         withLogs=True, CALI_number=cali) #<==========TEST FUNCTION
    #     # savegains(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature) # <==== FUNCTION TO RUN
    #     # #
    #     # separateCSV_foreachFEMB(path_to_csv='../results/LN/', output_path='../results/LN', datanames=['CALI1', 'CALI2', 'CALI3', 'CALI4'])
    #     #********************************ENC***************************************************************
    #     # CALI_numbers = [1]#, 2, 3, 4]
    #     CALI_numbers = [2, 3, 4]
    #     fembs_to_exclude = [75, 111]
    #     if temperature == 'RT':
    #         # CALI_numbers = ['']
    #         # fembs_to_exclude = ['07', 24, 27, 55, 75]
    #         fembs_to_exclude = [7, 24, 27, 55, 75, 111]
    #     for CALI_number in CALI_numbers:
    #         get_ENC_CALI(input_dir=savedir, temperature=temperature, CALI_number=CALI_number, fembs_to_exclude=fembs_to_exclude)
    # for temperature in temperatures:
    #     listgains = ['4_7', '7_8', '14_0', '25_0']
    #     larasic_gains = ['{}mVfC'.format(g) for g in listgains]
    #     CALI_numbers = [1, 2, 3, 4]
    #     for CALI in CALI_numbers:
    #         for larasic_gain in larasic_gains:
    #             distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=True)
    #             distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=False)
    
    # savedir = '../results/analysis/test_MON_FE'
    for T in temperatures:
        mon_fe = MON_LARASIC(input_dir=inputdir, output_dir=savedir, output_dirname='MON_FE', temperature=T, fembs_to_exclude=[7, 24, 27, 55])
        mon_fe.run_MON_LArASIC()
        mon_fe.run_MON_LArASIC_DAC()
        mon_adc = MON_ColdADC(input_dir=inputdir, output_dir=savedir, temperature=T, fembs_to_exclude=[7, 24, 27, 55, 75])
        mon_adc.run_MON_ColdADC(read_bin=True, n_rmse=1)
