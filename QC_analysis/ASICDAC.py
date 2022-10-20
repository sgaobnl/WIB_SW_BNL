#-----------------------------------------------------------------------
# Author: Rado
# email: radofana@gmail.com
# last update: 10/19/2022
#----------------------------------------------------------------------

from asyncio import transports
from utils import *

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
        self.peakdata_df = pd.DataFrame()
        self.rmsdata_df = pd.DataFrame()
    
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
        all_rms_list = [] # save the rms in this variable
        for femb_number in [0, 1, 2, 3]:
            print('nfemb  = {}'.format(femb_number))
            peak_values = []
            rms_list = [] # rms for one femb
            ch_count = 0
            for ich in tqdm(range(128)):
                iich = femb_number*128+ich
                first_peak = False
                
                #allpls = np.empty(0)
                allpls = []

                # only get the first event
                for iev in range(nevent):
                    pos_peaks, _ = find_peaks(pldata[iev][iich], height=np.amax(pldata[iev][iich]))
                    if not first_peak:
                        for ppeak in pos_peaks:
                            startpos = ppeak - 50
                            # go to the next pulse if the starting position is negative
                            if startpos<0:
                                startpos_neg = True
                                continue
                            endpos = startpos + 100
                            selected_peak = np.max(pldata[iev][iich][startpos:endpos])
                            peak_values.append(selected_peak)
                            #allpls = np.append(allpls, pldata[iev][iich][startpos:endpos]) # to get the rms
                            #rms_list.append(np.std(pldata[iev][iich][startpos:endpos])) #
                            ch_count += 1
                            first_peak = True
                            break
                        allpls = np.append(allpls, pldata[iev][iich]) # to get the rms
                    else:
                        break
                # get rms
                #allpls = np.empty(0)
                #for iev in range(nevent):
                #    evtdata = pldata[iev][iich]
                #    allpls = np.append(allpls, evtdata)
                ch_rms = np.std(allpls)
                rms_list.append(ch_rms)
            # append DAC and peak_values for one femb
            all_peak_values.append((DAC, peak_values))
            # append rms for one femb
            all_rms_list.append((DAC, rms_list))
            if len(peak_values) != len(rms_list):
                print('ch_count = {}'.format(ch_count))
                print('len(rms_list) = {}\tlen(peak_values) = {}\t dac = {}'.format(len(rms_list), len(peak_values), DAC))
        # I expect to get the DAC value and an array of length 128 where each element is a value of one peak for each channel
        # return the (DAC, rms) for 4 fembs and the (DAC, peak_values) for 4 fembs
        return (all_rms_list, all_peak_values)

    def get_peakValues_withRMS_forallDAC(self, path_to_binfolder='', config=[200,  14.0, 2.0], withlogs=False):
        # all_peakdata_dict = {}
        self.config = config
        list_binfiles = self.list_bin(input_dir=path_to_binfolder, BL=self.config[0], gain=self.config[1], shapingTime=self.config[2])
        #
        data_list = []
        for ibin in range(len(list_binfiles)):
            # tmpDAC, tmpPeak_values = self.decode_onebin(path_to_binFolder=path_to_binfolder, bin_filename=list_binfiles[ibin], femb_number=femb_number)
            data_list.append(self.decode_onebin(path_to_binFolder=path_to_binfolder, bin_filename=list_binfiles[ibin]))
        
        FEMBs = [0, 1, 2, 3]
        for femb_number in FEMBs:
            all_peakdata_dict = {}
            all_rmsdata_dict = {}
            for ibin in range(len(list_binfiles)):
                # all_rmsdata_list.append(data_list[ibin][0][femb_number])

                DAC = data_list[ibin][1][femb_number][0]
                peak_values = data_list[ibin][1][femb_number][1]
                all_peakdata_dict[DAC] = peak_values
                #
                rms_values = data_list[ibin][0][femb_number][1]
                all_rmsdata_dict[DAC] = rms_values
            #
            # peak and DAC
            DACs, peaks, CHs = [], [], []
            RMSs = []
            for dac, peak_array in all_peakdata_dict.items():
                tmp_dac = [dac for _ in range(len(peak_array))]
                tmp_peaks_values = peak_array
                tmp_rms = all_rmsdata_dict[dac] # get rms using dac
                ch_numbers = [i for i in range(len(peak_array))]
                # try to catch the error in the length of RMS
                if len(tmp_rms) != len(tmp_peaks_values):
                    print('dac = {}'.format(dac))

                DACs += tmp_dac
                peaks += tmp_peaks_values
                RMSs += tmp_rms # append rms to RMSs
                CHs += ch_numbers

            
            # try to catch the error
            if len(DACs) != len(RMSs):
                print('config = {}\t len(DACs) = {}\t len(RMS) = {}'.format(config, len(DACs), len(RMSs)))
            
            #transformed_rmsdata_df = pd.DataFrame({
            #    'CH': CHs,
            #    'RMS': RMSs,
            #    'DAC': DACs
            #})
            transformed_peakdata_df = pd.DataFrame({
                'CH': CHs,
                'peak_value': peaks,
                'DAC': DACs,
                'RMS': RMSs
            })
            self.peakdata_df = pd.DataFrame()
            self.peakdata_df = transformed_peakdata_df
            #self.rmsdata_df = transformed_rmsdata_df

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
            rms_csvname = 'rms_femb{}_{}mVBL_{}mVfC_{}us'.format(femb_id, self.config[0], config1, config2) # csv file for rms
            if self.sgp1:
                peak_csvname += '_sgp1'
            # save peakdata with DAC in csv
            self.peakdata_df.to_csv('/'.join([self.output_dir, peak_csvname + '.csv']), index=False)
            # save rmsdata in csv
            #self.rmsdata_df.to_csv('/'.join([self.output_dir, rms_csvname + '.csv']), index=False)
        
    #================ use data_df from this part------no need to read the data bin files except logs_env.bin===========
    def plot_peakValue_vs_DAC_allch(self, data_df, ch_list=range(128)):
        '''
        Run get_peakValues_withRMS_forallDAC before using this method
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
        return index, DAC_values[index], peak_values[index]
        

    def get_gains(self, peak_csvname=''):
        # self.config = config
        peak_csvname = '_'.join(peak_csvname.split('.')[:-1])
        # read the csv file in a dataframe
        self.peakdata_df = pd.read_csv('/'.join([self.output_dir, peak_csvname + '.csv']))
        # self.get_peakValues_withRMS_forallDAC(path_to_binfolder=path_to_binfolder, config=config, femb_number=femb_number)
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
       
        gain_mVfC = '_'.join(peak_csvname.split('_')[ifirst:ilast])
        # print(peak_csvname)
        # print(gain_mVfC)
        sgs = gain_mVfC

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
        for ich in self.peakdata_df['CH'].unique():
        # for ich in [0, 1, 2]:
            df_for_ch = self.peakdata_df[self.peakdata_df['CH']==ich].reset_index()
            df_for_ch['DAC'] = df_for_ch['DAC'].astype(int)
            df_for_ch = df_for_ch.sort_values(by='DAC', ascending=True)
            starting_of_nonlinearity = self.checkLinearity(DAC_values=df_for_ch['DAC'], peak_values=df_for_ch['peak_value'])
            slope, y0 = np.polyfit(df_for_ch['DAC'][:starting_of_nonlinearity[0]], df_for_ch['peak_value'][:starting_of_nonlinearity[0]], 1)

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
            os.mkdir('/'.join([self.output_dir, 'gains']))
        except:
            pass
        output_dir = '/'.join([self.output_dir, 'gains'])
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
        plt.ylabel('Gain', fontsize=20)
        plt.xlim([-1, 128])
        plt.savefig('/'.join([output_dir, gains_figname + '.png']))
        #
        # DAC corresponding to peak_max
        plt.figure(figsize=(12, 7))
        plt.plot(CHs, DAC_for_peakmax, marker='.', markersize=7)
        plt.xlabel('CH');plt.ylabel('DAC_for_peakmax')
        plt.savefig('/'.join([output_dir, '_'.join([gains_figname, 'DAC_peakmax', '.png'])]))
        print('Figures saved....')
        #
        # save the Gains in a csv file
        gain_df = pd.DataFrame({'CH': self.peakdata_df['CH'].unique(), 'Gain': Gains, 'DAC_peakmax': DAC_for_peakmax})
        gain_df.to_csv('/'.join([output_dir, gains_figname + '.csv']), index=False)
        print('Gains saved in a csv file at {}'.format(output_dir))

# look at the github repo and change it to the original one in order to save data in the future
def Gains_CALI1(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=1, sgp1=False)
    mVfC = [4.7, 7.8, 14.0, 25.0]
    for data_dir in asic.input_dir_list:
        for gain_in_mVfC in mVfC:
            config = [200, gain_in_mVfC, 2.0]
            asic.get_peakValues_withRMS_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)

def Gains_CALI2(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=2, sgp1=False)
    config = [900, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        asic.get_peakValues_withRMS_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)
        # asic.get_gains_for_allFEMBs(path_to_binfolder=data_dir, config=config, withlogs=withlogs)

def Gains_CALI3_or_CALI4(path_to_dataFolder='', output_dir='', temperature='LN', withlogs=False, CALI_number=3):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=True)
    config = [200, 14.0, 2.0]
    if CALI_number==4:
        config = [900, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        asic.get_peakValues_withRMS_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withlogs)
            
def savegains(path_to_dataFolder='', output_dir='', temperature='LN'):
    CALI_numbers = [1,2,3,4]
    for cali in CALI_numbers:
        sgp1 = False
        if cali==3 or cali==4:
            sgp1 = True
        asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=cali, sgp1=sgp1)
        list_csv = [csvname for csvname in os.listdir(asic.output_dir) if '.csv' in csvname]
        for csv_filename in list_csv:
            asic.get_gains(peak_csvname=csv_filename)

# this function is for one CALI_number only and was used for test
def save_peakValues_to_csv(path_to_dataFolder='', output_dir='', temperature='LN', withLogs=False, CALI_number=3):
    asic = ASICDAC(input_data_dir=path_to_dataFolder, output_dir=output_dir, temperature=temperature, CALI_number=CALI_number, sgp1=True)
    config = [200, 14.0, 2.0]
    for data_dir in asic.input_dir_list:
        # asic.get_peakValues_withRMS_forallDAC(path_to_binfolder=data_dir, config=config, withlogs=withLogs)
        data_df = pd.read_csv('/'.join([asic.output_dir, 'peakValues_femb75_900mVBL_14_0mVfC_2_0us_sgp1.csv']))
        asic.plot_peakValue_vs_DAC_allch(data_df, ch_list=range(128))
