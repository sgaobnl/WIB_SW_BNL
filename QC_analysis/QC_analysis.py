# outputdir : D:/IO-1865-1C/QC/analysis
# datadir : D:/IO-1865-1C/QC/data/..../PWR_Meas
# import chunk
# import csv
from importlib.resources import path
from re import I
import sys
# from tkinter import Listbox
# from tracemalloc import start
# from turtle import begin_fill
sys.path.append('..')
import os
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.signal import find_peaks
from QC_tools import QC_tools

import gc

def was_femb_saved(sourceDir='', temperature='RT', dataname='Bias5V', new_femb_dir=''):
    '''
    This function checks if the femb data in the folder new_femb_dir is already saved in temperature/dataname.csv.
    sourceDir: parent folder of the csv file, e.g: D:/IO-1865-1C/QC/analysis,
    temperature: LN or RT
    dataname: Bias5V, LArASIC, ColdDATA or ColdADC
    new_femb_dir: name of the folder where the data is located
    '''
    try:
        df = pd.read_csv('/'.join([sourceDir, temperature, dataname + '.csv']))
        FEMB_names = new_femb_dir.split('_')[:-3]
        FEMB_ids = [femb[4:] for femb in FEMB_names]
        FEMB_check = []
        for femb in FEMB_ids:
            temp_check = False
            if femb in df['FEMB_ID']:
                temp_check = True
            FEMB_check.append((femb, temp_check))
        FEMB_dict = dict(FEMB_check)
        return FEMB_dict
    except:
        return dict() # return an empty dictionary if the csv file doesn't exist

class QC_analysis:
    def __init__(self, datadir='', output_dir='', temperature='RT', dataType='power_measurement'):
        try:
            os.mkdir('/'.join([output_dir, temperature]))
        except:
            print('--------------{} already exists----------'.format(temperature))
            pass
        # save the temperature
        self.temperature = temperature
        
        self.particularDataFolderName = ''
        # choose which data to use
        # dataType = 'power_measurement'
        # ----------------------------------------------
        # --> Modification here: what if dataType is RMS
        if (dataType=='power_measurement') | (dataType=='PWR_Meas'):
            self.indexData = 1
            self.particularDataFolderName = 'PWR_Meas'
        elif dataType=='RMS':
            self.particularDataFolderName = 'RMS'
        elif dataType=='PWR_Cycle':
            self.indexData = 1
            self.particularDataFolderName = 'PWR_Cycle'
        #
        # save the path to the output
        try:
            os.mkdir('/'.join([output_dir, temperature, self.particularDataFolderName]))
        except:
            print('{} folder already exists !!!'.format(self.particularDataFolderName))
        self.output_analysis_dir = '/'.join([output_dir, temperature, self.particularDataFolderName])

        #
        # check if a folder named PWR_Meas exists --> if self.particularDataFolderName exists
        new_data_dir = []
        for onefolder in os.listdir(datadir):
            if (temperature in onefolder) & (self.particularDataFolderName in os.listdir('/'.join([datadir, onefolder]))):
                new_data_dir.append('/'.join([datadir, onefolder, self.particularDataFolderName]))
        self.input_data_dir = new_data_dir
        #self.input_data_dir = ['/'.join([datadir, onefolder, self.particularDataFolderName]) for onefolder in os.listdir(datadir) if temperature in onefolder]
        self.bin_filenames = os.listdir(self.input_data_dir[0]) ## the *.bin filenames are the same for all the folders

    def read_bin(self, filename, input_data_dir):
        with open('/'.join([input_data_dir, filename]), 'rb') as fp:
            if (self.particularDataFolderName=='PWR_Meas') | (self.particularDataFolderName=='PWR_Cycle'):
                return pickle.load(fp)[self.indexData]
            elif self.particularDataFolderName=='RMS':
                # read the logs_env.bin file to get the informations about the femb#, temperature, note
                logs_dir = input_data_dir.split('/')[:-1]
                with open('/'.join(['/'.join(logs_dir), 'logs_env.bin']), 'rb') as fp_log:
                    logs_env = pickle.load(fp_log)
                #
                # decode data here
                raw = pickle.load(fp)
                rawdata = raw[0]
                # pwr_meas = raw[1]
                # data decoding <-- same as in QC_tools
                qc = QC_tools()
                pldata = qc.data_decode(rawdata)
                pldata = np.array(pldata)
                # print(len(pldata[0]))
                nevent = len(pldata)
                if nevent>100:
                    nevent=100
                #
                # femb ids
                nfembs = [0, 1, 2, 3]
                ch_list = []
                femb_id_list = []
                rms_list = []
                ped_list = []
                for nfemb in nfembs:
                    #print('Getting data for femb id: {}....\n'.format(logs_env['femb id']['femb'+str(nfemb)]))
                    # rms = []
                    # ped = []
                    for ich in range(128):
                        global_ch = nfemb*128 + ich
                        peddata = np.empty(0)
                        
                        allpls = np.empty(0)
                        for itr in range(nevent):
                            evtdata = pldata[itr][global_ch]
                            allpls = np.append(allpls, evtdata)
                        ch_ped = np.mean(allpls)
                        ch_mean = np.std(allpls)
                        # ped.append(ch_ped)
                        # rms.append(ch_mean)
                        ch_list.append(ich)
                        femb_id_list.append(logs_env['femb id']['femb'+str(nfemb)])
                        rms_list.append(ch_mean)
                        ped_list.append(ch_ped)
                    # rms_list.append((str(nfemb), rms))
                    # ped_list.append((str(nfemb), ped))
                # rms_dict = dict(rms_list)
                # ped_dict = dict(ped_list)
                rms_dict = {'channelNumber': ch_list, 'femb_ids': femb_id_list, 'RMS': rms_list}
                ped_dict = {'channelNumber': ch_list, 'femb_ids': femb_id_list, 'Pedestal': ped_list}
                # return dictionaries of RMS and Pedestal
                return rms_dict, ped_dict

    def save_rms_pedestal_to_csv(self):
        if self.particularDataFolderName != 'RMS':
            print('Unable to save rms and pedestal....')
            return False

        # create folders for RMS and pedestal
        for d in ['RMS', 'Pedestal']:
            try:
                os.mkdir('/'.join([self.output_analysis_dir, d]))
            except:
                print('Folder already exists...')
                pass
        ## ***************************************************************************************
        ## CHANGE BEING MADE: now, the output of the code is one csv file for each configuration.
        ## ***************************************************************************************
        #for inputdatadir in self.input_data_dir:
        for binfile in tqdm(self.bin_filenames):
            rms_df = pd.DataFrame({'channelNumber': [], 'femb_ids': [], 'RMS': [], 'folderName': []})
            ped_df = pd.DataFrame({'channelNumber': [], 'femb_ids': [], 'Pedestal': [], 'folderName': []})

            # name of the csv file
            csv_name = '_'.join([ binfile, '.csv'])
            for inputdatadir in self.input_data_dir:
                #csv_name = '_'.join([ binfile, '.csv'])
                # try to create a folder having the same name as the data_folder
                #try:
                #    os.mkdir('/'.join([self.output_analysis_dir, inputdatadir.split('/')[-2]]))
                #except:
                    # print('----Error when creating the folder....')
                #    pass
                #outputdir = '/'.join([self.output_analysis_dir, inputdatadir.split('/')[-2]])
                # try to create folders for RMS and Pedestal
                #for d in ['RMS', 'Pedestal']:
                #    try:
                #        os.mkdir('/'.join([outputdir, d]))
                #    except:
                #        pass
                rms_dict, ped_dict = self.read_bin(filename=binfile, input_data_dir=inputdatadir)
                #
                # add the folderName = fembID_Temperature_inputCapacitance
                folderName = (inputdatadir.split('/')[-2]).split('_')
                folderName_col = ['_'.join([str(femb_id), folderName[-2], folderName[-1]]) for femb_id in rms_dict['femb_ids']]
                rms_dict['folderName'] = folderName_col
                ped_dict['folderName'] = folderName_col
                #rms_df = pd.DataFrame(rms_dict)
                #ped_df = pd.DataFrame(ped_dict)
                # save in csv at self.output_analysis_dir
                #rms_df.to_csv('/'.join([outputdir, 'RMS', csv_name]), index=False)
                #ped_df.to_csv('/'.join([outputdir, 'Pedestal', csv_name]), index=False)
                rms_df = pd.concat([rms_df, pd.DataFrame(rms_dict)])
                ped_df = pd.concat([ped_df, pd.DataFrame(ped_dict)])
            rms_df.to_csv('/'.join([self.output_analysis_dir, 'RMS', csv_name]), index=False)
            ped_df.to_csv('/'.join([self.output_analysis_dir, 'Pedestal', csv_name]), index=False)

    def get_oneData_PWR(self, sourceDataDir='', powerTestType_with_BL='SE_200mVBL', dataname='bias', bin_filenames=[]):
        '''----Help section-----'''
        # read the logs_env.bin file to get the informations about the femb#, temperature, note
        logs_dir = sourceDataDir.split('/')[:-1]
        #print('/'.join(logs_dir))
        with open('/'.join(['/'.join(logs_dir), 'logs_env.bin']), 'rb') as fp:
            logs_env = pickle.load(fp)
        #
        # get the filename to be used
        file_to_be_used = ''
        for f in bin_filenames:
            if powerTestType_with_BL in f:
                file_to_be_used = f
                break
        # current_data is a dictionary of the data
        current_data = self.read_bin(filename=file_to_be_used, input_data_dir=sourceDataDir)
        # keys: femb#
        # values: the data we want
        # structure of one value: [name, V_meas(V), I_meas(A), P_meas(W)]
        femb_numbers = current_data.keys()
        name, indexData = '', -1
        if (dataname=='bias') | (dataname=='BIAS') | (dataname=='Bias5V') | (dataname=='Bias'):
            name = 'Bias5V'
            indexData = 0
        elif dataname=='LArASIC':
            name = 'PWR_FE'
            indexData = 1
        elif dataname=='ColdDATA':
            name = 'PWR_CD'
            indexData = 2
        elif dataname=='ColdADC':
            name = 'PWR_ADC'
            indexData = 3
        
        V_meas = [((current_data[femb])[indexData])[1] for femb in femb_numbers]
        I_meas = [((current_data[femb])[indexData])[2] for femb in femb_numbers]
        P_meas = [((current_data[femb])[indexData])[3] for femb in femb_numbers]
    
        # title of the plot
        title = '_'.join([name, '_'.join(powerTestType_with_BL.split('_')[:-1])])
        dirname = sourceDataDir.split('/')[-2]
        #
        # get the femb IDs: 115, 103, etc.
        femb_ids = []
        # get the toytpc: e.g: 150pF
        toytpc = []
        for femb in femb_numbers:
            #femb_ids.append('_'.join(['fembID_', logs_env['femb id'][femb]]))
            femb_ids.append(logs_env['femb id'][femb])
            toytpc.append(logs_env['toytpc'])

        return (title, dirname, femb_ids, toytpc, V_meas, I_meas, P_meas)

    def save_PWRdata_from_allFolders(self, dataname='bias', pwr_test_types=['SE_200mVBL', 'SE_SDF_200mVBL', 'DIFF_200mVBL']):
        # pwr_test_types = ['SE_200mVBL', 'SE_SDF_200mVBL', 'DIFF_200mVBL']

        title = ''
        all_femb_ids = []
        out_df = pd.DataFrame()
        all_toytpc= [] # new line
        for pwr in pwr_test_types:
            femb_ids, toytpc, V_meas, I_meas, P_meas = [], [], [], [], []
            for inputdir_name in self.input_data_dir:
                tmp_title, tmp_dirname, tmp_femb_ids, tmp_toytpc, tmp_V_meas, tmp_I_meas, tmp_P_meas = self.get_oneData_PWR(sourceDataDir=inputdir_name,
                                                                                                                            powerTestType_with_BL=pwr,
                                                                                                                            dataname=dataname,
                                                                                                                            bin_filenames=self.bin_filenames)
                V_meas += tmp_V_meas
                I_meas += tmp_I_meas
                P_meas += tmp_P_meas
                femb_ids += tmp_femb_ids
                toytpc += tmp_toytpc
                title = tmp_title
            #csv_name = '_'.join([title, '.csv'])
            tmp_out_df = pd.DataFrame({
                #'FEMB_ID_': [femb.split('_')[-1] for femb in femb_ids],
                'V_meas_'+'_'.join(pwr.split('_')[:-1]): V_meas,
                'I_meas_'+'_'.join(pwr.split('_')[:-1]): I_meas,
                'P_meas_'+'_'.join(pwr.split('_')[:-1]): P_meas})
            out_df = pd.concat([out_df, tmp_out_df], axis=1)
            all_femb_ids = femb_ids
            all_toytpc = toytpc ## -- new line
        all_femb_ids = [femb for femb in all_femb_ids]
        final_df = pd.DataFrame({'FEMB_ID': all_femb_ids})
        final_df = pd.concat([final_df, out_df], axis=1)
        final_df['FEMB_ID'] = final_df.FEMB_ID.astype(str)
        final_df['toytpc'] = pd.Series(all_toytpc) # add the list of toytpc
        #
        pwrs = ['_'.join(p.split('_')[:-1]) for p in pwr_test_types]
        csv_name = dataname+ '_' + '_'.join(pwrs) + '.csv'
        #
        final_df.to_csv('/'.join([self.output_analysis_dir, csv_name]), index=False)
    
    def get_PWRCycle_SE_from_allFolders(self, dataname='bias'):
        pwr_test_types = 'SE_200mVBL'
        ## select the right list of bin files
        bin_files = []
        for f in self.bin_filenames:
            if pwr_test_types in f:
                bin_files.append(f)
        femb_ids, toytpc, V_meas, I_meas, P_meas = [], [], [], [], []
        for inputdir in self.input_data_dir:
            for binfile in bin_files:
                # get the data for one bin file
                tmp_title, tmp_dirname, tmp_femb_ids, tmp_toytpc, tmp_V_meas, tmp_I_meas, tmp_P_meas = self.get_oneData_PWR(sourceDataDir=inputdir,
                                                                                                                                powerTestType_with_BL=pwr_test_types,
                                                                                                                                dataname=dataname,
                                                                                                                                bin_filenames=[binfile])
                info_in_bin = binfile.split('_')
                theCycle = ''
                if 'cycle' in info_in_bin[1]:
                    theCycle = info_in_bin[1][-1]
                tmp_femb_ids = ['_'.join([femb, theCycle]) for femb in tmp_femb_ids]
                femb_ids += tmp_femb_ids
                toytpc += tmp_toytpc
                V_meas += tmp_V_meas
                I_meas += tmp_I_meas
                P_meas += tmp_P_meas
        out_df = pd.DataFrame({
                'FEMB_ID': femb_ids,
                'toy_tpc': toytpc,
                'V_meas_'+'_'.join(pwr_test_types.split('_')[:-1]): V_meas,
                'I_meas_'+'_'.join(pwr_test_types.split('_')[:-1]): I_meas,
                'P_meas_'+'_'.join(pwr_test_types.split('_')[:-1]): P_meas })
        return out_df
    
    def save_PWRCycle_from_allFolders(self, dataname='bias'):
        SE_df = self.get_PWRCycle_SE_from_allFolders(dataname=dataname)
        csvname = dataname + '_SE.csv'
        SE_df.to_csv('/'.join([self.output_analysis_dir, csvname]), index=False)
        # get SE_SDF and DIFF
        pwr_test_types = ['SE_SDF_200mVBL', 'DIFF_200mVBL']
        self.save_PWRdata_from_allFolders(dataname=dataname, pwr_test_types=pwr_test_types)

                
# save all informations from the *.bin files to csv
# PWR_Meas
def save_allInfo_PWR_tocsv(data_input_dir='', output_dir='', temperature_list=[], dataname_list=[]):
    for T in temperature_list:
        qc = QC_analysis(datadir=data_input_dir, output_dir=output_dir, temperature=T, dataType='power_measurement')
        print('Saving data for {}.....'.format(T))
        for dataname in tqdm(dataname_list):
            qc.save_PWRdata_from_allFolders(dataname=dataname)
# PWR_Cycle
def save_allInfo_PWRCycle_tocsv(data_input_dir='', output_dir='', temperature_list=[], dataname_list=[]):
    for T in temperature_list:
            qc = QC_analysis(datadir=data_input_dir, output_dir=output_dir, temperature=T, dataType='PWR_Cycle')
            print('Saving data from {}......'.format(T))
            for dataname in tqdm(dataname_list):
                qc.save_PWRCycle_from_allFolders(dataname=dataname)
#
#
# produce plots of PWR_Meas vs femb_id
def one_plot_PWR(csv_source_dir='', temperature='LN', data_csvname='Bias5V', data_meas='P_meas', marker='.'):
        unit_data = ''
        # ylim = []
        if data_meas=='P_meas':
            unit_data = 'W'
            # ylim = [-0.5, 6]
        elif data_meas=='I_meas':
            unit_data = 'A'
            # ylim = [-0.5, 2]
        elif data_meas=='V_meas':
            unit_data = 'V'
            # ylim = [0, 5.5]
        path_to_csv = '/'.join([csv_source_dir, temperature, data_csvname + '.csv'])
        data_df = pd.read_csv(path_to_csv)
        # get the right columns
        columns = [col for col in data_df.columns if data_meas in col]
        # selected dataframe
        selected_df = pd.concat([data_df['FEMB_ID'], data_df[columns]], axis=1)
        
        figTitle = data_meas
        #
        # figLegends follow the same order as columns
        figLegends = ['_'.join(col.split('_')[2:]) for col in columns]
        #
        # create figure
        plt.figure(figsize=(12, 7))
        plt.rcParams.update({'font.size': 15})
        for i, col in enumerate(columns):
            # calculate the mean and standard deviation
            mean = np.mean(selected_df[col])
            std = np.std(selected_df[col])
            plt.plot(selected_df['FEMB_ID'].astype(str), selected_df[col], label='__'.join([figLegends[i], 'mean = {:.3f}'.format(mean), 'std = {:.3f}'.format(std)]), 
                    marker=marker, markersize=12)
        plt.title('_'.join([figTitle, data_csvname]))
        # plt.xticks(fontsize=15)
        # plt.yticks(fontsize=15)
        plt.xlabel('FEMB_ID')
        plt.ylabel(''.join([data_meas, '(', unit_data, ')']))
        # # plt.ylim(ylim)
        plt.legend()
        try:
            os.mkdir('/'.join([csv_source_dir, temperature, 'plots']))
        except:
            pass
        plt.savefig('/'.join([csv_source_dir, temperature, 'plots', '_'.join([figTitle, data_csvname, '.png'])]))
        plt.clf() # clear figure

def all_PWR_Meas_plots(csv_source_dir='', measured_info_list=[], temperature_list=[], dataname_list=[]):
    mpl.rcParams.update({'figure.max_open_warning': 0})
    marker = '.' # add this marker to the plots
    for T in temperature_list:
        for type_data in dataname_list:
            print('Producing the plots for {}.....'.format(T))
            for meas in tqdm(measured_info_list):
                one_plot_PWR(csv_source_dir=csv_source_dir, temperature=T, data_csvname=type_data, data_meas=meas, marker=marker)


##
##
## ------ PWR Consumption -----------
def get_PWR_consumption(csv_source_dir='', temperature='LN', all_data_types=[], power='PWR_Meas'):
    '''
    PWR_consumption here is the sum of all P_meas 
    ==> We will have a dictionary for SE, SE_SDF and DIFF
    '''
    df_SE = pd.DataFrame()
    df_SE_SDF = pd.DataFrame()
    df_DIFF = pd.DataFrame()
    #----------> PWR_Meas <------------
    if power=='PWR_Meas':
        FEMB_ID = pd.Series()
        for data_csvname in all_data_types:
            path_to_csv = '/'.join([csv_source_dir, temperature, data_csvname + '.csv'])
            df = pd.read_csv(path_to_csv)
            col_id = ['FEMB_ID']
            cols = [col for col in df.columns if 'P_meas' in col] # we need the columns of Power measurement
            FEMB_ID = df[col_id]
            selected_df = df[cols]
        
            tmp_df_SE = selected_df[cols[0]]
            tmp_df_SE_SDF = selected_df[cols[1]]
            tmp_df_DIFF = selected_df[cols[2]]

            # rename the second column of the dataframe
            tmp_df_SE.columns = ['_'.join([cols[0], data_csvname])]
            tmp_df_SE_SDF.columns = ['_'.join([cols[1], data_csvname])]
            tmp_df_DIFF.columns = ['_'.join([cols[2], data_csvname])]
            df_SE = pd.concat([df_SE, tmp_df_SE], axis=1)
            df_SE_SDF = pd.concat([df_SE_SDF, tmp_df_SE_SDF], axis=1)
            df_DIFF = pd.concat([df_DIFF, tmp_df_DIFF], axis=1)
        # create df to do the sum
        final_df = pd.DataFrame(FEMB_ID)
        final_df['PWR_Cons_SE'] = df_SE.sum(axis=1)
        final_df['PWR_Cons_SE_SDF'] = df_SE_SDF.sum(axis=1)
        final_df['PWR_Cons_DIFF'] = df_DIFF.sum(axis=1)
        return final_df
    #-----------> End PWR_Meas <------------

    #--> PWR_Cycle <------
    elif power=='PWR_Cycle':
        FEMB_ID_se = pd.Series()
        FEMB_ID_sdf = pd.Series()
        for part_dataname in all_data_types:
            csvnames = [filename for filename in os.listdir('/'.join([csv_source_dir, temperature, 'PWR_Cycle'])) if part_dataname in filename]
            for csv in csvnames:
                path_to_csv = '/'.join([csv_source_dir, temperature, 'PWR_Cycle', csv])
                df = pd.read_csv(path_to_csv)
                # FEMB_ID = df['FEMB_ID']
                cols = [col for col in df.columns if 'P_meas' in col] # get the power measured
                cols.append('FEMB_ID')
                selected_df = df[cols]
                
                tmp_df_SE = pd.DataFrame()
                tmp_df_DIFF = pd.DataFrame()
                tmp_df_SE_SDF = pd.DataFrame()
                if 'SE.csv' in csv:
                    FEMB_ID_se = selected_df['FEMB_ID']
                    tmp_df_SE['_'.join([cols[0], csv.split('.')[0]])] = selected_df[cols[0]]
                    # tmp_df_SE.columns = ['_'.join([cols[0], csv.split('.')[0]])]
                    # print(tmp_df_SE.columns)
                    df_SE = pd.concat([df_SE, tmp_df_SE], axis=1)
                else:
                    FEMB_ID_sdf = selected_df['FEMB_ID']
                    tmp_df_SE_SDF['_'.join([cols[0], csv.split('.')[0]])] = selected_df[cols[0]]
                    tmp_df_DIFF['_'.join([cols[1], csv.split('.')[0]])] = selected_df[cols[1]]
                    # rename the column
                    # tmp_df_SE_SDF.columns = ['_'.join([cols[0], csv.split('.')[0]])]
                    # tmp_df_DIFF.columns = ['_'.join([cols[1], csv.split('.')[0]])]
                    df_SE_SDF = pd.concat([df_SE_SDF, tmp_df_SE_SDF], axis=1)
                    df_DIFF = pd.concat([df_DIFF, tmp_df_DIFF], axis=1)

        # create df to do the sum
        final_df_SE = pd.DataFrame(FEMB_ID_se)
        final_df_SE['PWR_Cons_SE'] = df_SE.sum(axis=1)

        final_df_others = pd.DataFrame(FEMB_ID_sdf)
        final_df_others['PWR_Cons_SE_SDF'] = df_SE_SDF.sum(axis=1)
        final_df_others['PWR_Cons_DIFF'] = df_DIFF.sum(axis=1)
        return (final_df_SE, final_df_others)
    #--------> End PWR_Cycle <--------

def plot_PWR_Consumption(csv_source_dir='', temperatures=['LN', 'RT'], all_data_types=[], output_dir='', powerType='PWR_Meas'):
    # ylim = [5, 10] # I noticed the value of the power consumption between 5W and 10W
    colors=['blue','orange','green']
    if powerType=='PWR_Meas':
        for T in temperatures:
            pwr_df = get_PWR_consumption(csv_source_dir=csv_source_dir, temperature=T, all_data_types=all_data_types)
            figname = 'power_consumption_{}'.format(T)
            tmp_output_dir = '/'.join([output_dir, T, figname])
            cols = [col for col in pwr_df.columns if col!='FEMB_ID']
            plt.figure(figsize=(12, 7))
            for i, col in enumerate(cols):
                # calculate mean and std
                mean = np.mean(pwr_df[col])
                std = np.std(pwr_df[col])
                label = '_'.join(col.split('_')[2:])
                label = '__'.join([label, 'mean = {:.3f}'.format(mean), 'std = {:.3f}'.format(std)])
                plt.plot(pwr_df['FEMB_ID'].astype(str), pwr_df[col], marker='.', markersize=12, label=label, color=colors[i])
            plt.xlabel('FEMB_ID')
            plt.ylabel('PWR_Consumption(W)')
            # plt.ylim(ylim)
            plt.title('PWR_Consumption')
            plt.legend()
            plt.savefig(tmp_output_dir + '.png')
            print('Plot of the power consumption {} saved.\n'.format(T))
            pwr_df.to_csv(tmp_output_dir + '.csv', index=False)
            print('csv file of the power consumption for {} saved.\n'.format(T))
    elif powerType=='PWR_Cycle':
        T = 'LN'
        pwr_se, pwr_sesdf_diff = get_PWR_consumption(csv_source_dir=csv_source_dir, temperature=T, all_data_types=all_data_types, power='PWR_Cycle')
        # PWR_SE
        pwr_se[['FEMB_ID', 'cycle']] = pwr_se.FEMB_ID.str.split('_', expand=True)
        # sort the dataframe by 'FEMB_ID' and cycle
        pwr_se = pwr_se.sort_values(by=['FEMB_ID', 'cycle'], ascending=True)
        pwr_se['FEMB_ID'] = pwr_se[['FEMB_ID', 'cycle']].agg('\n'.join, axis=1)
        pwr_se.drop('cycle', axis=1, inplace=True)
        # PWR_SE_SDF and PWR_DIFF
        pwr_sesdf_diff['FEMB_ID'] = pwr_sesdf_diff['FEMB_ID'].astype(str)
        pwr_sesdf_diff = pwr_sesdf_diff.sort_values(by='FEMB_ID', ascending=True)
        pwr_sesdf_diff['FEMB_ID'] = ['\n'.join([str(femb), '0']) for femb in pwr_sesdf_diff['FEMB_ID']]
        ##
        # mean and std for SE, SE_SDF and DIFF
        mean_SE = np.mean(pwr_se['PWR_Cons_SE'])
        std_SE = np.std(pwr_se['PWR_Cons_SE'])
        #
        mean_SE_SDF = np.mean(pwr_sesdf_diff['PWR_Cons_SE_SDF'])
        std_SE_SDF = np.std(pwr_sesdf_diff['PWR_Cons_SE_SDF'])
        #
        mean_DIFF = np.mean(pwr_sesdf_diff['PWR_Cons_DIFF'])
        std_DIFF = np.std(pwr_sesdf_diff['PWR_Cons_DIFF'])
        #
        # produce the plot of the power consumption
        plt.figure(figsize=(40, 10))
        ## SE
        plt.plot(pwr_se['FEMB_ID'], pwr_se['PWR_Cons_SE'], marker='.', markersize=20, color=colors[0],
                label='__'.join(['SE', 'mean = {:.3f}'.format(mean_SE), 'std = {:.3f}'.format(std_SE)]))
        plt.xticks(pwr_se['FEMB_ID'], fontsize=13)
        # SE_SDF
        plt.plot(pwr_sesdf_diff['FEMB_ID'], pwr_sesdf_diff['PWR_Cons_SE_SDF'], marker='.', markersize=20, color=colors[1],
                label='__'.join(['SE_SDF', 'mean = {:.3f}'.format(mean_SE_SDF), 'std = {:.3f}'.format(std_SE_SDF)]))
        # DIFF
        plt.plot(pwr_sesdf_diff['FEMB_ID'], pwr_sesdf_diff['PWR_Cons_DIFF'], marker='.', markersize=20, color=colors[2],
                label='__'.join(['DIFF', 'mean = {:.3f}'.format(mean_DIFF), 'std = {:.3f}'.format(std_DIFF)]))
        plt.yticks(fontsize=25);plt.yticks(fontsize=25)
        plt.xlabel('FEMB_ID\nCycle', fontsize=15)
        plt.ylabel('PWR_Consumption(W)', fontsize=20)
        plt.title('Power consumption for the PWR_Cycle', fontsize=25)
        plt.legend(fontsize=25)
        figname = 'power_consumption_{}'.format(T)
        tmp_output_dir = '/'.join([output_dir, T, 'PWR_Cycle', figname + '.png'])
        plt.savefig(tmp_output_dir)
        # save csv files
        pwr_se.to_csv('/'.join([output_dir, T, 'PWR_Cycle', 'power_consumption_SE.csv']), index=False)
        pwr_sesdf_diff.to_csv('/'.join([output_dir, T, 'PWR_Cycle', 'power_consumption_SE_SDF_DIFF.csv']), index=False)
        print('--------------FILES SAVED---------------')
        

# plot power cycle
def plot_PWR_Cycle(csv_source_dir='', measured_param='V_meas'):
    '''
    In this function, we need to combine the data of Bias_SE, Bias_SE_SDF and Bias_DIFF.
    Same for other datatypes.
    '''
    temperature = 'LN' # we only have PWR_Cycle on LN
    dataname_list = ['Bias5V', 'ColdADC', 'ColdDATA', 'LArASIC']
    colors=['blue','orange','green']
    #
    # create a folder nammed 'plots' to save the plots
    try:
        os.mkdir('/'.join([csv_source_dir, 'plots']))
    except:
        print('A folder nammed plots already exists.')
    output_dir = '/'.join([csv_source_dir, 'plots'])
    pwr_test_types = ['SE', 'SE_SDF', 'DIFF']
    for dataname in dataname_list:
        figurename = '_'.join([dataname, measured_param + '.png'])
        plt.figure(figsize=(45,7))
        for i, pwr in enumerate(pwr_test_types):
            df = pd.DataFrame()
            # figname = ''
            param_meas = '_'.join([measured_param, pwr])

            # --- START --->
            if pwr=='SE':
                figname = '_'.join([dataname, pwr])
                csvname = figname + '.csv'
                path_to_datafile = '/'.join([csv_source_dir, csvname])
                df = pd.read_csv(path_to_datafile)
                df[['FEMB_ID', 'cycle']] = df.FEMB_ID.str.split('_', expand=True)
                # sort the dataframe by 'FEMB_ID' and cycle
                df = df.sort_values(by=['FEMB_ID', 'cycle'], ascending=True)
                df['FEMB_ID'] = df[['FEMB_ID', 'cycle']].agg('\n'.join, axis=1)
                df.drop('cycle', axis=1, inplace=True)
                # calculate the mean and std of the df[param_meas]
                mean = np.mean(df[param_meas])
                std = np.std(df[param_meas])
                # plt.figure(figsize=(30, 10))
                plt.plot(df['FEMB_ID'], df[param_meas], marker='.', markersize=15, color=colors[i],
                        label='_'.join([pwr, 'mean = {:.3f}'.format(mean), 'std = {:.3f}'.format(std)]))
                plt.xticks(df['FEMB_ID'], fontsize=20);plt.yticks(fontsize=30)
                plt.xlabel('FEMB_ID\ncycle', fontsize=20)
                #
            else:
                figname = '_'.join([dataname, pwr])
                csvname = '_'.join([dataname, 'SE_SDF_DIFF']) + '.csv'
                path_to_datafile = '/'.join([csv_source_dir, csvname])
                df = pd.read_csv(path_to_datafile)
                # sort the dataframe by 'FEMB_ID'
                df['FEMB_ID'] = df['FEMB_ID'].astype(str)
                df = df.sort_values(by='FEMB_ID', ascending=True)
                df['FEMB_ID'] = ['\n'.join([str(femb), '0']) for femb in df['FEMB_ID']]
                # calculate the mean and std of the df[param_meas]
                mean = np.mean(df[param_meas])
                std = np.std(df[param_meas])
                #
                plt.plot(df['FEMB_ID'].astype(str), df[param_meas], marker='.', markersize=20, color=colors[i],
                        label='_'.join([pwr, 'mean = {:.3f}'.format(mean), 'std = {:.3f}'.format(std)]))
            # <------ END ----
            unit = ''
            if measured_param=='I_meas':
                unit = 'A'
            elif measured_param=='P_meas':
                unit='W'
            elif measured_param=='V_meas':
                unit='V'
            plt.ylabel(measured_param + '({})'.format(unit), fontsize=30)
            plt.title('_'.join([measured_param, dataname]), fontsize=30)
            plt.legend(fontsize=30)
            plt.savefig('/'.join([output_dir, figurename]))
            
#----------------------------------------------------------------------------
class ASICDAC:
    def __init__(self, input_data_dir='', output_dir='', temperature='LN', CALI_number=1, sgp1=False):
        '''
            input_data_dir: path to the list of data folders,
            CALI_number: can be 1, 2, 3 or 4,
            temperature: can be LN or RT
        '''
        self.sgp1 = False
        self.step = 4
        if sgp1:
            self.sgp1 = True
            self.step = 1
        self.config = []
        self.CALI = 'CALI{}'.format(CALI_number)
        #
        # self.input_dir = input_data_dir # this variable will be used to get the informations in logs_env.bin
        try:
            os.mkdir('/'.join([output_dir, temperature]))
        except:
            pass
        try:
            os.mkdir('/'.join([output_dir, temperature, self.CALI]))
        except:
            print('Folder already exists.....')
        self.output_dir = '/'.join([output_dir, temperature, self.CALI]) # this variable will be used to save the output of the code
        #
        self.temperature = temperature
        self.input_dir_list = ['/'.join([input_data_dir, data_folder, self.CALI]) for data_folder in os.listdir(input_data_dir) if self.temperature in data_folder]
        #
        # variable to store the data in a dataframe
        self.data_df = pd.DataFrame()
    
    def list_bin(self, input_dir='', BL=200, gain=4.7, shapingTime=2.0):
        str_BL = str(BL) + 'mVBL'
        str_gain = '_'.join(str(gain).split('.')) + 'mVfC'
        str_shapingTime = '_'.join(str(shapingTime).split('.')) + 'us'
        #
        all_bins_in_CALI = os.listdir(input_dir)
        # get the bin files matching the configuration
        match_bin_files = []
        for f in all_bins_in_CALI:
            for i in range(0, 64, self.step):
                part_of_filename = '_'.join([str_BL, str_gain, str_shapingTime, '{}'.format(hex(i))])
                if part_of_filename in f:
                    match_bin_files.append(f)    
                continue
        return match_bin_files

    def decode_onebin(self, path_to_binFolder='', bin_filename=''): #, femb_number=0):
        '''
        This function returns the value of the DAC corresponding to the bin file and
        an array of the peak values for all channels in the bin file.
        '''
        path_to_bin = '/'.join([path_to_binFolder, bin_filename])
        # read bin
        with open(path_to_bin, 'rb') as fp:
            raw = pickle.load(fp)
        rawdata = raw[0]
        # pwr_meas = raw[1]
        # data decoding <-- same as in QC_tools
        qc = QC_tools()
        pldata = qc.data_decode(rawdata)
        pldata = np.array(pldata, dtype=object)
        ##
        nevent = len(pldata)
        #
        # get the value of DAC
        tmp = (bin_filename.split('_')[-1]).split('.')[0]
        if tmp=='sgp1':
            tmp = (bin_filename.split('_')[-2]).split('.')[0]
            self.sgp1 = True
        hex = tmp
        DAC = int(hex, base=16)
        #
        # instead of returning all data, let's directly get the peak value
        all_peak_values = []
        for femb_number in [0, 1, 2, 3]:
            print('nfemb  = {}'.format(femb_number))
            peak_values = []
            for ich in tqdm(range(128)):
                iich = femb_number*128+ich
                first_peak = False
                # only get the first event
                for iev in range(nevent):
                    pos_peaks, _ = find_peaks(pldata[iev][iich], height=np.amax(pldata[iev][iich]))
                    for ppeak in pos_peaks:
                        startpos = ppeak - 50
                        # go to the next pulse if the starting position is negative
                        if startpos<0:
                            continue
                        endpos = startpos + 100
                        peak_values.append(np.max(pldata[iev][iich][startpos:endpos]))
                        first_peak = True
                        break
                    if first_peak:
                        first_peak = False
                        break
            all_peak_values.append((DAC, peak_values))
        # I expect to get the DAC value and an array of length 128 where each element is a value of one peak for each channel
        # return DAC, all_peak_values
        return all_peak_values

    def get_peakValues_forallDAC(self, path_to_binfolder='', config=[200,  14.0, 2.0], withlogs=False):
        # all_data_dict = {}
        self.config = config
        list_binfiles = self.list_bin(input_dir=path_to_binfolder, BL=self.config[0], gain=self.config[1], shapingTime=self.config[2])
        #
        data_list = []
        for ibin in range(len(list_binfiles)):
            # tmpDAC, tmpPeak_values = self.decode_onebin(path_to_binFolder=path_to_binfolder, bin_filename=list_binfiles[ibin], femb_number=femb_number)
            data_list.append(self.decode_onebin(path_to_binFolder=path_to_binfolder, bin_filename=list_binfiles[ibin]))
        
        FEMBs = [0, 1, 2, 3]
        for femb_number in FEMBs:
            all_data_dict = {}
            for ibin in range(len(list_binfiles)):
                DAC = data_list[ibin][femb_number][0]
                peak_values = data_list[ibin][femb_number][1]
                all_data_dict[DAC] = peak_values
            #
            DACs, peaks, CHs = [], [], []
            for dac, peak_array in all_data_dict.items():
                tmp_dac = [dac for _ in range(len(peak_array))]
                tmp_peaks_values = peak_array
                ch_numbers = [i for i in range(len(peak_array))]
                DACs += tmp_dac
                peaks += tmp_peaks_values
                CHs += ch_numbers
            transformed_data_df = pd.DataFrame({
                'CH': CHs,
                'peak_value': peaks,
                'DAC': DACs
            })
            self.data_df = pd.DataFrame()
            self.data_df = transformed_data_df
            
            # get the femb_id if withlogs
            femb_id = femb_number
            if withlogs:
                dir_to_logs = '/'.join(path_to_binfolder.split('/')[:-1])
                with open('/'.join([dir_to_logs, 'logs_env.bin']), 'rb') as pointer_logs:
                    info_logs = pickle.load(pointer_logs)
                #  get the list of femb_ids
                femb_ids = info_logs['femb id']
                femb_id = femb_ids['femb{}'.format(femb_number)]
            config1 = '_'.join(str(self.config[1]).split('.'))
            config2 = '_'.join(str(self.config[2]).split('.'))
            csvname = 'peakValues_femb{}_{}mVBL_{}mVfC_{}us'.format(femb_id, self.config[0], config1, config2)
            if self.sgp1:
                csvname += '_sgp1'
            self.data_df.to_csv('/'.join([self.output_dir, csvname + '.csv']), index=False)
        
    #================ use data_df from this part------no need to read the data bin files except logs_env.bin===========
    def plot_peakValue_vs_DAC_allch(self, data_df, ch_list=range(128)):
        '''
        Run get_peakValues_forallDAC before using this method
        '''
        plt.figure(figsize=(12, 7))
        for ch in ch_list:
            # self.plot_peakValue_vs_DAC(plt, ch_number=ch)
            df_for_ch = data_df[data_df['CH']==ch].reset_index()
            df_for_ch['DAC'] = df_for_ch['DAC'].astype(int)
            df_for_ch = df_for_ch.sort_values(by='DAC', ascending=True)
            # title = self.checkLinearity(DAC_values=df_for_ch['DAC'], peak_values=df_for_ch['peak_value'])
            starting_of_nonlinearity = self.checkLinearity(DAC_values=df_for_ch['DAC'], peak_values=df_for_ch['peak_value'])
            slope, y0 = np.polyfit(df_for_ch['DAC'][:starting_of_nonlinearity[0]+1], df_for_ch['peak_value'][:starting_of_nonlinearity[0]+1], 1)
            y_pred = np.array(df_for_ch['DAC'] * slope) + y0

            plt.plot(df_for_ch['DAC'], df_for_ch['peak_value'])
            plt.plot(df_for_ch['DAC'], y_pred, label='ch{}'.format(ch))
            # plt.title(title)
        plt.legend()
        # plt.show()
        plt.savefig('/'.join([self.output_dir, 'testfit.png']))

    def checkLinearity(self, DAC_values=[], peak_values=[]):
        peak_values = np.array(peak_values)
        DAC_values = np.array(DAC_values)
        y_max = peak_values[-1]
        #-> if y_max == peak_values[-2], maybe there's saturation
        ## fit the two points with a line and calculate y_pred
        index = -1
        # if y_max == peak_values[-2]:
        if np.abs(y_max - peak_values[-2]) <= 0.001:
            y_pred = []
            slope, y0 = np.polyfit(DAC_values[-2:], peak_values[-2:], 1)
            y_pred = DAC_values * slope + y0
            # find the last (last to start) value where y_true[i] - y_pred[i] != 0
            for i in range(len(peak_values)-1, -1, -1):
                if (np.abs(peak_values[i] - y_pred[i])/(peak_values[-1]-peak_values[0])) > 0.001:
                    index = i
                    break
        return index, DAC_values[index], peak_values[index]
        

    def get_gains(self, path_to_binfolder='', femb_number=0, config=[200, 14.0, 2.0], withlogs=False):
        self.config = config
        # get the femb_id if withlogs
        femb_id = femb_number
        if withlogs:
            dir_to_logs = '/'.join(path_to_binfolder.split('/')[:-1])
            with open('/'.join([dir_to_logs, 'logs_env.bin']), 'rb') as pointer_logs:
                info_logs = pickle.load(pointer_logs)
            #  get the list of femb_ids
            femb_ids = info_logs['femb id']
            femb_id = femb_ids['femb{}'.format(femb_number)]
        config1 = '_'.join(str(self.config[1]).split('.'))
        config2 = '_'.join(str(self.config[2]).split('.'))
        peak_csvname = 'peakValues_femb{}_{}mVBL_{}mVfC_{}us'.format(femb_id, self.config[0], config1, config2)
        if self.sgp1:
            peak_csvname += '_sgp1'
        #
        # read the csv file in a dataframe
        self.data_df = pd.read_csv('/'.join([self.output_dir, peak_csvname + '.csv']))
        # self.get_peakValues_forallDAC(path_to_binfolder=path_to_binfolder, config=config, femb_number=femb_number)
        #
        #
        dac_v = {} # mV/bit
        dac_v['4_7mVfC'] = 18.66
        dac_v['7_8mVfC'] = 14.33
        dac_v['14_0mVfC'] = 8.08
        dac_v['25_0mVfC'] = 4.61

        CC = 1.85*pow(10, -13)
        e = 1.602*pow(10, -19) # electron charge

        sgs = '_'.join(str(config[1]).split('.')) + 'mVfC'

        if self.sgp1:
            dac_du = dac_v['4_7mVfC']
        else:
            dac_du = dac_v[sgs]
        #
        #
        CHs = []
        Gains = []
        starting_of_nonlinearity = (0, 0, 0)

        #
        # DAC_indices = []
        # peak_max = []
        #
        DAC_for_peakmax = []
        for ich in self.data_df['CH'].unique():
        # for ich in [0, 1, 2]:
            df_for_ch = self.data_df[self.data_df['CH']==ich].reset_index()
            df_for_ch['DAC'] = df_for_ch['DAC'].astype(int)
            df_for_ch = df_for_ch.sort_values(by='DAC', ascending=True)
            starting_of_nonlinearity = self.checkLinearity(DAC_values=df_for_ch['DAC'], peak_values=df_for_ch['peak_value'])
            slope, y0 = np.polyfit(df_for_ch['DAC'][:starting_of_nonlinearity[0]+1], df_for_ch['peak_value'][:starting_of_nonlinearity[0]+1], 1)
            #
            # DAC value corresponding to peak_max
            DAC_for_peakmax.append(starting_of_nonlinearity[1])
            #
            # DAC_indices.append(starting_of_nonlinearity[1])
            # peak_max.append(starting_of_nonlinearity[2])
            #
            # convert gain to ADC bin/electron
            slope = 1/slope * dac_du/1000 * CC/e
            if slope < 0:
                slope = 0
            CHs.append(ich)
            Gains.append(slope)
        #
        tmp_gains_figname = peak_csvname.split('_')
        tmp_gains_figname[0] = 'gains'
        gains_figname = '_'.join(tmp_gains_figname)
        # GAIN
        plt.figure(figsize=(20,12))
        plt.plot(CHs, Gains, marker='.', markersize=7)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)
        plt.xlabel('CH', fontsize=20)
        # plt.ylabel('Gain(ADC bin/electron)', fontsize=20)
        plt.ylabel('Gain(ADC bin)', fontsize=20)
        plt.xlim([-1, 128])
        plt.savefig('/'.join([self.output_dir, gains_figname + '.png']))
        #
        # DAC corresponding to peak_max
        plt.figure(figsize=(12, 7))
        plt.plot(CHs, DAC_for_peakmax, marker='.', markersize=7)
        plt.xlabel('CH');plt.ylabel('DAC_for_peakmax')
        plt.savefig('/'.join([self.output_dir, '_'.join([gains_figname, 'DAC_peakmax', '.png'])]))
        print('Figures saved....')
        #
        # save the Gains in a csv file
        gain_df = pd.DataFrame({'CH': self.data_df['CH'].unique(), 'Gain': Gains, 'DAC_peakmax': DAC_for_peakmax})
        gain_df.to_csv('/'.join([self.output_dir, gains_figname + '.csv']), index=False)
        print('Gains saved in a csv file at {}'.format(self.output_dir))
        
    def get_gains_for_allFEMBs(self, path_to_binfolder='', config=[200, 14.0, 2.0], withlogs=False):
        nFEMBs = [0, 1, 2, 3]
        # nFEMBs = [0]
        for nfemb in nFEMBs:
            print('femb_number = {}...'.format(nfemb))
            self.get_gains(path_to_binfolder=path_to_binfolder, femb_number=nfemb, config=config, withlogs=withlogs)

def Gains_CALI1(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=1, sgp1=False)
    mVfC = [4.7, 7.8, 14.0, 25.0]
    for data_dir in asic.input_dir_list:
        for gain_in_mVfC in mVfC:
            asic.get_gains_for_allFEMBs(path_to_binfolder=data_dir, config=[200, gain_in_mVfC, 2.0], withlogs=withlogs)

def Gains_CALI2(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=2, sgp1=False)
    config = [900, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        asic.get_gains_for_allFEMBs(path_to_binfolder=data_dir, config=config, withlogs=withlogs)

def Gains_CALI3_or_CALI4(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False, CALI_number=3):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=True)
    config = [200, 14.0, 2.0]
    if CALI_number==4:
        config = [900, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        asic.get_gains_for_allFEMBs(path_to_binfolder=data_dir, config=config, withlogs=withlogs)
            

def save_peakValues_to_csv(path_to_dataFolder='', output_dir='', temperature='LN', withLogs=False, CALI_number=3):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=True)
    config = [200, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        asic.get_peakValues_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withLogs)

##---------------------------------------------------------------------------
##
if __name__ == '__main__':
	#------maybe we will not use this part ----------------
    #qc = QC_analysis(datadir='D:/IO-1865-1C/QC/data/', output_dir='D:/IO-1865-1C/QC/analysis', temperature='LN')
    #qc.save_PWRdata_from_allFolders(dataname='Bias5V')
    #qc.save_PWRdata_from_allFolders(dataname='LArASIC')
    #qc.save_PWRdata_from_allFolders(dataname='ColdDATA')
    #qc.save_PWRdata_from_allFolders(datafemb106_femb114_femb111_LN_0pF_R002name='ColdADC')
    #------------------------------------------------------
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    #temperatures = ['LN', 'RT']
    temperatures = ['LN']
    dataname_list = ['Bias5V', 'LArASIC', 'ColdDATA', 'ColdADC']
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
    Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True, CALI_number=3)
    #Gains_CALI3_or_CALI4(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True, CALI_number=4)
    #Gains_CALI1(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True)
    #Gains_CALI2(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN', withlogs=True)
    # save_peakValues_to_csv(path_to_dataFolder=inputdir, output_dir=savedir, temperature='LN',
    #                     withLogs=True, CALI_number=3)