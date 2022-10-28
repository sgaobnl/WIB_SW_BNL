#========================================================================
#       Author: Rado
#       email: radofana@gmail.com
#       last update: 10/28/2022
#========================================================================

from utils import *

class CompareGains:
    def __init__(self, femb1='', dirfemb1='', dirfemb2='', savedir='', temperature='LN'):
        '''
        This class is used to compare the gains of the FEMBs in the report and those I calculated
            femb1: femb_id from the reports,
            femb2: femb_id from ASICDAC analysis,
            self.dirfemb1: actual path to the gain in the reports,
            self.dirfemb2: list of actual paths to the gains from ASICDAC class
                which include CALI1, CALI2, CALI3, CALI4
        '''
        #
        self.femb1 = 'report'
        self.femb2 = 'rado'
        #
        self.config = ''
        self.femb_id = femb1
        # dirfemb1
        femb1_dir = ''
        if 'FEMB{}_{}_150pF_R001'.format(femb1, temperature) in os.listdir(dirfemb1):
            femb1_dir = 'FEMB{}_{}_150pF_R001'.format(femb1, temperature)
        else:
            femb1_dir = 'FEMB{}_{}_150pF'.format(femb1, temperature)
        self.dirfemb1 = '/'.join([dirfemb1, femb1_dir, 'CALI'])
        self.dirfemb2 = ['/'.join([dirfemb2, temperature, 'CALI{}'.format(i), 'gains']) for i in range(1, 5)]
        #
        self.savedir = '/'.join([savedir, temperature, 'ratio'])
        try:
            os.mkdir(self.savedir)
        except:
            pass

    def get_gainfiles_femb1(self, config=[200, 14.0, 2.0], sgp1=False):
        list_str_config = [str(c) for c in config]
        BL = list_str_config[0] + 'mVBL'
        G = '_'.join(list_str_config[1].split('.')) + 'mVfC'
        st = '_'.join(list_str_config[2].split('.')) + 'us'
        str_config = '_'.join([BL, G, st])
        Gain_bin_files = '_'.join(['Gain', str_config]) + '.bin'
        if sgp1:
            Gain_bin_files = '_'.join(['Gain', str_config, 'sgp1']) + '.bin'
        path_to_file = '/'.join([self.dirfemb1, Gain_bin_files])
        return path_to_file

    def get_gainfiles_femb2(self, config=[200, 14.0, 2.0], sgp1=False):
        list_str_config = [str(c) for c in config]
        BL = list_str_config[0] + 'mVBL'
        G = '_'.join(list_str_config[1].split('.')) + 'mVfC'
        st = '_'.join(list_str_config[2].split('.')) + 'us'
        str_config = '_'.join([BL, G, st])

        #
        self.config = str_config
        #

        CALI_folders = self.dirfemb2[:2]
        if sgp1:
            CALI_folders = self.dirfemb2[2:]
        
        csvname = '_'.join(['gains', 'femb{}'.format(self.femb_id), str_config]) + '.csv'
        if sgp1:
            csvname = csvname.split('.')[0] + '_sgp1.csv'
        
        # find in which folder this file is located
        dir_to_be_used = ''
        for d in CALI_folders:
            files_in_dir = os.listdir(d)
            if csvname in files_in_dir:
                dir_to_be_used = d
                break
        # path to csvname
        path_to_gaincsv = '/'.join([dir_to_be_used, csvname])
        return path_to_gaincsv
    
    def read_gainfiles(self, config=[200, 14.0, 2.0], sgp1=False):
        # bin file
        gainfile_femb1 = self.get_gainfiles_femb1(config=config, sgp1=sgp1)
        with open(gainfile_femb1, 'rb') as f1:
            gaindata_femb1 = pickle.load(f1)[0]
        gaindict_femb1 = {'CH': [i for i in range(128)], 'Gain_femb_{}'.format(self.femb1): gaindata_femb1}
        gaindf_femb1 = pd.DataFrame(gaindict_femb1)

        # csv file
        gainfile_femb2 = self.get_gainfiles_femb2(config=config, sgp1=sgp1)
        gaindata_femb2 = pd.read_csv(gainfile_femb2)
        gaindata_femb2.columns = ['CH', 'Gain_femb_{}'.format(self.femb2), 'DAC_peakmax']
        
        # merge the dataframes
        df = gaindf_femb1.merge(gaindata_femb2, how='left', on='CH').drop('DAC_peakmax', axis=1)
        
        return df
    
    def get_ratio(self, config=[200, 14.0, 2.0], sgp1=False):
        gains_data = self.read_gainfiles(config=config, sgp1=sgp1)
        # print(gains_data[gains_data['Gain_femb_report'] < 0])
        columns = gains_data.columns
        gains_data['ratio({}/{})'.format(columns[1], columns[2])] = np.array(gains_data[columns[1]]) / np.array(gains_data[columns[2]])
        # print(gains_data[gains_data['ratio({}/{})'.format(columns[1], columns[2])] < 0])
        cols = gains_data.columns

        ratio_filename = '_'.join(['ratio', 'gains', 'femb{}'.format(self.femb_id), self.config])
        if sgp1:
            ratio_filename += '_sgp1'
        # save ratio to csv
        gains_data.to_csv('/'.join([self.savedir, ratio_filename + '.csv']))

        # plot ratio
        plt.figure(figsize=(12, 7))
        plt.plot(gains_data['CH'], gains_data[cols[-1]])
        plt.xlabel('CH')
        plt.ylabel('ratio')
        plt.title(cols[-1])
        plt.savefig('/'.join([self.savedir, ratio_filename + '.png']))

    def get_allratio(self, sgp1=False):
        if not sgp1:
            all_configs = []
            BLs = [200, 900]
            Gains = [4.7, 7.8, 14.0, 25.0]
            Stime = [2.0]
            for BL in BLs:
                for Gain in Gains:
                    for st in Stime:
                        all_configs.append([BL, Gain, st])
            for config in all_configs:
                try:
                    self.get_ratio(config=config, sgp1=sgp1)
                except:
                    pass
        else:
            all_configs = [[200, 14.0, 2.0], [900, 14.0, 2.0]]
            for config in all_configs:
                try:
                    self.get_ratio(config=config, sgp1=sgp1)
                except:
                    pass

if __name__ == '__main__':
    fembs = [i for i in range(101, 116)]
    for femb in fembs:
        c = CompareGains(femb1=femb, dirfemb1='../results/reports', dirfemb2='../results',
                        savedir='../results', temperature='LN')
        c.get_allratio(sgp1=False)
        c.get_allratio(sgp1=True)