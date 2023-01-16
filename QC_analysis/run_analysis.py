#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 12/27/2022
#----------------------------------------------------------------------
import ast

import os
from MON import MON_LARASIC, MON_ColdADC
from ASICDAC import savegains, Gains_CALI1, Gains_CALI2, Gains_CALI3_or_CALI4
from ASICDAC import get_ENC_CALI, separateCSV_foreachFEMB
from ASICDAC import GainFEMBs_vs_GainLArASIC, ENC_vs_FEMB_ids
from ASICDAC import distribution_ENC_Gain
from QC_analysis import QC_analysis, save_allInfo_PWR_tocsv, plot_PWR_Consumption, all_PWR_Meas_plots, save_allInfo_PWRCycle_tocsv, plot_PWR_Cycle
import Analysis_FEMB_QC

def get_input_output_dirs(where='local', folderName=''):
    '''
        This function is used to select the input and output folder by providing the location
        where we want to run the script.
        Options available:
            - local: the input data (*.bin) should be in a folder named "../data"
            - hothstor
            - 1-216 (the lab)
            For hothstor and the lab, we need to provide the name of the data folder
    '''
    inputdir = ''
    savedir = ''
    if where=='local':
        #***************if running locally********************
        savedir = '../results/analysis/minisas'
        inputdir = '../data'
    elif where=='hothstor':
        #****************if running on hothstor***************
        # savedir = '/dsk/3/tmp/FEMB_QC/{}/QC/analysis'.format(folderName)
        savedir = "/home/rrazakami/workspace/QC_analysis"
        inputdir = '/dsk/3/tmp/FEMB_QC/{}/QC/data'.format(folderName)
    elif where=='1-216':
        #****************if running in lab 1-216**************
        inputdir = 'D:/{}/QC/data'.format(folderName)
        savedir = 'D:/{}/QC/analysis/'.format(folderName)
        #*****************************************************
    # try to create the saving folder
    try:
        os.mkdir(savedir)
    except OSError:
        print(OSError)
    return inputdir, savedir

def input_fembs_to_ignore():
    fembs_to_ignore = {}
    answer1 = input('Do you want to ignore some fembs ? (y/other) ::>')
    while answer1=='y':
        femb_in_folder = input('Enter the foldername and the list of fembs to ignore in the shape: femb_foldername : ["3", "54"] ::> ')
        key = femb_in_folder.split(':')[0].strip()
        value = [v.strip() for v in ast.literal_eval(femb_in_folder.split(':')[1].strip())]
        fembs_to_ignore[key] = value
        answer1 = input('Do you want to enter more folder ? (y/other) ::>')
    return fembs_to_ignore

def run_PWR_Meas(inputdir, savedir, fembs_to_ignore={}, fembs_to_exclude=[]):
    # ------------------------------------------------------
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    temperatures = ['LN', 'RT']
    dataname_list = ['Bias5V', 'ColDATA', 'LArASIC', 'ColdADC']
    # -----------This is a group ---------------------------
    # save data in csv file
    save_allInfo_PWR_tocsv(data_input_dir=inputdir, output_dir=savedir, temperature_list=temperatures, dataname_list=dataname_list, fembs_to_ignore=fembs_to_ignore)
    
    # produce all the plots
    all_PWR_Meas_plots(csv_source_dir=savedir, measured_info_list=measured_info, temperature_list=temperatures, dataname_list=dataname_list, fembs_to_exclude=fembs_to_exclude)
    ### Get power consumption ------- PWR_Meas------------
    plot_PWR_Consumption(csv_source_dir=savedir, temperatures=temperatures, fembs_to_exclude=fembs_to_exclude,
                        all_data_types=dataname_list, output_dir=savedir, powerType='PWR_Meas')

def run_RMS_Pedestal(inputdir, savedir, femb_to_exclude=[], fembs_to_ignore={}):
    temperatures = ['LN', 'RT']
    datanames = ['Pedestal', 'RMS']
    #------Save RMS in csv files--------------------------
    for T in temperatures:
        qc = QC_analysis(datadir=inputdir, output_dir=savedir, temperature=T, dataType='RMS', fembs_to_ignore=fembs_to_ignore)
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
            # if dataname=='Pedestal':
            #     ylim200 = [500, 1650]
            #     ylim900 = [7750, 9500]
            # elif dataname=='RMS':
            #     ylim200 = [0, 55]
            #     ylim900 = [0, 55]

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

def run_PWR_Cycle(inputdir, savedir, fembs_to_ignore={}, fembs_to_exclude=[]):
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    # temperatures = ['LN', 'RT']
    temperatures = ['LN']
    dataname_list = ['Bias5V', 'LArASIC', 'ColDATA', 'ColdADC']
    ## -----------------save PWR_Cycle to csv files-------
    save_allInfo_PWRCycle_tocsv(data_input_dir=inputdir, output_dir=savedir, temperature_list=temperatures, dataname_list=dataname_list, fembs_to_ignore=fembs_to_ignore)
    #
    # try to plot PWRCycle
    for m_param in measured_info:
       plot_PWR_Cycle(csv_source_dir='{}/LN/PWR_Cycle'.format(savedir), measured_param=m_param, fembs_to_exclude=fembs_to_exclude)
    # power consumption for PWR_Cycle
    plot_PWR_Consumption(csv_source_dir=savedir, all_data_types=dataname_list,
                       output_dir=savedir, powerType='PWR_Cycle', fembs_to_exclude=fembs_to_exclude)
    #--------------------------------------------------------------------------------------------------

def run_ASICDAC(inputdir, savedir, temperatures, fembs_to_exclude=[], fembs_to_ignore={}):
    # for temperature in temperatures:
        # Gains_CALI1(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, fembs_to_ignore=fembs_to_ignore)
        # Gains_CALI2(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, fembs_to_ignore=fembs_to_ignore)
        # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, fembs_to_ignore=fembs_to_ignore, CALI_number=3)
        # Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature, withlogs=True, fembs_to_ignore=fembs_to_ignore, CALI_number=4)
        # savegains(path_to_dataFolder=inputdir, output_dir=savedir, temperature=temperature) # <==== FUNCTION TO RUN
        # #
        # separateCSV_foreachFEMB(path_to_csv='/'.join([savedir, temperature]), output_path='/'.join([savedir, temperature]), datanames=['CALI1', 'CALI2', 'CALI3', 'CALI4'])
        # #********************************ENC***************************************************************
        # CALI_numbers = [1, 2, 3, 4]
        # listgains = ['4_7', '7_8', '14_0', '25_0']
        # for CALI_number in CALI_numbers:
        #     if CALI_number!=1:
        #         listgains = ['14_0']
        #     get_ENC_CALI(datadir=inputdir, input_dir=savedir, temperature=temperature, CALI_number=CALI_number, listgains=listgains,
        #                 fembs_to_exclude=fembs_to_exclude, fembs_to_ignore=fembs_to_ignore)
        #     larasic_gains = ['{}mVfC'.format(g) for g in listgains]
        #     # for CALI in CALI_numbers:
        #     for larasic_gain in larasic_gains:
        #         distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI_number, temperature=temperature, larasic_gain=larasic_gain, fit=True)
        #         distribution_ENC_Gain(csv_source_dir=savedir, CALI_number=CALI_number, temperature=temperature, larasic_gain=larasic_gain, fit=False)
    # GainFEMBs = f(GainLArASIC)
    GainFEMBs_vs_GainLArASIC(input_dir=savedir, fembs_to_exclude=fembs_to_exclude)
    #
    ## ENC = f(FEMB_IDs)
    ENC_vs_FEMB_ids(input_dir=savedir, fontsize_xticks=8)

def run_MON_FE_MON_ADC(inputdir, savedir, temperatures, fembs_to_exclude=[]):
    for T in temperatures:
        mon_fe = MON_LARASIC(input_dir=inputdir, output_dir=savedir, output_dirname='MON_FE', temperature=T, fembs_to_exclude=fembs_to_exclude)
        mon_fe.run_MON_LArASIC()
        # mon_fe.run_MON_LArASIC_DAC(read_bin=False)
        mon_adc = MON_ColdADC(input_dir=inputdir, output_dir=savedir, temperature=T, fembs_to_exclude=fembs_to_exclude)
        mon_adc.run_MON_ColdADC(read_bin=True, n_rmse=1)

if __name__ == '__main__':
    #------------------------------------------------------
    # lab 1-216: IO-1865-1C (old fembs)
    # hothstor: IO-1865-1D (new fembs)
    # inputdir, savedir = get_input_output_dirs(where='hothstor', folderName='IO-1865-1D')
    inputdir, savedir = '', '../results/IO-1865-1C/minisas'
    # inputdir, savedir = get_input_output_dirs(where='1-216', folderName='IO-1865-1C')
    # inputdir, savedir = get_input_output_dirs(where='local', folderName='')
    #------------------------------------------------------
    
    temperatures = ['LN', 'RT']

    # fembs_to_ignore = {
    #     "femb46_femb54_femb55_femb2": ['46', '2'],
    #     "femb0013_femb0075_femb0056_femb0026": ['0075'],
    #     "femb0011_femb0079_femb0008_femb0073": ['0073']
    # }
    fembs_to_ignore = {}
    # fembs_to_ignore = input_fembs_to_ignore() # if you want to input the fembs to ignore manually, uncomment this line
    # print(fembs_to_ignore)
    # run_PWR_Meas(inputdir=inputdir, savedir=savedir, fembs_to_ignore=fembs_to_ignore, fembs_to_exclude=[111])
    # run_RMS_Pedestal(inputdir=inputdir, savedir=savedir, femb_to_exclude=[], fembs_to_ignore=fembs_to_ignore)
    run_ASICDAC(inputdir=inputdir, savedir=savedir, temperatures=temperatures, fembs_to_exclude=[111], fembs_to_ignore=fembs_to_ignore)
    # run_PWR_Cycle(inputdir=inputdir, savedir=savedir, fembs_to_ignore=fembs_to_ignore, fembs_to_exclude=[111])
    # run_MON_FE_MON_ADC(inputdir=inputdir, savedir=savedir, temperatures=temperatures, fembs_to_exclude=[111])