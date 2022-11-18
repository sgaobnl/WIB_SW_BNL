#**********************************************************
#   Author: Rado
#   email: radofana@gmail.com
#   last modification: October 24, 2022
#**********************************************************
#from binascii import hexlify
#from codecs import readbuffer_encode
#from operator import index
import csv
import os
#from turtle import ondrag
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy.stats import norm
from scipy.optimize import curve_fit
import scipy.stats as stats
# progress bar
import time
from tqdm import tqdm
# for ASICDAC_CALI data analysis
import pickle

# function for one file
def get_pathToFile(sourceMainDir='', dataType='pedestal', indexFile=0):
    path_to_file = '/'.join([sourceMainDir, dataType, os.listdir(os.path.join(sourceMainDir, dataType))[indexFile]])
    return path_to_file

def read_csv(path_to_file: str):
    # path_to_file = get_pathToFile(sourceMainDir=sourceMainDir, dataType=dataType, indexFile=indexFile)
    data_df = pd.read_csv(path_to_file)
    return data_df

def get_temperature_pF(data_df: pd.DataFrame):
    '''
    This function should return:
        *   'LN' for liquid Nitrogen or 'RT' for Room Temperature.
        *   the input capacitance of a board that plugged into the FEMBs : '0pF' or '150pF'
        in an tuple (temperature, pF)
    '''
    # temperature
    temperature = 'RT'
    folderName = data_df['folderName']
    folderName_temp = pd.Series([k.split('_')[1] for k in folderName])
    if (folderName_temp == 'LN').sum() == len(folderName_temp):
        temperature = 'LN'
    # pF
    pF = '0pF'
    folderName_pF = pd.Series([k.split('_')[-1] for k in folderName])
    if (folderName_pF == '150pF').sum() == len(folderName_pF):
        pF = '150pF'
    return (temperature, pF)

def get_titleFromFileName(path_to_file='', temperature='LN', pF='0pF'):
    tmp_title = path_to_file.split('/')[-1].split('.')[0]
    tmp_title = tmp_title.split('_')[2:]
    tmp_title.append(temperature)
    tmp_title.append(pF)
    title = '_'.join(tmp_title)
    return title

def hist(plt, dataVec: pd.Series, xlabel='', ylabel='', title='', legend='', nbins=100, inLog=False, inDensity=False):
    d = plt.hist(dataVec, color='b', log=inLog, bins=nbins, density=inDensity, label=legend)
    plt.xlabel(xlabel, fontsize='13')
    plt.ylabel(ylabel, fontsize='13')
    plt.title(title)

def get_gaussPdf(dataVec: pd.Series, nstd=3, skewed=False):
    '''
    This function returns (dataSelected, mean, std, x, pdf) where mean and std are mean and std of the data selected;
    x is a list of number between the range xmin to xmax;
    pdf is the probability density function
    '''
    # select data in the range (mean - std * nstd) and (mean + std * nstd)
    old_mean = np.mean(dataVec)
    old_mean = np.mean(dataVec)
    old_std = np.std(dataVec)
    old_xmin = old_mean - nstd * old_std
    old_xmax = old_mean + nstd * old_std
    dataSelected = dataVec[(dataVec >= old_xmin) & (dataVec <= old_xmax)]
    # print('old_mean = {}\t old_std = {}'.format(old_mean, old_std))
    # ae, loc, scale = stats.skewnorm.fit(dataVec)
    # old_xmin = loc - nstd*scale
    # old_xmax = loc + nstd*scale
    # dataSelected = dataVec[(dataVec >= old_xmin) & (dataVec <= old_xmax)]
    # get new mean and new std from the selected data
    new_mean = np.mean(dataSelected)
    new_std = np.std(dataSelected)
    # mean and std are properties of the fitting distribution
    mean, std, xmin, xmax = 0.0, 0.0, 0.0, 0.0
    ae = 0.0
    x = []
    pdf = []
    if not skewed:
        # fit the dataSelected with gaussian distribution
        mean, std = norm.fit(dataSelected)
        xmin = mean - nstd * std
        xmax = mean + nstd * std
        x = np.linspace(xmin, xmax, 100)
        pdf = norm.pdf(x, mean, std)
    else:
        # fit the dataSelected with a skewed gaussian distribution
        # ae, loc, scale = stats.skewnorm.fit(dataSelected)
        # xmin = mean - nstd * std
        # xmax = mean + nstd * std
        xmin = 0
        xmax = 0
        for _ in range(2): # maybe change the value 4
            new_mean = np.mean(dataSelected)
            new_std = np.std(dataSelected)
            xmin = new_mean - nstd * new_std
            xmax = new_mean + nstd * new_std
            dataSelected = dataSelected[(dataSelected >= xmin) & (dataSelected <= xmax)]
        ae, loc, scale = stats.skewnorm.fit(dataSelected)   
        # print('mean = {}\tstd = {}'.format(mean, std))
        # xmin = loc - ae
        # xmax = loc + ae

        # print(ae)
        x = np.linspace(xmin, xmax, 1000)
        pdf = stats.skewnorm.pdf(x, ae, loc, scale)
        ## now can return loc and scale of the distribution
        return (dataSelected, new_mean, new_std, loc, scale, x, pdf)
    return (dataSelected, new_mean, new_std, x, pdf)

def fit_withGaussian(sourceMainDir='', dataType='pedestal', outputDir='', indexFile=0, nstd=3, nbins=100, skewed=False):
    '''
    This function fits the data with a gaussian distribution
    '''
    path_to_file = get_pathToFile(sourceMainDir=sourceMainDir, dataType=dataType, indexFile=indexFile)
    data_df = read_csv(path_to_file=path_to_file)
    temperature, pF = get_temperature_pF(data_df=data_df)
    histTitle = get_titleFromFileName(path_to_file=path_to_file, temperature=temperature, pF=pF) #
    # separate BL, Gain, Shaping Time, temperature, inputCapacitance
    tmp_histTitle = histTitle.split('_')
    BL = tmp_histTitle[0]
    Gain = '_'.join([tmp_histTitle[1], tmp_histTitle[2]])
    ShapingTime = '_'.join([tmp_histTitle[3], tmp_histTitle[4]])
    ## temperature and inputCapacitance=pF are already found
    # Gaussian parameters
    out_dist = get_gaussPdf(data_df[dataType], nstd=nstd, skewed=skewed)
    # get dataSelected and informations of the fitting distribution
    dataSelected, mean, std, x, pdf = out_dist[0], out_dist[1], out_dist[2], out_dist[-2], out_dist[-1]
    # if the distribution is skewed, need the loc and scale parameters
    loc = -2022
    scale = -2022
    if skewed:
        loc = out_dist[3]
        scale = out_dist[4]
    #
    # plot the distribution with the fitting curve
    plt.figure(figsize=(12,7))
    plt.rcParams.update({'figure.max_open_warning': 0}) # get rid of the warning
    plt.plot(x, pdf, color='r', label='Gaussian fit')
    hist(plt=plt, dataVec=dataSelected, xlabel=dataType, ylabel='#',
        title=histTitle, legend='data_selected: mean_data = {:.4f}; std_data = {:.4f}'.format(mean, std), nbins=nbins, inDensity=True, inLog=False)
    plt.legend()
    plt.savefig(os.path.join(outputDir, histTitle + '_.png'))
    if (loc >= 0) & (scale >= 0):
        return (BL,Gain, ShapingTime, temperature, pF, mean, std, loc, scale)
    return (BL,Gain, ShapingTime, temperature, pF, mean, std)

def save_gaussianInfo(sourceMainDir: str, dataType: str, outputDir: str, nstd=3, nbins=100, Nfiles=32, skewed=False):
    '''
    This function saves the configuration along with the mean and std in a csv file
    '''
    BL, Gain, ShapingTime, temperature, inputCapacitance, mean, std = [], [], [], [], [], [], []
    loc, scale = [], []
    for i in tqdm(range(Nfiles)):
        out_fit = fit_withGaussian(sourceMainDir=sourceMainDir, dataType=dataType,
                                                            outputDir=outputDir, indexFile=i, nstd=nstd,
                                                            nbins=nbins, skewed=skewed)
        if len(out_fit) == 9:
            loc.append(out_fit[-2])
            scale.append(out_fit[-1])
        # (tbl, tgain, tst, ttemp, ticap, tmean, tstd) = fit_withGaussian(sourceMainDir=sourceMainDir, dataType=dataType,
        #                                                     outputDir=outputDir, indexFile=i, nstd=nstd,
        #                                                     nbins=nbins, skewed=skewed)
        BL.append(out_fit[0])
        Gain.append(out_fit[1])
        ShapingTime.append(out_fit[2])
        temperature.append(out_fit[3])
        inputCapacitance.append(out_fit[4])
        mean.append(out_fit[5])
        std.append(out_fit[6])
        time.sleep(0.001)
    filename = '_'.join(['gaussian', dataType + '.csv'])
    # save info in a dataframe
    gaussFit_df = pd.DataFrame()
    if (len(loc) != 0) & (len(scale) != 0):
        gaussFit_df = pd.DataFrame({
            'BL': BL,
            'Gain': Gain,
            'ShapingTime': ShapingTime,
            'Temperature': temperature,
            'inputCapacitance': inputCapacitance,
            'mean': mean,
            'std': std,
            'loc': loc,
            'scale': scale
        })
    else:
        gaussFit_df = pd.DataFrame({
            'BL': BL,
            'Gain': Gain,
            'ShapingTime': ShapingTime,
            'Temperature': temperature,
            'inputCapacitance': inputCapacitance,
            'mean': mean,
            'std': std
        })
    t = '-'*20
    print('{} Saving the fitting information {}\n'.format(t, t))
    try:
        gaussFit_df.to_csv(os.path.join(outputDir, filename), index=False)
        print('{} Information saved {}\n'.format(t, t))
    except:
        print('{} Error occured {}'.format(t, t))

# plot mean vs shaping time
def convert_Gain_to_float(df):
    df['Gain'] = df['Gain'].apply(lambda x: x.split('_')[0] + '.' + x.split('_')[1].split('m')[0])
    df['Gain'] = df['Gain'].apply(lambda x: float(x))
    return df

def convert_Timing_to_float(df):
    df['ShapingTime'] = df['ShapingTime'].apply(lambda x: float(x.split('_')[0] + '.' + x.split('_')[1].split('u')[0]))
    # df['ShapingTime'] = df['ShapingTime'].apply(lambda x: float(x))
    return df

def plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv',
                            BL='200mV', outputDir='', ylabel='pedestal', addToTitle='', skewed=False,
                            ylim=[], colors=['red', 'green', 'blue', 'orange']):
    dataFrame = pd.read_csv(path_to_csv)
    dataFrame['BL'] = dataFrame['BL'].apply(lambda x: x[:-2])
    # condition to get the corresponding BL
    condition = (dataFrame['BL']==BL)
    dataFrame = convert_Gain_to_float(dataFrame)
    ##
    ## add the colors to the dataframe
    colors_map = {4.7: colors[0], 7.8: colors[1], 14.0: colors[2], 25.0: colors[3]}
    dataFrame['color'] = dataFrame['Gain'].map(colors_map)
    Gain = dataFrame[condition]['Gain'].unique()
    Colors = dataFrame[condition]['color'].unique()
    #-> dataFrame for BL==200mV
    df = dataFrame[condition]
    # -> shaping time to float
    df = convert_Timing_to_float(df)
    df = df.sort_values(by='ShapingTime', ascending=True)
    # plot baseline vs shapingTime
    plt.figure(figsize=(12,12))
    for i, gain in tqdm(enumerate(Gain)):
        plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'], y=df[df['Gain']==gain]['mean'],
                     yerr=df[df['Gain']==gain]['std'],
                     label= '_'.join([BL, str(gain) + 'mV/fC']), ecolor=Colors[i], color=Colors[i])
        # time.sleep(0.001)
    plt.xlabel('Shaping time($\mu$s)', fontsize=15);plt.ylabel(' '.join([ylabel, 'mean']), fontsize=15)
    if len(ylim)!=0:
        plt.ylim(ylim)
    plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique(), fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(fontsize=15)
    plt.title('_'.join([addToTitle, 'shapingTime_vs_' + ylabel + 'Mean', BL]), fontsize=15)
    plt.savefig(os.path.join(outputDir, '_'.join(['shapingTime_vs_' + ylabel + 'Mean', BL]) + '.png'))
    #
    # save another fig if the distribution is skewed
    # shapingtime vs loc of max
    if skewed:
        plt.figure(figsize=(12,12))
        for gain in tqdm(Gain):
            plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'], y=df[df['Gain']==gain]['loc'],
                        yerr=df[df['Gain']==gain]['scale'],
                        label= '_'.join([BL, str(gain) + 'mV/fC']))
            time.sleep(0.001)
        plt.xlabel('Shaping time');plt.ylabel(' '.join([ylabel, 'locMax']))
        plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique())
        plt.legend()
        plt.title('_'.join([addToTitle, 'shapingTime_vs_' + ylabel + 'locMax', BL]))
        plt.savefig(os.path.join(outputDir, '_'.join(['shapingTime_vs_' + ylabel + 'locMax', BL]) + '.png'))

# plot std/mean vs shaping time
def plot_stdDIVmean_vs_shapingTime(path_to_csv='', BL='200mV', outputDir='',
                                    ylabel='pedestal'):
    dataFrame = pd.read_csv(path_to_csv)
    dataFrame['BL'] = dataFrame['BL'].apply(lambda x : x[:-2])
    condition = (dataFrame['BL']==BL)
    dataFrame = convert_Gain_to_float(dataFrame)
    Gain = dataFrame[condition]['Gain'].unique()
    #-> dataFrame for BL==200mV
    df = dataFrame[condition]
    # -> shaping time to float
    df = convert_Timing_to_float(df)
    df['ratio_std_mean'] = df['std'] / df['mean']
    plt.figure(figsize=(12, 7))
    for gain in Gain:
        plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'],# y=df[df['Gain']==gain]['mean'],
                    y=df[df['Gain']==gain]['ratio_std_mean'],
                    label= '_'.join([BL, str(gain) + 'mV/fC']))
    plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique())
    plt.legend()
    plt.show()
#
#
## The dataFrame needs to have a columns named femb_ids
## Function to remove informations about one femb
def removeInfo_for_FEMB(dataFrame=pd.DataFrame(), fembID=24):
    return dataFrame[dataFrame['femb_ids'] != int(fembID)]

## Function to remove informations about a list of femb
def removeInfo_for_FEMBs(dataFrame=pd.DataFrame(), femb_list=[]):
    df = dataFrame
    for femb_id in femb_list:
        df = removeInfo_for_FEMB(dataFrame=df, fembID=femb_id)
    return df

def saveCorrectedCSV(path_to_csv='', femb_list=[], output_path='', datanames=['Pedestal', 'RMS']):
    '''
        This function removes RMS and Pedestal for some femb ids from the csv files
    '''
    for dataname in datanames:
        path_to_file = '/'.join([path_to_csv, dataname])
        output_path_to_file = '/'.join([output_path, dataname])
        for csvname in os.listdir(path_to_file):
            dataFrame = pd.read_csv('/'.join([path_to_file, csvname]))
            dataFrame = removeInfo_for_FEMBs(dataFrame=dataFrame, femb_list=femb_list)
            dataFrame.to_csv('/'.join([output_path_to_file, csvname]), index=False)


def separateCSV_foreachFEMB(path_to_csv='', output_path='', datanames=['Pedestal', 'RMS']):
    '''
        Having csv files of 4 fembs, this function separate one csv file to 4 csv files for each femb
    '''
    for dataname in datanames:
        path_to_file = '/'.join([path_to_csv, dataname])
        output_path_file = '/'.join([output_path, dataname])
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
                df = pd.read_csv('/'.join([path_to_file, csvname]))
                femb_ids = df['femb_ids'].unique()
                for femb in femb_ids:
                    df_femb = df[df['femb_ids']==femb].reset_index().drop('index', axis=1)
                    femb_csvname = '_'.join(['femb{}'.format(femb), part_csvname + '.csv'])
                    df_femb.to_csv('/'.join([output_path_file, femb_csvname]), index=False)
                    print(femb_csvname)