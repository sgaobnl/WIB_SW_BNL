#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 10/19/2022
#----------------------------------------------------------------------

# from QC_analysis import *
from ASICDAC import savegains

if __name__ == '__main__':
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
    #      qc = QC_analysis(datadir='D:/IO-1865-1C/QC/data', output_dir='D:/IO-1865-1C/QC/analysis', temperature=T, dataType='RMS')
    #      qc.save_rms_pedestal_to_csv()
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
    savedir = '../results'
    inputdir = '../data'
    # inputdir = 'D:/IO-1865-1C/QC/data'
    # savedir = 'D:/IO-1865-1C/QC/analysis'
    # try to save and plot the gains for the data in inputdir
    # asic = ASICDAC_CALI(input_data_dir=inputdir, CALI_number=1, temperature='LN')
    # asic.save_gain_for_all_fembs(savedir=savedir, config=[200, 14.0, 2.0])
    # asic.save_gain_for_allData_oneConfig(savedir=savedir, config=[200, 14.0, 2.0], withLogs=True)
    # plot_gain_vs_CH(savedir=savedir, temperature='LN', CALI_number=1)
    # asic = ASICDAC_CALI(input_data_dir='D:/IO-1865-1C/QC/data/femb115_femb103_femb112_femb75_LN_150pF', CALI_number=1)
    # asic.plot_peakvalue_vs_DAC(savedir='D:/IO-1865-1C/QC/analysis/test', femb_number=3, ch_number=127)
    
    # Gains_CALI1(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=False)
    # Gains_CALI2(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True)
    # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True, CALI_number=3)
    # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True, CALI_number=4)
    # save_peakValues_to_csv(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN',
    #                     withLogs=True, CALI_number=4)
    savegains(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN')