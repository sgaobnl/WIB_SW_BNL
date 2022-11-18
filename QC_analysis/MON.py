'''
    Author: Rado
    email: radofana@gmail.com, rrazakami@bnl.gov
    last update: 11/09/2022
'''
from utils import *

class MON_LARASIC:
    '''
        Monitoring LArASIC
        Parameters:
            temperature: self.temperature,
            data_dir: self.data_dir,
            output_dir: self.output_dir
    '''
    def __init__(self, input_dir='', output_dir='', temperature='LN', fembs_to_exclude=[]):
        self.temperature = temperature
        self.data_dir = input_dir
        self.output_dir = output_dir
        self.femb_dir_list = self.list_femb_dirs(fembs_to_exclude=fembs_to_exclude)
    
    def exclude_fembs(self, fembs_to_exclude=[24], fembs_folder_name=''):
        list_femb_str = [str(femb) for femb in fembs_to_exclude]
        femb_name_split = fembs_folder_name.split('_')[:4]
        for femb in femb_name_split:
            femb_id = femb[4:]
            if femb_id in list_femb_str:
                return True
        return False

    def list_femb_dirs(self, fembs_to_exclude=[]):
        femb_dir_list = []
        for femb_folder in os.listdir(self.data_dir):
            if (self.temperature in femb_folder) & (not self.exclude_fembs(fembs_to_exclude=fembs_to_exclude, fembs_folder_name=femb_folder)):
                if 'MON_FE' in os.listdir('/'.join([self.data_dir, femb_folder])):
                    femb_dir_list.append('/'.join([self.data_dir, femb_folder, 'MON_FE']))
        return femb_dir_list

    def read_bin(self, bin_dir='', bin_filename='LArASIC_mon.bin'):
        '''
            Read the bin file.
            This function will also be used in MON_ADC
        '''
        path_to_bin = '/'.join([bin_dir, bin_filename])
        with open(path_to_bin, 'rb') as bin_pointer:
            return pickle.load(bin_pointer)
    
    def get_data_index(self, dataname='bandgap'):
        index = -1
        if dataname=='bandgap':
            index = 0
        elif dataname=='temperature':
            index = 1
        elif dataname=='BL200':
            index = 2
        elif dataname=='BL900':
            index = 3
        elif dataname=='logs':
            index = 4
        return index

    def get_MONdata(self, data_from_bin=[], dataname='bandgap'):
        index_MONdata = self.get_data_index(dataname=dataname)
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

    def run_MON_LArASIC(self):
        datanames = ['bandgap', 'temperature', 'BL200', 'BL900']
        for idir in range(len(self.femb_dir_list)):
            data = self.read_bin(self.femb_dir_list[idir], bin_filename='LArASIC_mon.bin')
            #
            femb_foldername = self.femb_dir_list[idir].split('/')[-2]
            # new_output_dir = '/'.join([self.output_dir, femb_foldername])
            # print(new_output_dir)
            # try:
            #     os.mkdir(new_output_dir)
            # except:
            #     print('Folder already exists')
            fembs = data[self.get_data_index(dataname='logs')]['femb id']
            for dataname in datanames:
                MON_data = self.get_MONdata(data_from_bin=data, dataname=dataname)
                ylabel = dataname
                xlabel = 'chip#'
                if 'BL' in dataname:
                    ylabel = dataname[2:] + 'mVBL'
                    xlabel = 'ch'
                for ifemb, femb_id in fembs.items():
                    iifemb = int(ifemb[-1])
                    toytpc = (self.femb_dir_list[idir].split('/')[-2]).split('_')[-1]
                    femb_folderName = '_'.join(['FEMB', fembs[ifemb], self.temperature, toytpc])
                    new_output_dir = '/'.join([self.output_dir, femb_folderName])
                    try:
                        os.mkdir(new_output_dir)
                    except:
                        print('Folder already exists.....')
                    self.plotMon(femb_data_x=MON_data[iifemb][0], femb_data_y=MON_data[iifemb][1],
                                femb_id=fembs[ifemb], dataname=dataname,
                                xlabel=xlabel, ylabel=ylabel, output_dir=new_output_dir)
                    self.saveMon_to_csv(femb_data_x=MON_data[iifemb][0], femb_data_y=MON_data[iifemb][1],
                                        femb_id=fembs[ifemb], dataname=dataname,
                                        output_dir=new_output_dir)


class MON_ADC:
    def __init__(self, input_dir=''):
        pass