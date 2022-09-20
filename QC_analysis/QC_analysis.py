# outputdir : D:/IO-1865-1C/QC/analysis
# datadir : D:/IO-1865-1C/QC/data/..../PWR_Meas

import os
import pickle
import matplotlib.pyplot as plt

class QC_analysis:
    def __init__(self, datadir='', output_dir=''):
        self.output_analysis_dir = output_dir
        particularDataFolderName = ''
        # choose which data to use
        dataType = 'power_measurement'
        if dataType=='power_measurement':
            self.indexData = 1
            particularDataFolderName = 'PWR_Meas'
        self.input_data_dir = ['/'.join([datadir, onefolder, particularDataFolderName]) for onefolder in os.listdir(datadir)]
        self.bin_filenames = os.listdir(self.input_data_dir[0]) ## the *.bin filenames are the same for all the folders

    def read_bin(self, filename, input_data_dir):
        with open(os.path.join(input_data_dir, filename), 'rb') as fp:
            return pickle.load(fp)[self.indexData]

    def get_oneData(self, sourceDataDir='', powerTestType_with_BL='SE_200mVBL', dataname='bias'):
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
        elif dataname=='ADC':
            name = 'PWR_ADC'
            indexData = 3
        
        V_meas = [((current_data[femb])[indexData])[1] for femb in femb_numbers]
        I_meas = [((current_data[femb])[indexData])[2] for femb in femb_numbers]
        P_meas = [((current_data[femb])[indexData])[3] for femb in femb_numbers]
    
        # title of the plot
        title = '_'.join([name, powerTestType_with_BL])
        # name of the figure
        #print(sourceDataDir)
        #figname = '/'.join([self.output_analysis_dir, '_'.join([title, sourceDataDir.split('/')[-2], sourceDataDir.split('/')[-1] + '.png'])])
        dirname = sourceDataDir.split('/')[-2]
        return (title, dirname, femb_numbers, V_meas, I_meas, P_meas)

    def _plot(self, dataname='bias', inputdir_name=''):
        pwr_test_types = ['SE_200mVBL', 'SE_SDF_200mVBL', 'DIFF_200mVBL']
        # create figure
        plt.figure(figsize=(12, 7))
        title = ''
        dirname = ''
        for pwr in pwr_test_types:
            title, dirname, femb_numbers, V_meas, I_meas, P_meas = self.get_oneData(sourceDataDir=inputdir_name,
                    powerTestType_with_BL=pwr, dataname=dataname)
            plt.plot(femb_numbers, V_meas, label=title)
        plt.title(title.split('_')[0])
        plt.legend()
        plt.savefig('/'.join([self.output_analysis_dir, dirname + '.png']))


    def test(self, dataname='bias'):
        #data = self.read_bin(filename='PWR_DIFF_200mVBL_14_0mVfC_2_0us_0x20.bin', input_data_dir=self.input_data_dir[0])
        #out = self.get_oneData(sourceDataDir=self.input_data_dir[0], powerTestType_with_BL='SE_200mVBL', dataname='Bias5V')
        for inputdir in self.input_data_dir:
            self._plot(dataname=dataname, inputdir_name=inputdir)


if __name__ == '__main__':
    qc = QC_analysis(datadir='D:/IO-1865-1C/QC/data/', output_dir='D:/IO-1865-1C/QC/analysis')
    qc.test(dataname='bias')
