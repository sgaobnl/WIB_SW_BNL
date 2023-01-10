'''
    Author: Rado Razakamiandra
    email: radofana@gmail.com
    last update: 12/27/2022
'''
import os
from fpdf import FPDF
import pandas as pd
import numpy as np

class PDF(FPDF):
    def __init__(self, title, temperatures=[], sourceDir=''):
        FPDF.__init__(self, 'P', 'mm', 'A4')
        # set margins
        self.set_top_margin(0.05)
        self.set_left_margin(0.5)
        self.set_right_margin(0.5)
        
        self.y_pos = 0
        self.title = title
        self.temperatures = temperatures
        self.sourceDir = sourceDir # parent folder
        self.sourceDirs = ['/'.join([sourceDir, T]) for T in self.temperatures]

    def header(self):
        self.y_pos += 1
        self.set_y(self.y_pos)
        self.set_text_color(r=0, g=200, b=100)
        self.set_font('Arial', 'B', 10)
        self.cell(2.5)
        self.cell(205, 10, self.title, 1, 1, 'C')
        # self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'B', 10)
        self.cell(80)
        # self.cell(30, 5, 'BNL CE Team', 0, 0, 'c')
        self.cell(30, 5, '', 0, 0, 'c')

    def RMS_Pedestal(self):
        '''
            This method adds the plots of the mean of RMS(Pedestal) in function of the shaping
            time to the pdf output file at RT and LN2.
        '''
        print('## Adding RMS and Pedestal.....')
        datanames = ['RMS', 'Pedestal']
        RMSdir = ['/'.join([DIR, 'RMS/correctedCSV_rms_pedestal/plots']) for DIR in self.sourceDirs]
        sourceDirs = ['/'.join([rmsdir, dataname]) for rmsdir in RMSdir for dataname in datanames]
        BLs = ['200mV', '900mV']
        for dataname in datanames:
            # add page
            self.add_page()
            y_pos = self.y_pos + 15
            self.set_y(y_pos)
            self.set_font('Times', 'IB', 10)
            self.cell(210, 10, '{}'.format(dataname), 0, 1, 'C')
            dataDirs = [dir for dir in sourceDirs if 'plots/'+dataname in dir]
            y_pos += 5
            for datadir in dataDirs:
                T = datadir.split('/')[-5]
                self.set_y(y_pos)
                self.set_font('Times', 'I', 10)
                self.cell(210, 10, T, 0, 1, 'C')
                y_pos += 7
                ## In case we need the data source of the plots,
                ## we can uncomment this part
                # csvname = 'gaussian_{}.csv'.format(dataname)
                # csv_df = pd.read_csv('/'.join([datadir, csvname]))
                x_pos = 0
                for BL in BLs:
                    # self.set_x(x_pos)
                    # self.set_y(y_pos)
                    figname = 'shapingTime_vs_{}Mean_{}.png'.format(dataname, BL)
                    path_to_png = '/'.join([datadir, figname])
                    self.set_y(y_pos)
                    self.image(path_to_png, x_pos, y_pos, 100, 75)
                    x_pos += 100
                y_pos += 75

    def PWR_Consumption(self):
        print('## Adding Power consumption.....')
        try:
            # path_to_csv_list = ['/'.join([self.sourceDirs[0], f]) for f in os.listdir(self.sourceDirs[0]) if ('.csv' in f) & ('power_consumption' in f)]
            path_to_csv_list = []
            for sourceDir in self.sourceDirs:
                for f in os.listdir(sourceDir):
                    if ('.csv' in f) & ('power_consumption' in f):
                        path_to_csv_list.append('/'.join([sourceDir, f]))
            paths_to_csv = []
            if len(path_to_csv_list) != 0:
                for path in path_to_csv_list:
                    paths_to_csv.append(path)
            
            # add page
            self.add_page()
            x_pos = 10
            # std_RT, mean_RT, std_LN, mean_LN = 0.0, 0.0, 0.0, 0.0
            for i, path_to_csv in enumerate(paths_to_csv):
                path_to_png = path_to_csv.split('.csv')[0] + '.png'
                print(path_to_png)
                pwr_csv_file = pd.read_csv(path_to_csv)
                cols = [col for col in pwr_csv_file.columns if 'PWR_Cons' in col]
                
                y_pos = self.y_pos + 20
                self.set_y(y_pos)
                self.set_font('Times', 'IB', 12)
                # self.cell(40)
                self.cell(210, 0, 'Power Consumption Measurement', 0, 1, 'C')

                y_pos += 10
                self.set_font('Times', 'I', 8)
                self.cell(x_pos + 20)
                self.cell(100, 10, self.temperatures[i], 'C')
                self.image(path_to_png, x_pos, y_pos, 100, 75)

                self.set_font('Arial', '', 8)
                y_pos += 80
                for col in cols:
                    std = np.std(pwr_csv_file[col])
                    mean = np.mean(pwr_csv_file[col])
                    dataname = col.split('PWR_Cons_')[-1]
                    self.text(x_pos + 10, y_pos, 'mean {} = {:.3f}'.format(dataname, mean))
                    self.text(x_pos + 50, y_pos, 'std {} = {:.3f}'.format(dataname, std))
                    y_pos += 5
                self.ln(-y_pos - 50 - 3)
                x_pos += 100
                
        except OSError as error:
            print(error)

    def PWR_Measurement(self):
        print('## Adding Power measurements.....')
        datanames = ['ColdADC', 'ColDATA', 'LArASIC', 'Bias5V']
        Quantities_measured = [q_meas + '_meas' for q_meas in ['I', 'V', 'P']]
        
        for dataname in datanames:
            # add page
            self.add_page()
            y_pos = self.y_pos + 15
            self.set_y(y_pos)
            self.set_font('Times', 'IB', 10)
            self.cell(210, 10, 'Power Measurement : {}'.format(dataname), 0, 1, 'C')
            y_pos += 5
            print('{} : '.format(dataname))
            all_meas = {}
            for itemperature, sourceDir in enumerate(self.sourceDirs):
                # write temperature in a page
                self.set_y(y_pos)
                self.set_font('Times', 'I', 10)
                self.cell(210, 10, '{}'.format(self.temperatures[itemperature]), 0, 1, 'C', False)
                y_pos += 10
                measurements = {}
                x_pos = 0
                for i_meas, q_meas in enumerate(Quantities_measured):
                    sourceDir_csv = '/'.join([sourceDir, 'PWR_Meas'])
                    path_to_csv = '/'.join([sourceDir_csv, dataname + '.csv'])
                    data_df = pd.read_csv(path_to_csv)
                    cols = [col for col in data_df.columns if q_meas in col]
                    
                    tmp_meas = {}
                    for col in cols:
                        std = np.std(data_df[col])
                        mean = np.mean(data_df[col])
                        tmp_meas[col] = [std, mean]
                    measurements[q_meas] = tmp_meas

                    path_to_png = '/'.join([sourceDir_csv, 'plots', '_'.join([q_meas, dataname + '_.png'])])
                    self.image(path_to_png, x_pos, y_pos, w=70, h=50)
                    x_pos += 71
                all_meas[self.temperatures[itemperature]] = measurements
                y_pos += 50
            ## The codes above only add the images in the pdf file.
            ## The next position in y you can use is y_pos. It will reset for the next iteration on datanames
            #### since we will write each dataname in a new page.
            ## to be able to draw conclusions about the standard deviation and the mean
            #### please use the dictionary all_meas
        #
        # since we get the power consumption after doing the power measurement,
        # let's run the script to add the power consumption in the pdf file here
        self.PWR_Consumption()

    def Gain(self):
        print('## Adding Gain.....')
        sourceGain = '/'.join([self.sourceDir, 'gainsfemb_vs_gainlarasic'])
        self.add_page()
        y_pos = self.y_pos + 15
        self.set_y(y_pos)
        self.set_font('Times', 'IB', 10)
        self.cell(210, 10, 'Gain of FEMBs vs Gain of LArASIC', 0, 1, 'C')
        y_pos += 5
        # for imgfile in os.listdir(sourceGain):
        x_pos = 0
        icali = 1
        for i in range(2):
            y_pos += 10
            for j in range(2):
                CALI = 'CALI{}'.format(icali)
                imgfile = 'gain_vs_gainLArASIC_{}.png'.format(CALI)
                self.set_font('Times', 'I', 7)
                # y_pos += 10
                self.set_y(y_pos)
                self.set_x(x_pos)
                self.cell(100, 10, '{}'.format(imgfile.split('.')[0]), 0, 1, 'C')
                y_pos += 10
                # self.set_y(y_pos)
                path_to_img = '/'.join([sourceGain, imgfile])
                self.image(path_to_img, x_pos, y_pos, 100, 50)
                icali += 1
                x_pos += 100
                y_pos -= 10
            x_pos = 0
            y_pos += 50
        
if __name__ == '__main__':
    sourceDir = '../results/IO-1865-1D/QC_analysis'
    pdf = PDF(title='Universal Performance Analysis FEMB QC', temperatures=['LN', 'RT'], sourceDir=sourceDir)
    # pdf.RMS_Pedestal()
    # pdf.PWR_Measurement()
    pdf.Gain()
    # pdf.PWR_Consumption()
    pdf.output('{}/tuto.pdf'.format(sourceDir), 'F')