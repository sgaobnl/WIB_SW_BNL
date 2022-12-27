#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 12/27/2022
#----------------------------------------------------------------------

from importlib.resources import path
from tkinter import Listbox
from QC_analysis import rms
from Analysis_FEMB_QC import get_gaussPdf
from utils import *

#----------------------------------------------------------------------------
class ASICDAC:
    def __init__(self, input_data_dir='', output_dir='', temperature='LN', CALI_number=1, sgp1=False, fembs_to_ignore={}):
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
        self.output_dirCALI = '/'.join([output_dir, temperature, self.CALI]) # this variable will be used to save the output of the code
        #
        self.temperature = temperature
        self.input_dirCALI_list = ['/'.join([input_data_dir, data_folder, self.CALI]) for data_folder in os.listdir(input_data_dir) if self.temperature in data_folder]
        # dir to get RMS
        self.input_dirRMS_list = ['/'.join([input_data_dir, data_folder, 'RMS']) for data_folder in os.listdir(input_data_dir) if self.temperature in data_folder]
        #
        # variable to store the data in a dataframe
        self.peakdata_df = pd.DataFrame()
        #
        # use QC_analysis to get rms instead of writing a new function
        # self.qc_analysis = QC_analysis(self, datadir=input_data_dir, output_dir=output_dir,
        #                                 temperature=self.temperature, dataType='RMS')
        self.fembs_to_ignore = fembs_to_ignore
    
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
    
    def get_DAC_fromfilename(self, bin_filename=''):
        # get the value of DAC
        tmp = (bin_filename.split('_')[-1]).split('.')[0]
        if tmp=='sgp1':
            tmp = (bin_filename.split('_')[-2]).split('.')[0]
            self.sgp1 = True
        hex = tmp
        DAC = int(hex, base=16)
        return DAC

    def get_pkDAC_from_decodebin(self, pldata, nevent, bin_filename='', femb_numbers=[0, 1, 2, 3]):
        DAC = self.get_DAC_fromfilename(bin_filename=bin_filename)
        print('DAC = {}'.format(DAC))
        #
        # instead of returning all data, let's directly get the peak value
        all_peak_values = []
        for femb_number in tqdm(femb_numbers):
            # print('nfemb  = {}'.format(femb_number))
            peak_values = []
            # for ich in tqdm(range(128)):
            for ich in range(128):
                iich = femb_number*128+ich
                first_peak_found = False
                
                #allpls = np.empty(0)
                allpls = []

                # only get the first event
                for iev in range(nevent):
                    pos_peaks, _ = find_peaks(pldata[iev][iich], height=np.amax(pldata[iev][iich])-100)
                    if not first_peak_found:
                        for ppeak in pos_peaks:
                            startpos = ppeak - 50
                            # go to the next pulse if the starting position is negative
                            if startpos<0:
                                # print('pos_peaks = {}'.format(pos_peaks))
                                continue
                            endpos = startpos + 100
                            selected_peak = np.max(pldata[iev][iich][startpos:endpos])
                            peak_values.append(selected_peak)
    
                            first_peak_found = True
                            break
                    else:
                        break
            # append DAC and peak_values for one femb
            all_peak_values.append((DAC, peak_values))
        return all_peak_values

    def decode_onebin_peakvalues(self, path_to_binFolder='', bin_filename='', logs_env=dict()): #, femb_number=0):
        '''
        This function returns the value of the DAC corresponding to the bin file and
        an array of the peak values for all channels in the bin file.
        '''
        # get DAC
        DAC = self.get_DAC_fromfilename(bin_filename=bin_filename)

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
        all_peak_values = []
        rms_dict, ped_dict = {}, {}
        if DAC==0:
            rms_dict, ped_dict = rms(pldata=pldata, nevent=nevent, nfembs=[0, 1, 2, 3], logs_env=logs_env)
            return rms_dict, ped_dict
        else:
            # all_peak_values = self.get_pkDAC_from_decodebin(pldata=pldata, nevent=nevent, bin_filename=bin_filename, femb_numbers=[0, 1, 2, 3])
            all_peak_values = []
            femb_numbers = [0, 1, 2, 3]
            for femb_number in tqdm(femb_numbers):
                # print('nfemb  = {}'.format(femb_number))
                peak_values = []
                # for ich in tqdm(range(128)):
                for ich in range(128):
                    iich = femb_number*128+ich
                    first_peak_found = False
                    
                    #allpls = np.empty(0)
                    allpls = []

                    # only get the first event
                    for iev in range(nevent):
                        pos_peaks, _ = find_peaks(pldata[iev][iich], height=np.amax(pldata[iev][iich])-100)
                        if not first_peak_found:
                            for ppeak in pos_peaks:
                                startpos = ppeak - 50
                                # go to the next pulse if the starting position is negative
                                if startpos<0:
                                    # print('pos_peaks = {}'.format(pos_peaks))
                                    continue
                                endpos = startpos + 100
                                selected_peak = np.max(pldata[iev][iich][startpos:endpos])
                                peak_values.append(selected_peak)
        
                                first_peak_found = True
                                break
                        else:
                            break
                # append DAC and peak_values for one femb
                all_peak_values.append((DAC, peak_values))
            return all_peak_values
        # I expect to get the DAC value and an array of length 128 where each element is a value of one peak for each channel
        # return all_peak_values, rms_dict, ped_dict
        # return all_peak_values

    def get_peakValues_forallDAC(self, path_to_binfolder='', config=[200,  14.0, 2.0], withlogs=False):
        # all_peakdata_dict = {}
        self.config = config
        config1 = '_'.join(str(self.config[1]).split('.'))
        config2 = '_'.join(str(self.config[2]).split('.'))
        list_binfiles = self.list_bin(input_dir=path_to_binfolder, BL=self.config[0], gain=self.config[1], shapingTime=self.config[2])
        #
        logs_env = dict()
        if withlogs:
            dir_to_logs = '/'.join(path_to_binfolder.split('/')[:-1])
            with open('/'.join([dir_to_logs, 'logs_env.bin']), 'rb') as pointer_logs:
                info_logs = pickle.load(pointer_logs)
                logs_env = info_logs
        #
        peakdata_list = []
        rms_data, ped_data = {}, {}
        new_bin_files = []
        for ibin in range(len(list_binfiles)):
            # tmpDAC, tmpPeak_values = self.decode_onebin_peakvalues(path_to_binFolder=path_to_binfolder, bin_filename=list_binfiles[ibin], femb_number=femb_number)
            # peak_data = self.decode_onebin_peakvalues(path_to_binFolder=path_to_binfolder, 
            #                                                                     bin_filename=list_binfiles[ibin], logs_env=logs_env)
            DAC = self.get_DAC_fromfilename(bin_filename=list_binfiles[ibin])
            if DAC == 0:
                datafolder_name = path_to_binfolder.split('/')[-2] # gets the name of the data folder
                rms_dict, _ = self.decode_onebin_peakvalues(path_to_binFolder=path_to_binfolder, 
                                                                                bin_filename=list_binfiles[ibin], logs_env=logs_env)
                rms_csvname = 'rms_{}_{}mVBL_{}mVfC_{}us'.format(datafolder_name, self.config[0], config1, config2)
                if self.sgp1:
                    rms_csvname += '_sgp1'
                # print(rms_data)
                rms_dict_df = pd.DataFrame(rms_dict)
                # print(rms_dict_df.head())
                #
                input_datadirname = '_'.join(path_to_binfolder.split('/')[-2].split('_')[:-2])
                tt = [k for k, v in self.fembs_to_ignore.items() if k == input_datadirname]
                if len(tt) == 1:
                        _femb_ids = self.fembs_to_ignore[tt[0]]
                        for _femb_id in _femb_ids:
                            rms_dict_df = rms_dict_df[rms_dict_df['femb_ids'] != _femb_id]
                #
                rms_dict_df.to_csv('/'.join([self.output_dirCALI, rms_csvname + '.csv']), index=False)
            else:
                peak_data = self.decode_onebin_peakvalues(path_to_binFolder=path_to_binfolder, 
                                                                                bin_filename=list_binfiles[ibin], logs_env=logs_env)
                peakdata_list.append(peak_data)
                new_bin_files.append(list_binfiles[ibin])
            # peak_data, tmprms_data, tmpped_data = self.decode_onebin_peakvalues(path_to_binFolder=path_to_binfolder, 
            #                                                                     bin_filename=list_binfiles[ibin], logs_env=logs_env)
            # peakdata_list.append(peak_data)
            # if tmprms_data == {}:
            #     print(tmprms_data)
            # if tmprms_data != {}:
            #     rms_data = tmprms_data
            #     ped_data = tmpped_data
            #     rms_csvname = 'rms_{}mVBL_{}mVfC_{}us'.format(self.config[0], config1, config2)
            #     if self.sgp1:
            #         rms_csvname += '_sgp1'
            #     # print(rms_data)
            #     pd.DataFrame(rms_data).to_csv('/'.join([self.output_dirCALI, rms_csvname + '.csv']), index=False)
        
        # if DAC == 0, rms_data != {}
        # if rms_data != {}:
        #     # save rms in csv
        #     rms_csvname = 'rms_{}mVBL_{}mVfC_{}us'.format(self.config[0], config1, config2)
        #     if self.sgp1:
        #         rms_csvname += '_sgp1'
        #     print(rms_data)
        #     pd.DataFrame(rms_data).to_csv('/'.join([self.output_dirCALI, rms_csvname + '.csv']), index=False)

        FEMBs = [0, 1, 2, 3]
        for femb_number in FEMBs:
            #
            skip = False
            input_datadirname = '_'.join(path_to_binfolder.split('/')[-2].split('_')[:-2])
            # print(input_datadirname)
            tt = [k for k, v in self.fembs_to_ignore.items() if k == input_datadirname]
            # print(self.fembs_to_ignore.keys())
            if len(tt) == 1:
                _femb_ids = self.fembs_to_ignore[tt[0]]
                for _femb_id in _femb_ids:
                    if _femb_id == info_logs['femb id']['femb{}'.format(femb_number)]:
                        skip = True
                        print('FEMB to skip = {}'.format(_femb_id))
            #
            if not skip:
                all_peakdata_dict = {}
                # for ibin in range(len(list_binfiles)):
                for ibin in range(len(new_bin_files)):
                    # all_rmspeakdata_list.append(peakdata_list[ibin][0][femb_number])

                    # DAC = peakdata_list[ibin][femb_number][0]
                    DAC = self.get_DAC_fromfilename(bin_filename=new_bin_files[ibin])
                    if DAC!=0:
                        # DAC = peakdata_list[ibin][femb_number][0]
                        peak_values = peakdata_list[ibin][femb_number][1]
                        all_peakdata_dict[DAC] = peak_values
                #
                # peak and DAC
                DACs, peaks, CHs = [], [], []
                for dac, peak_array in all_peakdata_dict.items():
                    tmp_dac = [dac for _ in range(len(peak_array))]
                    tmp_peaks_values = peak_array
                    ch_numbers = [i for i in range(len(peak_array))]

                    DACs += tmp_dac
                    peaks += tmp_peaks_values
                    CHs += ch_numbers

                
                transformed_peakdata_df = pd.DataFrame({
                    'CH': CHs,
                    'peak_value': peaks,
                    'DAC': DACs
                })
                self.peakdata_df = pd.DataFrame()
                self.peakdata_df = transformed_peakdata_df

                # get the femb_id if withlogs
                femb_id = femb_number
                if withlogs:
                    #  get the list of femb_ids
                    femb_ids = info_logs['femb id']
                    femb_id = femb_ids['femb{}'.format(femb_number)]
                peak_csvname = 'peakValues_femb{}_{}mVBL_{}mVfC_{}us'.format(femb_id, self.config[0], config1, config2)
                
                if self.sgp1:
                    peak_csvname += '_sgp1'
                # save peakdata with DAC in csv
                self.peakdata_df.to_csv('/'.join([self.output_dirCALI, peak_csvname + '.csv']), index=False)
                #
                # print this line instead of a progessbar
                print('saved in {}/{}.csv'.format(self.CALI, peak_csvname))
        
    #================ use data_df from this part------no need to read the data bin files except logs_env.bin===========
    def plot_peakValue_vs_DAC_allch(self, data_df, figname='', ch_list=range(128)):
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
        plt.title(figname)
        plt.legend()
        # plt.show()
        plt.savefig('/'.join([self.output_dirCALI, '{}.png'.format(figname)]))
        plt.close()

    # def checkLinearity(self, DAC_values=[], peak_values=[]):
    #     peak_values = np.array(peak_values)
    #     DAC_values = np.array(DAC_values)
    #     y_max = peak_values[-1]
    #     #-> if y_max == peak_values[-2], maybe there's saturation
    #     ## fit the two points with a line and calculate y_pred
    #     index = len(peak_values)-1
    #     # if y_max == peak_values[-2]:
    #     if np.abs(y_max - peak_values[-2]) <= 0.001:
    #         y_pred = []
    #         slope, y0 = np.polyfit(DAC_values[-2:], peak_values[-2:], 1)
    #         y_pred = DAC_values * slope + y0
    #         # find the last (last to start) value where y_true[i] - y_pred[i] != 0
    #         for i in range(len(peak_values)-1, -1, -1):
    #             if (np.abs(peak_values[i] - y_pred[i])/(peak_values[-1]-peak_values[0])) > 0.001:
    #                 index = i
    #                 break
    #     return index, DAC_values[index], peak_values[index]
    def checkLinearity(self, DAC_values=[], peak_values=[], lowdac=10, updac=20):
        #========== NEED TO FIND A WAY TO NOT HARD CODE THIS PART ============
        if self.CALI == 'CALI4':
            updac = 10
            lowdac = 0
        #==============================================================
        peak_values = np.array(peak_values)
        DAC_values = np.array(DAC_values)

        # print('DAC_values = {}'.format(DAC_values))
        # print('low dac = {}'.format(lowdac))
        
        index_low_dac = np.where(DAC_values >= lowdac)[0][0]
        old_index = np.where(DAC_values >= updac)[0][0]
        # print('low = {}\t old = {}'.format(index_low_dac, old_index))
        index = old_index

        peak_values_init = peak_values[index_low_dac : old_index+1]
        DAC_values_init = DAC_values[index_low_dac : old_index+1]
        #
        slope, y0 = np.polyfit(DAC_values_init, peak_values_init, 1)
        #
        for i in range(old_index+1, len(DAC_values)):
            y_pred = slope * DAC_values[i] + y0
            condition = (np.abs(y_pred - peak_values[i])/(peak_values[-1]-peak_values[0])) > 0.03
            if condition:
                index = i
                break
            index += 1
            peak_values_init = peak_values[index_low_dac : index+1]
            DAC_values_init = DAC_values[index_low_dac : index+1]
            #
            slope, y0 = np.polyfit(DAC_values_init, peak_values_init, 1)
            # print(slope)
        return index, DAC_values[index], peak_values[index]
        

    def get_gains(self, peak_csvname=''):
        # self.config = config
        peak_csvname = '_'.join(peak_csvname.split('.')[:-1])
        # read the csv file in a dataframe
        self.peakdata_df = pd.read_csv('/'.join([self.output_dirCALI, peak_csvname + '.csv']))
        # self.get_peakValues_forallDAC(path_to_binfolder=path_to_binfolder, config=config, femb_number=femb_number)
        #
        #
        dac_v = {} # mV/bit
        dac_v['4_7mVfC'] = 18.66
        dac_v['7_8mVfC'] = 14.33
        dac_v['14_0mVfC'] = 8.08
        dac_v['25_0mVfC'] = 4.61

        CC = 1.85*pow(10, -13) # capacitance of the Toy-tpc
        e = 1.602*pow(10, -19) # electron charge
        ifirst = 3
        ilast = 5
       
        print(peak_csvname)
        gain_mVfC = '_'.join(peak_csvname.split('_')[ifirst:ilast])
        # print(peak_csvname)
        print('gain mVfC ',gain_mVfC)
        sgs = gain_mVfC
        print(sgs)

        if self.sgp1:
            dac_du = dac_v['4_7mVfC']
        else:
            dac_du = dac_v[sgs]
        print(dac_du)
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
        for ich in self.peakdata_df['CH'].unique():
        # for ich in [0, 1, 2]:
            df_for_ch = self.peakdata_df[self.peakdata_df['CH']==ich].reset_index()
            df_for_ch['DAC'] = df_for_ch['DAC'].astype(int)
            df_for_ch = df_for_ch.sort_values(by='DAC', ascending=True)
            starting_of_nonlinearity = self.checkLinearity(DAC_values=df_for_ch['DAC'], peak_values=df_for_ch['peak_value'], lowdac=10, updac=25)
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
        # try to create a folder named gains
        try:
            os.mkdir('/'.join([self.output_dirCALI, 'gains']))
        except:
            pass
        output_dir = '/'.join([self.output_dirCALI, 'gains'])
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
        plt.ylabel('Gain (electron/ADC bin)', fontsize=20)
        plt.xlim([-1, 128])
        plt.title(gains_figname, fontsize=20)
        plt.savefig('/'.join([output_dir, gains_figname + '.png']))
        plt.close()
        #
        # DAC corresponding to peak_max
        plt.figure(figsize=(12, 7))
        plt.plot(CHs, DAC_for_peakmax, marker='.', markersize=7)
        plt.xlabel('CH');plt.ylabel('DAC_for_peakmax')
        plt.title(gains_figname, fontsize=20)
        plt.savefig('/'.join([output_dir, '_'.join([gains_figname, 'DAC_peakmax', '.png'])]))
        plt.close()
        print('Figures saved....')
        #
        # save the Gains in a csv file
        gain_df = pd.DataFrame({'CH': self.peakdata_df['CH'].unique(), 'Gain': Gains, 'DAC_peakmax': DAC_for_peakmax})
        gain_df.to_csv('/'.join([output_dir, gains_figname + '.csv']), index=False)
        print('Gains saved in a csv file at {}'.format(output_dir))

#***************************************************************
# These functions get the peak values and DAC from the bin files
def Gains_CALI1(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False, fembs_to_ignore={}):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=1, sgp1=False, fembs_to_ignore=fembs_to_ignore)
    mVfC = [4.7, 7.8, 14.0, 25.0]
    for data_dir in asic.input_dirCALI_list:
        for gain_in_mVfC in mVfC:
            config = [200, gain_in_mVfC, 2.0]
            asic.get_peakValues_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)

def Gains_CALI2(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False, fembs_to_ignore={}):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=2, sgp1=False, fembs_to_ignore=fembs_to_ignore)
    config = [900, 14.0, 2.0]
    for data_dir in asic.input_dirCALI_list:
        asic.get_peakValues_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)
        # asic.get_gains_for_allFEMBs(path_to_binfolder=data_dir, config=config, withlogs=withlogs)

def Gains_CALI3_or_CALI4(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False, fembs_to_ignore={}, CALI_number=3):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=True, fembs_to_ignore=fembs_to_ignore)
    config = [200, 14.0, 2.0]
    if CALI_number==4:
        config = [900, 14.0, 2.0]
    for data_dir in asic.input_dirCALI_list:
        asic.get_peakValues_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)
#***************************************************************

def savegains(path_to_dataFolder='', output_dir='', temperature='LN', femb_to_excludes=[7, 24, 27, 55, 75]):
    '''
        This function is to be run after Gains_CALI{} functions.
        It saves the gains in a new folder named 'gains' once the peak values are available.
    '''
    CALI_numbers = [1, 2,3,4]
    for cali in CALI_numbers:
        sgp1 = False
        if cali==3 or cali==4:
            sgp1 = True
        asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=cali, sgp1=sgp1)
        list_csv = [csvname for csvname in os.listdir(asic.output_dirCALI) if ('.csv' in csvname) & ('rms' not in csvname)]
        #
        samtec = []
        for femb in femb_to_excludes:
            strfemb = 'femb{}'.format(femb)
            if femb < 10:
                strfemb = 'femb0{}'.format(femb)
                samtec.append(strfemb)
        csv_to_be_used = []
        for csvname in list_csv:
            femb = csvname.split('_')[1]
            if femb not in samtec:
                csv_to_be_used.append(csvname)
        #
        #print(csv_to_be_used)
        for csv_filename in csv_to_be_used:
            asic.get_gains(peak_csvname=csv_filename)

#*********************************************************************************
#************************get ENC**************************************************
def select_fembs_report_dir(input_dir='', fembs_to_exclude=[], temperature='LN'):
    selected = []
    for DIR in os.listdir(input_dir):
        femb_report = DIR.split('_')[0]
        if (femb_report not in fembs_to_exclude) & (temperature in DIR):
            selected.append('/'.join([input_dir, DIR]))
    return selected

def get_fembID_list(input_dir='', fembs_to_exclude=[], temperature='LN'):
    tmp_listdir = select_fembs_report_dir(input_dir=input_dir, fembs_to_exclude=fembs_to_exclude, temperature=temperature)
    femb_ids = []
    for rmsfilename in tmp_listdir:
        femb = (rmsfilename.split('/')[-1]).split('_')[0]
        femb_ids.append(femb.split('B')[-1])
    return femb_ids

def read_rms_ana(list_path_to_file=[], femb_id='101',
                 gain_larasic='14_0mVfC'):
    input_femb = 'femb{}'.format(femb_id)
    for f in list_path_to_file:
        femb = (f.split('/')[-1]).split('_')[0]
        filename = f.split('/')[-1]
        if (input_femb == femb) & (gain_larasic in filename):
            df = pd.read_csv(f)
            return df

def read_gain_ana(list_path_to_file=[], femb_id='101', gain_larasic='14_0mVfC'):
    input_femb = 'femb{}'.format(femb_id)
    for f in list_path_to_file:
        femb = (f.split('/')[-1]).split('_')[1]
        filename = f.split('/')[-1]
        if (input_femb == femb) & (gain_larasic in filename):
            df = pd.read_csv(f)
            return df

def get_ENC_CALI(datadir='', input_dir='', temperature='LN', CALI_number=1, listgains=[], fembs_to_exclude=[], sgp1=False, fembs_to_ignore={}):    
    # list larasic gains
    # listgains = ['4_7', '7_8', '14_0', '25_0']
    larasic_gains = ['{}mVfC'.format(g) for g in listgains]

    # seelct rms files without samtec fembs
    ana_rms_files = []
    # rms_input_dir = '/'.join([input_dir, temperature, 'CALI1', 'rms'])
    rms_input_dir = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number), 'rms'])
    
    for rms_file in os.listdir(rms_input_dir):
        femb_ana = rms_file.split('_')[0]
        if femb_ana not in fembs_to_exclude:
            ana_rms_files.append('/'.join([rms_input_dir, rms_file]))
    
    # get fembs list
    tmp_fembs_to_exclude = []
    for femb in fembs_to_exclude:
        if femb<10:
            tmp_fembs_to_exclude.append('femb0{}'.format(femb))
        else:
            tmp_fembs_to_exclude.append('femb{}'.format(femb))
    # modification 12/26/2022
    # output_enc = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number), 'ENC'])
    list_fembs = []
    if len(tmp_fembs_to_exclude) != 0:
        all_fembs = []
        for femb_folder in os.listdir(datadir):
            if 'femb' in femb_folder:
                folder_name_split = femb_folder.split('_')[:-2]
                for femb in folder_name_split:
                    all_fembs.append(femb)
        # list_fembs = []
        for femb in all_fembs:
            if femb not in tmp_fembs_to_exclude:
                list_fembs.append(femb.split('femb')[-1])
    else:
        calidir = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number)])
        print(calidir)
        for file in os.listdir(calidir):
            if ('.csv' in file) & ('rms' in file):
                part_filenames = file.split('_')
                for part in part_filenames:
                    if 'femb' in part:
                        part_in_v = False
                        for k, v in fembs_to_ignore.items():
                            if part.split('femb')[-1] in v:
                                part_in_v = True
                        if not part_in_v:
                            list_fembs.append(part.split('femb')[-1])
    output_enc = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number), 'ENC'])
    try:
        os.mkdir(output_enc)
    except:
        print('ENC folder already exists...')
    # select gains csv files
    # path_to_gains = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number), 'gains'])
    path_to_gains = '/'.join([input_dir, temperature, 'CALI{}'.format(CALI_number), 'gains'])
    selected_gains_csv = []
    for csvfile in os.listdir(path_to_gains):
        if '.csv' in csvfile:
            femb = csvfile.split('_')[1]
            if (femb not in tmp_fembs_to_exclude) & (femb.split('femb')[-1] in list_fembs):
                selected_gains_csv.append('/'.join([path_to_gains, csvfile]))
    # get enc for each femb and larasic gains
    for femb in list_fembs:
        for larasicgain in larasic_gains:
            # try:
                ana_rms = read_rms_ana(list_path_to_file=ana_rms_files, femb_id=femb, gain_larasic=larasicgain)[['channelNumber', 'RMS']]
                # print(ana_rms.head())
                ana_gain = read_gain_ana(list_path_to_file=selected_gains_csv, femb_id=femb, gain_larasic=larasicgain)[['CH', 'Gain']]
                ana_rms['CH'] = ana_rms['channelNumber'].astype(int)
                ana_rms.drop('channelNumber', axis=1, inplace=True)
                df_enc = pd.merge(ana_gain, ana_rms, on='CH', how='left')
                df_enc['ENC'] = df_enc.apply(lambda x: x.Gain * x.RMS, axis=1)
                #
                BL = ((ana_rms_files[0].split('/')[-1]).split('BL_')[0]).split('_')[-1]
                figname = '_'.join(['femb{}'.format(femb), '{}BL'.format(BL), larasicgain, '2_0us'])
                if (CALI_number==3) | (CALI_number==4):
                    figname += '_sgp1'
                # plot ENC vs CH number
                # save the plot in png file
                plt.figure(figsize=(12, 7))
                plt.plot(df_enc['CH'], df_enc['ENC'], marker='.', markersize=7.5)
                plt.xlabel('CH')
                plt.ylabel('ENC(electron)')
                plt.title(figname)
                plt.savefig('/'.join([output_enc, figname + '.png']))
                plt.close()
                # save the plot of RMS for all channel number in jpg file
                plt.figure(figsize=(12, 7))
                plt.plot(df_enc['CH'], df_enc['RMS'], marker='.', markersize=7.5)
                plt.xlabel('CH')
                plt.ylabel('RMS')
                plt.title(figname)
                plt.savefig('/'.join([output_enc, 'RMS_' + figname + '.png']))
                plt.close()
                # save dataframe with enc to csv file
                df_enc.to_csv('/'.join([output_enc, figname + '.csv']), index=False)
                print('CALI{}/ENC/{} saved'.format(CALI_number, figname + '.csv'))
            # except:
            #     print('error : fem = {}, gain = {}'.format(femb, larasicgain))

def distribution_ENC_Gain(csv_source_dir='', CALI_number=1, temperature='LN', larasic_gain='4_7mVfC', fit=False):
    '''
    In this function, the csv files stored in the folder ENC will be used to get
    the ENC and the Gain.
        What does this function do ?
    Basically, concatenating the csv files in the folder CALI{} along the axis=0 (row after row) for each configuration.
    Then get the columns Gain and ENC and plot an histogram of each of them. These histograms are the distributions
    of Gain and ENC.
    '''
    input_dir = '/'.join([csv_source_dir, temperature, 'CALI{}'.format(CALI_number), 'ENC'])
    output_dir = '/'.join([input_dir, 'distribution'])
    try:
        os.mkdir(output_dir)
    except:
        print('A folder named distribution already exists!!')
    #
    # listgains = ['4_7', '7_8', '14_0', '25_0']
    # larasic_gains = ['{}mVfC'.format(g) for g in listgains]
    #
    #@ get list of csv files in input_dir
    list_existing_csv_files = [f for f in os.listdir(input_dir) if '.csv' in f]
    #
    #@ select only the csv files corresponding to the larasic_gain
    list_selected_csv_files = []
    for f in list_existing_csv_files:
        f_split = f.split('BL_')[-1]
        if larasic_gain in f_split:
            list_selected_csv_files.append(f)
    #
    try:
        #@ concatenate all of the selected csv files -> one_df
        one_df = pd.DataFrame()
        for f in list_selected_csv_files:
            femb = f.split('_')[0]
            path_to_file = '/'.join([input_dir, f])
            df = pd.read_csv(path_to_file)
            df['femb'] = [femb for _ in range(len(df))]
            one_df = pd.concat([one_df, df], axis=0)
        #
        #@ save one_df in output_dir
        one_df.to_csv('/'.join([output_dir, 'all_gain_rms_enc_CALI{}.csv'.format(CALI_number)]), index=False)
        #
        BL = list_selected_csv_files[0].split('_')[1]
        st = ('_'.join(list_selected_csv_files[0].split('_')[4:])).split('.')[0]
        figname = '{}_{}_{}'.format(BL, larasic_gain, st)
        #
        gain_selected = one_df['Gain']
        enc_selected = one_df['ENC']
        #
        #@ fit with gaussian
        # gain_x, gain_pdf, enc_x, enc_pdf = pd.Series([]), pd.Series([]), pd.Series([]), pd.Series([])
        gain_mean, gain_std, enc_mean, enc_std = 0., 0., 0., 0.
        if fit:
            gain_selected, gain_mean, gain_std, gain_loc, gain_scale, gain_x, gain_pdf = get_gaussPdf(dataVec=gain_selected, nstd=3, skewed=True)
            enc_selected, enc_mean, enc_std, enc_loc, enc_scale, enc_x, enc_pdf = get_gaussPdf(dataVec=enc_selected, nstd=3, skewed=True)
            #@ set plot style: seaborn-white
            plt.style.use('seaborn-white')
            #@ plot the distribution of the Gain
            plt.figure(figsize=(10,10))
            plt.hist(np.array(gain_selected), bins=50, density=True, label='gain, mean = {:.4f}, std = {:.4f}'.format(gain_mean, gain_std))
            plt.plot(gain_x, gain_pdf, color='red', label='gaussian fit')
            plt.xlabel('Gain', fontsize=15)
            plt.ylabel('#')
            plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
            plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
            plt.title('Gain for {}'.format(figname))
            plt.legend()
            plt.savefig('/'.join([output_dir, 'gain_distribution_CALI{}_fitted.png'.format(CALI_number)]))
            plt.close()
            #
            #@ plot the distribution of the ENC
            plt.figure(figsize=(10,10))
            plt.hist(enc_selected, bins=50, density=True, label='ENC, mean = {:.4f}, std = {:.4f}'.format(enc_mean, enc_std))
            plt.plot(enc_x, enc_pdf, color='red', label='gaussian fit')
            plt.xlabel('ENC', fontsize=15);plt.ylabel('#')
            plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
            plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
            plt.title('ENC for {}'.format(figname))
            plt.legend()
            plt.savefig('/'.join([output_dir, 'enc_distribution_CALI{}_fitted.png'.format(CALI_number)]))
            plt.close()
        else:
            plt.figure(figsize=(10, 10))
            plt.hist(gain_selected, bins=50)
            plt.xlabel('Gain', fontsize=15)
            plt.ylabel('#')
            plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
            plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
            plt.title('Gain for {}'.format(figname))
            plt.savefig('/'.join([output_dir, 'gain_distribution_CALI{}.png'.format(CALI_number)]))
            plt.close()
            #
            plt.figure(figsize=(10,10))
            plt.hist(enc_selected, bins=50, log=True)
            plt.xlabel('ENC', fontsize=15);plt.ylabel('#')
            plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
            plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
            plt.title('ENC for {}'.format(figname))
            plt.savefig('/'.join([output_dir, 'enc_distribution_CALI{}.png'.format(CALI_number)]))
            plt.close()        
        #
        #@
        print('Distributions of the gain and enc saved...')
    except:
        print('error')
        pass

#****************************************************************
#----------------------------------------------------------------
# this function is for one CALI_number only and was used for test
def save_peakValues_to_csv(path_to_dataFolder='', output_dir='', temperature='LN', withLogs=False, CALI_number=1):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=False)
    listcsvname = [f for f in os.listdir(asic.output_dirCALI) if ('.csv' in f) & ('rms' not in f)]
    config = [200, 14.0, 2.0]
    # for data_dir in asic.input_dirCALI_list:
    for csvname in listcsvname:
        # asic.get_peakValues_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withLogs)
        figname = csvname.split('.')[0]
        data_df = pd.read_csv('/'.join([asic.output_dirCALI, csvname]))
        asic.plot_peakValue_vs_DAC_allch(data_df, ch_list=range(128), figname=figname)

##
## Function from Xilinx
def separateCSV_foreachFEMB(path_to_csv='', output_path='', datanames=['CALI1']):
    '''
        Having csv files of 4 fembs, this function separate one csv file to 4 csv files for each femb
    '''
    for dataname in datanames:
        path_to_file = '/'.join([path_to_csv, dataname])
        output_path_file = '/'.join([output_path, dataname, 'rms'])
        # try to create the output folder
        try:
            os.mkdir(output_path_file)
        except:
            pass
        #
        for csvname in os.listdir(path_to_file):
            if (('rms' in csvname) or ('RMS' in csvname)) & ('.csv' in csvname):
                part_csvname = csvname.split('.')[0]
                #
                # dataframe
                df = pd.read_csv('/'.join([path_to_file, csvname]), dtype={'femb_ids': str})
                femb_ids = df['femb_ids'].unique()
                for femb in femb_ids:
                    df_femb = df[df['femb_ids']==femb].reset_index().drop('index', axis=1)
                    femb_csvname = '_'.join(['femb{}'.format(femb), part_csvname + '.csv'])
                    df_femb.to_csv('/'.join([output_path_file, femb_csvname]), index=False)
                    # print(femb_csvname)

#---------------------------------CODES FROM JUPYTER NOTEBOOK----------------------------------------
#---------- GainFEMBs vs Gain of LArASIC ------------------------------------------------------------
def GainFEMBs_vs_GainLArASIC(input_dir, fembs_to_exclude=[]):
    '''
        input_dir should be the main folder of the analysis. e.g: '../results/IO-1865-1D/QC_analysis/'
    '''
    # gains
    temperatures = ['LN', 'RT']
    cali_numbers = ['CALI1', 'CALI2', 'CALI3', 'CALI4']

    for CALI in cali_numbers:
        plt.figure(figsize=(15, 5))
        plt.style.use('seaborn-white')
        plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
        plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
        output_dir = '/'.join([input_dir, 'gains_vs_femb'])
        try:
            os.mkdir(output_dir)
        except:
            pass

        for T in temperatures:
            configs = []
            for f in os.listdir('/'.join([input_dir, T, CALI, 'gains'])):
                if ('.csv' in f) & ('gains' in f):
                    config1 = f.split('_')[2]
                    config2 = (f.split('mVBL_')[-1]).split('.')[0]
                    configs.append('_'.join([config1, config2]))
            configs = pd.Series(configs)
            #----------------------
            mean_per_configs = []
            std_per_configs = []
            unique_configs = []
            for c in configs.unique():
                tmp_c = c.split('_')
                p1 = tmp_c[1]
                p2 = tmp_c[2].split('m')[0]
                unique_configs.append(float('.'.join([p1, p2])))
                
            #----------------------
            for config in configs.unique():
                femb_ids = []
    #             mean_gains = []
                gains = []
                sgp1 = False
                print(config)
                for f in os.listdir('/'.join([input_dir, T, CALI, 'gains'])):
                    if ('.csv' in f) & ('gains' in f) & (config in f):
                        femb_id = f.split('_')[1]
                        # if femb_id != 'femb111': # failed board --> belongs to previous test : 1C
                        #     if 'sgp1' in f:
                        #         sgp1 = True
                        #     if femb_id == 'femb75':
                        #         continue
                        tmp_fembs_to_exclude = ['femb'+femb for femb in fembs_to_exclude]
                        if femb_id not in tmp_fembs_to_exclude:
                            # if 'sgp1' in f:
                            #     sgp1 = True
                            femb_id = str(femb_id.split('b')[-1])
                            femb_ids.append(femb_id)
                            df = pd.read_csv('/'.join([input_dir, T, CALI, 'gains', f]))
                            gains += list(df['Gain'])
                print(femb_ids)
                mean_per_configs.append(np.mean(gains))
                std_per_configs.append(np.std(gains))
            df_mean = pd.DataFrame({'gain_larasic': unique_configs, 'mean_gain': mean_per_configs, 'std': std_per_configs})
            df_mean = df_mean.sort_values(by='gain_larasic', ascending=True)

            plt.errorbar(x=df_mean['gain_larasic'], y=df_mean['mean_gain'], yerr=df_mean['std'], marker='.',
                        capsize=10, markersize=5, label=T)
            plt.xticks(df_mean['gain_larasic'], fontsize=15)
            plt.yticks(fontsize=15)
        plt.xlabel('Gain of the LArASIC ($mV/fC$)', fontsize=15)
        plt.ylabel('Gain($e^-/ADC bin$)', fontsize=15)
        plt.legend(fontsize=15)
        plt.title('baseline = 200mV, shaping time = 2.0$\mu s$', fontsize=15)
        plt.savefig('/'.join([output_dir, 'gain_vs_gainLArASIC_{}.png'.format(CALI)]))
        plt.close()
#-----------------------------ENC vs FEMB_IDs-------------------------------------------------------------
def ENC_vs_FEMB_ids(input_dir, fembs_to_exclude=[], fontsize_xticks=10):
    '''
        input_dir should be the main folder of the analysis. e.g: '../results/IO-1865-1D/QC_analysis/'
    '''
    # enc
    temperatures = ['LN', 'RT']
    cali_numbers = ['CALI1', 'CALI2', 'CALI3', 'CALI4']
    for T in temperatures:
        for CALI in cali_numbers:
            output_dir = '/'.join([input_dir, T, CALI, 'enc_vs_femb'])
            try:
                os.mkdir(output_dir)
            except:
                pass

            configs = []
            for f in os.listdir('/'.join([input_dir, T, CALI, 'ENC'])):
                if ('.csv' in f):
                    config1 = f.split('_')[1]
                    config2 = (f.split('mVBL_')[-1]).split('.')[0]
                    configs.append('_'.join([config1, config2]))
            configs = pd.Series(configs)
            #
            plt.figure(figsize=(15, 5))
            plt.style.use('seaborn-white')
            plt.tick_params(axis='x', direction='out', length=5, width=2, color='black', top=False)
            plt.tick_params(axis='y', direction='out', length=5, width=2, color='black', right=False)
            colors = ['red', 'green', 'blue', 'orange']
            #
            gain_df = pd.DataFrame()
            for i, config in enumerate(configs.unique()):
                femb_ids = []
                mean_encs = []
                std_encs = []
                sgp1 = False
                for f in os.listdir('/'.join([input_dir, T, CALI, 'ENC'])):
                    if ('.csv' in f) & (config in f):
                        femb_id = f.split('_')[0]
                        if 'sgp1' in f:
                            sgp1 = True
                        tmp_fembs_to_exclude = ['femb'+femb for femb in fembs_to_exclude]
                        # if femb_id == 'femb75':
                        if femb_id in tmp_fembs_to_exclude:
                            continue
                        femb_ids.append(femb_id)
                        df = pd.read_csv('/'.join([input_dir, T, CALI, 'ENC', f]))
                        mean_enc = np.mean(df['ENC'])
                        mean_encs.append(mean_enc)
                        std_encs.append(np.std(df['ENC']))
                #
                tmp_df = pd.DataFrame({'femb': femb_ids, 'enc_{}'.format(config): mean_encs, 'std_{}'.format(config): std_encs})
                if i==0:
                    gain_df = pd.concat([gain_df, tmp_df], axis=1)
                else:
                    gain_df = gain_df.merge(tmp_df, how='left', on='femb')

            cols = gain_df.columns
            BL = cols[1].split('_')[1]

            i = 0
            for ii in range(1, len(cols), 2):
                config = '_'.join(cols[ii].split('_')[2:])
                coly = cols[ii]
                colerr = cols[ii+1]
                gain_df.sort_values(by='femb', ascending=True, inplace=True)
                plt.errorbar(x=gain_df['femb'], y=gain_df[coly], yerr=gain_df[colerr], color=colors[i],
                            capsize=5, label='{}'.format(config))
                i += 1
            plt.xlabel('FEMB')
            plt.ylabel('mean_ENC ($e^-$)')
            plt.xticks(fontsize=fontsize_xticks)

            plt.title('mean ENC vs FEMB for {} at {}'.format(BL, T))
            plt.legend()
            figname = '_'.join([CALI, 'ENC_vs_femb'])
            if sgp1:
                figname += '_sgp1'
            plt.savefig('/'.join([output_dir, figname + '.png']))
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
