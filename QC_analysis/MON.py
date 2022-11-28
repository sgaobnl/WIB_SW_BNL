'''
    Author: Rado
    email: radofana@gmail.com, rrazakami@bnl.gov
    last update: 11/28/2022
'''
from utils import *
import re

class MON_LARASIC:
    '''
        Monitoring LArASIC
        Parameters:
            temperature: self.temperature,
            data_dir: self.data_dir,
            output_dir: self.output_dir,
            fembs_to_exclude: a list of the femb_id to exclude
    '''
    def __init__(self, input_dir='', output_dir='', temperature='LN', fembs_to_exclude=[]):
        print('..........init............')
        self.temperature = temperature
        self.data_dir = input_dir
        self.output_dir = '/'.join([output_dir, 'MON_FE'])
        try:
            os.mkdir(self.output_dir)
        except:
            pass
        self.femb_dir_list = self.list_femb_dirs(fembs_to_exclude=fembs_to_exclude)
    
    def exclude_fembs(self, fembs_to_exclude=[24], fembs_folder_name=''):
        '''
            This function returns True if at least one of the ids in fembs_to_exclude is in the fembs_folder_name.
        '''
        list_femb_str = [str(femb) for femb in fembs_to_exclude]
        femb_name_split = fembs_folder_name.split('_')[:4]
        for femb in femb_name_split:
            femb_id = femb[4:]
            if femb_id in list_femb_str:
                return True
        return False

    def list_femb_dirs(self, fembs_to_exclude=[]):
        '''
            Knowing the femb_ids we want to exclude, this function lists the selected femb directories.
        '''
        femb_dir_list = []
        for femb_folder in os.listdir(self.data_dir):
            if (self.temperature in femb_folder) & (not self.exclude_fembs(fembs_to_exclude=fembs_to_exclude, fembs_folder_name=femb_folder)):
                if 'MON_FE' in os.listdir('/'.join([self.data_dir, femb_folder])):
                    femb_dir_list.append('/'.join([self.data_dir, femb_folder, 'MON_FE']))
        return femb_dir_list

    def read_bin(self, bin_dir='', bin_filename='LArASIC_mon.bin'):
        '''
            Read the bin file.
            This function will also be used in MON_ADC.
        '''
        path_to_bin = '/'.join([bin_dir, bin_filename])
        with open(path_to_bin, 'rb') as bin_pointer:
            return pickle.load(bin_pointer)
    
    def get_data_index(self, dataname='bandgap'):
        '''
            This function returns the index of dataname in the data_list.
        '''
        index = -1
        if (dataname=='bandgap') | (dataname=='dac_sgp1'):
            index = 0
        elif (dataname=='temperature') | (dataname=='dac_14mVfC'):
            index = 1
        elif (dataname=='BL200') | (dataname=='dac_logs'):
            index = 2
        elif dataname=='BL900':
            index = 3
        elif dataname=='logs':
            index = 4
        return index

    def get_MONdata(self, data_from_bin=[], dataname='bandgap'):
        '''
            input:
                data_from_bin: a list returned after reading the bin data,
                dataname: the name of the data we want to get from data_from_bin
            output:
                a list of the data for 4 fembs after calculating the average of the data saved.
                For 200mVBL and 900mVBL, xx represents the channel numbers.
        '''
        index_MONdata = self.get_data_index(dataname=dataname)
        index_logs = -1
        if 'dac' in dataname:
            index_logs = self.get_data_index(dataname='dac_logs')
        else:
            index_logs = self.get_data_index(dataname='logs')
        fadc = 1/(2**14) * 2048 # mV
        mon_refs = data_from_bin[index_MONdata]
        fembs = data_from_bin[index_logs]['femb id']
        data_allFEMBs = []
        for ifemb, femb_id in fembs.items():
            mon_list = []
            xlabels = []
            nfemb = int(ifemb[-1])
            for key, value in mon_refs.items():
                sps = len(value)
                total = list(map(sum, zip(*value)))
                avg = np.array(total) / sps * fadc
                mon_list.append(avg[nfemb])
                xlabels.append(key)
            xx = []
            if (dataname=='BL200') | (dataname=='BL900'):
                xx = list(range(len(xlabels)))
            else:
                xx = xlabels
            data_allFEMBs.append((xx, mon_list))
        return data_allFEMBs
        
    def plotMon(self, femb_data_x, femb_data_y, femb_id, dataname='bandgap', xlabel='', ylabel='', output_dir=''):
        '''
        Save monitoring data to png file.
        '''
        plt.figure(figsize=(10, 6))
        if 'BL' in dataname:
            plt.scatter(femb_data_x, femb_data_y, s=7, color='blue')    
        else:
            plt.plot(femb_data_x, femb_data_y, marker='.', markersize=7)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('/'.join([output_dir, '_'.join(['mon', dataname, 'femb' + femb_id + '.png'])]))
        plt.close()
    
    def saveMon_to_csv(self, femb_data_x, femb_data_y, femb_id, dataname='bandgap', output_dir=''):
        '''
            Save monitoring data to csv file.
        '''
        col1 = 'chip#'
        if 'BL' in dataname:
            col1 = 'ch'
        df = pd.DataFrame({col1: femb_data_x, dataname: femb_data_y})
        csvname = '_'.join(['mon', dataname, 'femb' + femb_id])
        df.to_csv('/'.join([output_dir, csvname + '.csv']), index=False)

    def get_dist(self, dataname, data=[], output_dir=''):
        mean = np.mean(data)
        std = np.std(data)
        figname = '_'.join(['hist', dataname, self.temperature])
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=50, label='mean = {:.4f}, std = {:.4f}'.format(mean, std))
        plt.xlabel(dataname + '(mV)', fontsize=12)
        plt.ylabel('#')
        plt.legend()
        plt.savefig('/'.join([output_dir, figname + '.png']))
        #
        # save to csv
        df = pd.DataFrame({dataname: data})
        df.to_csv('/'.join([output_dir, figname + '.csv']), index=False)

    def run_MON_LArASIC(self):
        '''
            This function runs the script for monitoring the LArASIC.
            Name of the bin file: LArASIC_mon.bin,
            List of the datanames: ['bandgap', 'temperature', 'BL200', 'BL900'],
            How it works?
                - Select the dataname
                - select the name of the main folder: femb_dir_name
                - get the monitoring data from the selected folder and dataname
                - for each femb_id:
                    * plot a scatter/line plot using matplotlib.pyplot
                    * save the monitoring data to csv file
                - get the distribution of the data for all fembs.
        '''
        datanames = ['bandgap', 'temperature', 'BL200', 'BL900']
        for dataname in datanames:
            histdata_x = []
            histdata_y = []
            for idir in range(len(self.femb_dir_list)):
                data = self.read_bin(self.femb_dir_list[idir], bin_filename='LArASIC_mon.bin')
                fembs = data[self.get_data_index(dataname='logs')]['femb id']

                MON_data = self.get_MONdata(data_from_bin=data, dataname=dataname)
                ylabel = dataname + '(mV)'
                xlabel = 'chip#'
                if 'BL' in dataname:
                    ylabel = dataname[2:] + 'mVBL (mV)'
                    xlabel = 'ch'
                print(fembs)
                for ifemb, femb_id in fembs.items():
                    iifemb = int(ifemb[-1])
                    toytpc = (self.femb_dir_list[idir].split('/')[-2]).split('_')[-1]
                    femb_folderName = '_'.join(['FEMB', femb_id, self.temperature, toytpc])
                    new_output_dir = '/'.join([self.output_dir, femb_folderName])
                    try:
                        os.mkdir(new_output_dir)
                    except:
                        pass
                        # print('Folder already exists.....')
                    self.plotMon(femb_data_x=MON_data[iifemb][0], femb_data_y=MON_data[iifemb][1],
                                femb_id=femb_id, dataname=dataname,
                                xlabel=xlabel, ylabel=ylabel, output_dir=new_output_dir)
                    self.saveMon_to_csv(femb_data_x=MON_data[iifemb][0], femb_data_y=MON_data[iifemb][1],
                                        femb_id=femb_id, dataname=dataname,
                                        output_dir=new_output_dir)
                    histdata_x += MON_data[iifemb][0]
                    histdata_y += MON_data[iifemb][1]
            self.get_dist(dataname=dataname, data=histdata_y, output_dir=self.output_dir)
        print('-------LArASIC_mon DONE------------')


    def checkLinearity(self, x=[], y=[], lowdac=0, updac=30):
        '''
            Check the linearity of the plot for each chip.
            The slope for LArASIC_DAC is negative.
            input:
                x: list of DAC values,
                y: list of values corresponding to the DACs,
                lowdac and updac: min and max values of DAC between which we want to check the linearity.
            output:
                index: index of the maximum DAC we found a linear fit,
                x[index]: value of this maximum DAC,
                y[index]: y_value corresponding to max DAC.
        '''
        x = np.array(x)
        y = np.array(y)
        index_low_dac = np.where(x >= lowdac)[0][0]
        old_index = np.where(x >= updac)[0][0]
        # print('low = {}\t old = {}'.format(index_low_dac, old_index))
        index = old_index

        y_init = y[index_low_dac : old_index+1]
        x_init = x[index_low_dac : old_index+1]
        #
        slope, y0 = np.polyfit(x_init, y_init, 1)
        #
        for i in range(old_index+1, len(x)):
            y_pred = slope * x[i] + y0
            # err = np.std(y[index_low_dac:old_index+1]) / len(y[index_low_dac:old_index+1])
            condition = (np.abs(y_pred - y[i])/(y[0]-y[-1])) > 0.01
            if condition:
                index = i
                break
            index += 1
            y_init = y[index_low_dac : index+1]
            x_init = x[index_low_dac : index+1]
            #
            slope, y0 = np.polyfit(x_init, y_init, 1)
        return index, x[index], y[index]

    def run_MON_LArASIC_DAC(self):
        '''
            This function runs the script for monitoring LArASIC_DAC.
            How it works ?
                - select the data name from ['dac_sgp1', 'dac_14mVfC'],
                - select the femb dir folder,
                - get the monitoring data from LArASIC_mon_DAC.bin,
                - for each femb
                    * plot the monitoring value in function of the DAC for each chip --> png,
                    * save the monitoring values of the DAC for all chips in a dataframe femb_df --> csv,
                    * check linearity for each chip and save the max DAC and chip number in a dataframe --> csv.
        '''
        datanames = ['dac_sgp1', 'dac_14mVfC']
        for dataname in datanames:
            for idir in range(len(self.femb_dir_list)):
                data = self.read_bin(self.femb_dir_list[idir], bin_filename='LArASIC_mon_DAC.bin')
                fembs = data[self.get_data_index(dataname='dac_logs')]['femb id']
                MON_data = self.get_MONdata(data_from_bin=data, dataname=dataname)
                for ifemb, femb_id in fembs.items():
                    iifemb = int(ifemb[-1])
                    x = MON_data[iifemb][0]
                    y = MON_data[iifemb][1]
                    xx = [re.findall(r'[0-9]+', s) for s in x] # find numbers in x
                    # get the data for all chips
                    femb_df = pd.DataFrame() # <-- save the data here
                    index_lin = []
                    plt.figure(figsize=(10, 7))
                    for ichip in range(8):
                        chip = []
                        chip_dac = []
                        chip_y = []
                        for ixx in range(len(xx)):
                            if xx[ixx][1] == str(ichip):
                                chip_dac.append(int(xx[ixx][0]))
                                chip_y.append(y[ixx])
                                chip.append(ichip)
                        # if ichip==4:
                        plt.plot(chip_dac, chip_y, label='chip{}'.format(ichip)) #, marker='.', markersize='5.7')
                        chip_df = pd.DataFrame({'dac': chip_dac, 'chip{}'.format(ichip): chip_y})
                        if ichip==0:
                            femb_df = pd.concat([femb_df, chip_df], axis=0)
                        else:
                            femb_df = femb_df.merge(chip_df, on='dac', how='inner')

                    tmpchipNumber = []
                    maxLinearDAC = []
                    for ichip in range(8):
                        lin = self.checkLinearity(x=femb_df['dac'], y=femb_df['chip{}'.format(ichip)], lowdac=0, updac=30)
                        slope, y0 = np.polyfit(femb_df['dac'][:lin[0]+1], femb_df['chip{}'.format(ichip)][:lin[0]+1], 1)
                        tmpchipNumber.append(ichip)
                        maxLinearDAC.append(lin[1])
                        # x = np.array(femb_df['dac'][:lin[0]+1])
                        # y = slope * x + y0
                        # plt.plot(x, y, label='fit', color='red')
                        print(lin)
                        print(slope)
                    chipNumber = ['chip{}'.format(ichip) for ichip in tmpchipNumber]
                    maxLinearDAC_df = pd.DataFrame({'chip': chipNumber, 'maxDAC': maxLinearDAC})
                    
                    # save df in csv file
                    toytpc = (self.femb_dir_list[idir].split('/')[-2]).split('_')[-1]
                    femb_folderName = '_'.join(['FEMB', femb_id, self.temperature, toytpc])
                    new_output_dir = '/'.join([self.output_dir, femb_folderName])
                    try:
                        os.mkdir(new_output_dir)
                    except:
                        pass
                    figname = '_'.join(['LArASIC', dataname])
                    femb_df.to_csv('/'.join([new_output_dir, figname + '.csv']), index=False)
                    maxLinearDAC_name = '_'.join([figname, 'maxDAC'])
                    maxLinearDAC_df.to_csv('/'.join([new_output_dir, maxLinearDAC_name + '.csv']), index=False)
                    plt.xlabel('DAC')
                    plt.title(figname)
                    plt.legend()
                    plt.savefig('/'.join([new_output_dir, figname + '.png']))
                    plt.close()
        

class MON_ADC:
    def __init__(self, input_dir=''):
        pass
