# outputdir : D:/IO-1865-1C/QC/analysis
# datadir : D:/IO-1865-1C/QC/data/..../PWR_Meas
import sys
sys.path.append('..')
import os
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm
from QC_tools import QC_tools

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
        # save the path to the output
        self.output_analysis_dir = '/'.join([output_dir, temperature])
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
        # check if a folder named PWR_Meas exists --> if self.particularDataFolderName exists
        new_data_dir = []
        for onefolder in os.listdir(datadir):
            if (temperature in onefolder) & (self.particularDataFolderName in os.listdir('/'.join([datadir, onefolder]))):
                new_data_dir.append('/'.join([datadir, onefolder, self.particularDataFolderName]))
        self.input_data_dir = new_data_dir
        #self.input_data_dir = ['/'.join([datadir, onefolder, self.particularDataFolderName]) for onefolder in os.listdir(datadir) if temperature in onefolder]
        self.bin_filenames = os.listdir(self.input_data_dir[0]) ## the *.bin filenames are the same for all the folders

    def read_bin(self, filename, input_data_dir):
        with open(os.path.join(input_data_dir, filename), 'rb') as fp:
            if self.particularDataFolderName=='PWR_Meas':
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
        for inputdatadir in self.input_data_dir:
            for binfile in tqdm(self.bin_filenames):
                csv_name = '_'.join([ binfile, '.csv'])
                # try to create a folder having the same name as the data_folder
                try:
                    os.mkdir('/'.join([self.output_analysis_dir, inputdatadir.split('/')[-2]]))
                except:
                    # print('----Error when creating the folder....')
                    pass
                outputdir = '/'.join([self.output_analysis_dir, inputdatadir.split('/')[-2]])
                # try to create folders for RMS and Pedestal
                for d in ['RMS', 'Pedestal']:
                    try:
                        os.mkdir('/'.join([outputdir, d]))
                    except:
                        pass
                rms_dict, ped_dict = self.read_bin(filename=binfile, input_data_dir=inputdatadir)
                rms_df = pd.DataFrame(rms_dict)
                ped_df = pd.DataFrame(ped_dict)
                # save in csv at self.output_analysis_dir
                rms_df.to_csv('/'.join([outputdir, 'RMS', csv_name]), index=False)
                ped_df.to_csv('/'.join([outputdir, 'Pedestal', csv_name]), index=False)

    def get_oneData_PWR(self, sourceDataDir='', powerTestType_with_BL='SE_200mVBL', dataname='bias'):
        '''----Help section-----'''
        # read the logs_env.bin file to get the informations about the femb#, temperature, note
        logs_dir = sourceDataDir.split('/')[:-1]
        #print('/'.join(logs_dir))
        with open('/'.join(['/'.join(logs_dir), 'logs_env.bin']), 'rb') as fp:
            logs_env = pickle.load(fp)
        #
        # get the filename to be used
        file_to_be_used = ''
        for f in self.bin_filenames:
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
        for femb in femb_numbers:
            #femb_ids.append('_'.join(['fembID_', logs_env['femb id'][femb]]))
            femb_ids.append(logs_env['femb id'][femb])

        return (title, dirname, femb_ids, V_meas, I_meas, P_meas)

    def save_PWRdata_from_allFolders(self, dataname='bias'):
        pwr_test_types = ['SE_200mVBL', 'SE_SDF_200mVBL', 'DIFF_200mVBL']

        title = ''
        all_femb_ids = []
        out_df = pd.DataFrame()
        for pwr in pwr_test_types:
            femb_ids, V_meas, I_meas, P_meas = [], [], [], []
            for inputdir_name in self.input_data_dir:
                tmp_title, tmp_dirname, tmp_femb_ids, tmp_V_meas, tmp_I_meas, tmp_P_meas = self.get_oneData_PWR(sourceDataDir=inputdir_name, powerTestType_with_BL=pwr, dataname=dataname)
                V_meas += tmp_V_meas
                I_meas += tmp_I_meas
                P_meas += tmp_P_meas
                femb_ids += tmp_femb_ids
                title = tmp_title
            #csv_name = '_'.join([title, '.csv'])
            tmp_out_df = pd.DataFrame({
                #'FEMB_ID_': [femb.split('_')[-1] for femb in femb_ids],
                'V_meas_'+'_'.join(pwr.split('_')[:-1]): V_meas,
                'I_meas_'+'_'.join(pwr.split('_')[:-1]): I_meas,
                'P_meas_'+'_'.join(pwr.split('_')[:-1]): P_meas})
            out_df = pd.concat([out_df, tmp_out_df], axis=1)
            all_femb_ids = femb_ids
        all_femb_ids = [femb for femb in all_femb_ids]
        final_df = pd.DataFrame({'FEMB_ID': all_femb_ids})
        final_df = pd.concat([final_df, out_df], axis=1)
        final_df['FEMB_ID'] = final_df.FEMB_ID.astype(str)
        csv_name = dataname + '.csv'
        final_df.to_csv('/'.join([self.output_analysis_dir, csv_name]), index=False)

# save all informations from the *.bin files to csv
def save_allInfo_tocsv(data_input_dir='', output_dir='', temperature_list=[], dataname_list=[]):
    for T in temperature_list:
        qc = QC_analysis(datadir=data_input_dir, output_dir=output_dir, temperature=T)
        print('Saving data for {}.....'.format(T))
        for dataname in tqdm(dataname_list):
            qc.save_PWRdata_from_allFolders(dataname=dataname)
#
#
# produce plots of PWR_Meas vs femb_id
def one_plot_PWR(csv_source_dir='', temperature='LN', data_csvname='Bias5V', data_meas='P_meas', marker='.'):
        csv_dir = '/'.join([csv_source_dir, temperature, data_csvname + '.csv'])
        data_df = pd.read_csv(csv_dir)
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
        plt.figure(figsize=(30, 20))
        plt.rcParams.update({'font.size': 12})
        for i, col in enumerate(columns):
            plt.plot(selected_df['FEMB_ID'].astype(str), selected_df[col], label=figLegends[i], marker=marker, markersize=12)
        plt.title(figTitle)
        plt.xlabel('FEMB_ID')
        plt.ylabel(data_meas)
        plt.legend()
        try:
            os.mkdir('/'.join([csv_source_dir, temperature, 'plots']))
        except:
            pass
        plt.savefig('/'.join([csv_source_dir, temperature, 'plots', '_'.join([figTitle, data_csvname, '.png'])]))
        plt.clf() # clear figure

def all_plots(csv_source_dir='', measured_info_list=[], temperature_list=[], dataname_list=[]):
    mpl.rcParams.update({'figure.max_open_warning': 0})
    marker = '.' # add this marker to the plots
    for T in temperature_list:
        for type_data in dataname_list:
            print('Producing the plots for {}.....'.format(T))
            for meas in tqdm(measured_info_list):
                one_plot_PWR(csv_source_dir=csv_source_dir, temperature=T, data_csvname=type_data, data_meas=meas, marker=marker)

if __name__ == '__main__':
	#------maybe we will not use this part ----------------
    #qc = QC_analysis(datadir='D:/IO-1865-1C/QC/data/', output_dir='D:/IO-1865-1C/QC/analysis', temperature='LN')
    #qc.save_PWRdata_from_allFolders(dataname='Bias5V')
    #qc.save_PWRdata_from_allFolders(dataname='LArASIC')
    #qc.save_PWRdata_from_allFolders(dataname='ColdDATA')
    #qc.save_PWRdata_from_allFolders(datafemb106_femb114_femb111_LN_0pF_R002name='ColdADC')
    #------------------------------------------------------
    measured_info = ['P_meas', 'V_meas', 'I_meas']
    temperatures = ['LN', 'RT']
    types_of_data = ['Bias5V', 'LArASIC', 'ColdDATA', 'ColdADC']
    #-----------This is a group ---------------------------
    # save data in csv file
    save_allInfo_tocsv(data_input_dir='D:/IO-1865-1C/QC/data', output_dir='D:/IO-1865-1C/QC/analysis', temperature_list=temperatures, dataname_list=types_of_data)
    #
    # produce all the plots
    all_plots(csv_source_dir='D:/IO-1865-1C/QC/analysis', measured_info_list=measured_info, temperature_list=temperatures, dataname_list=types_of_data)
    #-----------------------------------------------------
    #------Save RMS in csv files-------------------------
    for T in temperatures:
        qc = QC_analysis(datadir='D:/IO-1865-1C/QC/data', output_dir='D:/IO-1865-1C/QC/analysis', temperature=T, dataType='RMS')
        qc.save_rms_pedestal_to_csv()
