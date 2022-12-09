#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 11/28/2022
#----------------------------------------------------------------------

import os
from MON import MON_LARASIC, MON_ColdADC
# from QC_analysis import QC_analysis
from ASICDAC import savegains, Gains_CALI1, Gains_CALI2, Gains_CALI3_or_CALI4
from ASICDAC import get_ENC_CALI
# from ASICDAC import save_peakValues_to_csv
from ASICDAC import separateCSV_foreachFEMB
from ASICDAC import distribution_ENC_Gain
#
# for RMS, Pedestal and PWR
# from ASICDAC import all_PWR_Meas_plots
from QC_analysis import QC_analysis, save_allInfo_PWR_tocsv, plot_PWR_Consumption, all_PWR_Meas_plots, save_allInfo_PWRCycle_tocsv, plot_PWR_Cycle
import Analysis_FEMB_QC

def run_PWR_Meas(inputdir, savedir):
    # ------------------------------------------------------
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    temperatures = ['LN', 'RT']
    dataname_list = ['Bias5V', 'LArASIC', 'ColdDATA', 'ColdADC']
    # -----------This is a group ---------------------------
    # save data in csv file
    save_allInfo_PWR_tocsv(data_input_dir=inputdir, output_dir=savedir, temperature_list=temperatures, dataname_list=dataname_list)
    
    # produce all the plots
    all_PWR_Meas_plots(csv_source_dir=savedir, measured_info_list=measured_info, temperature_list=temperatures, dataname_list=dataname_list)
    ### Get power consumption ------- PWR_Meas------------
    plot_PWR_Consumption(csv_source_dir=savedir, temperatures=temperatures,
                        all_data_types=dataname_list, output_dir=savedir, powerType='PWR_Meas')

def run_RMS_Pedestal(inputdir, savedir, femb_to_exclude=[75, 24, 55, 7, 27]):
    temperatures = ['LN', 'RT']
    datanames = ['Pedestal', 'RMS']
    #------Save RMS in csv files--------------------------
    for T in temperatures:
        qc = QC_analysis(datadir=inputdir, output_dir=savedir, temperature=T, dataType='RMS')
        qc.save_rms_pedestal_to_csv()
    #-----------END saving--------------------------------
    # correct csv files for RMS by removing some fembs
        path_to_csvfiles = '/'.join([savedir, T, 'RMS'])
        output_path = '/'.join([savedir, T, 'RMS', 'correctedCSV_rms_pedestal'])
        try:
            os.mkdir(output_path)
        except OSError:
            print(OSError)

        Analysis_FEMB_QC.saveCorrectedCSV(path_to_csv=path_to_csvfiles, femb_list=femb_to_exclude, output_path=output_path, datanames=datanames)

        for dataname in datanames:
            try:
                os.mkdir('/'.join([output_path, 'plots']))
            except OSError:
                print(OSError)
            sourceMainDir = output_path
            new_output_path = '/'.join([output_path, 'plots', dataname])
            try:
                os.mkdir(new_output_path)
            except OSError:
                print(OSError)

            Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir=sourceMainDir,
                                            dataType=dataname, outputDir=new_output_path,
                                            nstd=3, nbins=60, skewed=True)
            ylim200, ylim900 = [], []
            if dataname=='Pedestal':
                ylim200 = [500, 1650]
                ylim900 = [7750, 9500]
            elif dataname=='RMS':
                ylim200 = [0, 55]
                ylim900 = [0, 55]

            Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='/'.join([new_output_path, 'gaussian_'+dataname+'.csv']),
                                                     BL='200mV',
                                                     outputDir= new_output_path,
                                                     ylabel=dataname,
                                                     addToTitle='', skewed=True, ylim=ylim200)
            Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv= new_output_path + '/gaussian_'+ dataname +'.csv',
                                                     BL='900mV',
                                                     outputDir=new_output_path,
                                                     ylabel=dataname,
                                                     addToTitle='', skewed=True, ylim=ylim900)

def run_PWR_Cycle(inputdir, savedir):
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    temperatures = ['LN', 'RT']
    dataname_list = ['Bias5V', 'LArASIC', 'ColdDATA', 'ColdADC']
    ## -----------------save PWR_Cycle to csv files-------
    save_allInfo_PWRCycle_tocsv(data_input_dir='../data', output_dir='../data/analysis', temperature_list=temperatures, dataname_list=dataname_list)
    #
    # try to plot PWRCycle
    for m_param in measured_info:
       plot_PWR_Cycle(csv_source_dir='{}/LN/PWR_Cycle'.format(savedir), measured_param=m_param)
    # power consumption for PWR_Cycle
    plot_PWR_Consumption(csv_source_dir=savedir, all_data_types=dataname_list,
                       output_dir=savedir, powerType='PWR_Cycle')
    #--------------------------------------------------------------------------------------------------

def run_ASICDAC(inputdir, savedir, temperatures, fembs_to_exclude=[]):
    for temperature in temperatures:
        Gains_CALI1(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True)
        Gains_CALI2(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True)
        Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=3)
        Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, CALI_number=4)
        # savegains(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature) # <==== FUNCTION TO RUN
        #
        # separateCSV_foreachFEMB(path_to_csv='/'.join([savedir, temperature]), output_path='/'.join([savedir, temperature]), datanames=['CALI1', 'CALI3'])
        separateCSV_foreachFEMB(path_to_csv='/'.join([savedir, temperature]), output_path='/'.join([savedir, temperature]), datanames=['CALI1', 'CALI2', 'CALI3', 'CALI4'])
        #********************************ENC***************************************************************
        CALI_numbers = [1, 2, 3, 4]
        # CALI_numbers = [1,3]
        for CALI_number in CALI_numbers:
            get_ENC_CALI(datadir=inputdir, input_dir=savedir, temperature=temperature, CALI_number=CALI_number, fembs_to_exclude=fembs_to_exclude)
        listgains = ['4_7', '7_8', '14_0', '25_0']
        larasic_gains = ['{}mVfC'.format(g) for g in listgains]
        # CALI_numbers = [1, 2, 3, 4]
        for CALI in CALI_numbers:
            for larasic_gain in larasic_gains:
                distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=True)
                distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=False)

def run_MON_FE_MON_ADC(inputdir, savedir, temperatures, fembs_to_exclude=[]):
    for T in temperatures:
        mon_fe = MON_LARASIC(input_dir=inputdir, output_dir=savedir, output_dirname='MON_FE', temperature=T, fembs_to_exclude=fembs_to_exclude)
        mon_fe.run_MON_LArASIC()
        mon_fe.run_MON_LArASIC_DAC()
        mon_adc = MON_ColdADC(input_dir=inputdir, output_dir=savedir, temperature=T, fembs_to_exclude=fembs_to_exclude)
        mon_adc.run_MON_ColdADC(read_bin=True, n_rmse=1)

if __name__ == '__main__':
    #------------------------------------------------------
    savedir = '../results/analysis/test'
    inputdir = '../data'
    # inputdir = 'D:/IO-1865-1C/QC/data'
    # savedir = 'D:/IO-1865-1C/QC/analysis/'
    #------------------------------------------------------
    # measured_info = ['P_meas', 'V_meas', 'I_meas']
    #temperatures = ['LN', 'RT']
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
    # plot_PWR_Consumption(csv_source_dir=savedir, all_data_types=dataname_list,
    #                    output_dir=savedir, powerType='PWR_Cycle')
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
    #         get_ENC_CALI(datadir=inputdir, input_dir=savedir, temperature=temperature, CALI_number=CALI_number, fembs_to_exclude=fembs_to_exclude)
    # for temperature in temperatures:
    #     listgains = ['4_7', '7_8', '14_0', '25_0']
    #     larasic_gains = ['{}mVfC'.format(g) for g in listgains]
    #     CALI_numbers = [1, 2, 3, 4]
    #     for CALI in CALI_numbers:
    #         for larasic_gain in larasic_gains:
    #             distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=True)
    #             distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI, temperature=temperature, larasic_gain=larasic_gain, fit=False)
    
    # savedir = '../results/analysis/test_MON_FE'
    run_PWR_Meas(inputdir=inputdir, savedir=savedir)
    run_RMS_Pedestal(inputdir=inputdir, savedir=savedir, femb_to_exclude=[])
    run_ASICDAC(inputdir=inputdir, savedir=savedir, temperatures=temperatures, fembs_to_exclude=[])
    run_PWR_Cycle(inputdir=inputdir, savedir=savedir)
    run_MON_FE_MON_ADC(inputdir=inputdir, savedir=savedir, temperatures=temperatures, fembs_to_exclude=[])