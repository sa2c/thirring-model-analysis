#!/usr/bin/env python3
import numpy as np
import pandas as pd
from os import path
import numpy as np
from matplotlib import pyplot as plt
import re


def mean_square(series,blocksize):
    '''
    Takes a 1D array and a blocksize as input and returns an unbiased 
    estimator of the square mean, removing the products of terms that might 
    be correlated.
    '''
    return np.triu(
       np.outer(series,series)[:-blockSize,blocksize:]
       ).sum()/(
            (series.size-blocksize)*
            (series.size-blocksize+1)/2)

def variance(series,blocksize):
    '''
    Takes a 1D array and a block size as input and returns an unbiased estimator
    of the variance.
    '''

    return (series**2).mean() - mean_square(series,blocksize)


# stupid blocking, for mean and error
def blockingMeanErr(data0,blockSize):
    '''
    Takes 1D array and block size and outputs mean and error.
    Error is computed assuming that in the limit of large block size 
    correlations are going to be negligible, and if there are enough blocks
    it is possible to esimate the variance of the block mean reliably, obtaining
    and error on the estimator "mean of the block mean" which is just 
    sigma_block_mean / sqrt(no_of_blocks).
    '''
  
    sampleSize = data0.shape[0]
    
    mean = np.mean(data0)

    xblocks = sampleSize/blockSize 
    leftovers = sampleSize%blockSize 
    nblocks = int(np.ceil(xblocks))

#    print("block number: ",nblocks," lefovers:", leftovers, " xblocks:", xblocks)

    data = np.resize(data0, (nblocks,blockSize))

    blockMeans = np.mean(data,axis=1)
    
    if (leftovers) != 0:
        blockMeans[nblocks-1] = np.mean(data[nblocks-1,0:leftovers])
    

    blockedDataWeigths = np.zeros(nblocks) + blockSize
    if (leftovers) != 0:
        blockedDataWeigths[nblocks-1] = leftovers

#    print("Sigma of data: ",np.std(data))
#    print("Mean of data: ",mean)

    standardError = np.sqrt(np.average((blockMeans - mean )**2, weights = blockedDataWeigths)\
            / xblocks)
    
    return mean, standardError


def parameters_from_dirname(dirname):
    match = re.search('Ls(?P<Ls>[0-9]{2})\.beta(?P<beta>0\.[0-9][0-9])\.m(?P<mass>0\.0[0-9])',dirname)

    Ls = int(match['Ls'])
    beta = float(match['beta'])
    mass = float(match['mass'])

    return {'Ls': Ls,'beta': beta,'mass': mass}


def filelist_parser(filename):
    '''
    Takes as input a tab separated value file with analysis settings.
    Returns dataframe containing the same information, indexed by Ls,beta,mass.
    '''
    print(f"Reading {filename}")

    analysis_settings = pd.read_csv(filename,sep='\t',comment='#')

    run_params_list = [ parameters_from_dirname( path.basename(
            path.dirname(filename))) for filename in analysis_settings.filename ]
    
    parnames = ['Ls','beta','mass']
    for parname in parnames:
        analysis_settings[parname] = [ run_params[parname] for run_params in run_params_list ]

    return analysis_settings.set_index(parnames)


def cut_and_paste(analysis_settings):
    ''' 
    Takes as input dataframe containing the same information, indexed by 
    Ls,beta,mass. Returns a dictionary of dataframes with thermalization removed,
    merged by Ls,beta,mass
    '''
    dataframes = dict()
    for idx in analysis_settings.index:
        Ls,beta,mass = idx
        therm_ntrajs = analysis_settings.thermalization[idx].drop_duplicates()[0]
        meas_every = analysis_settings.measevery[idx].drop_duplicates()[0]
        dfs_to_concatenate = []
        for filename in analysis_settings.loc[idx,'filename']:
            df = pd.read_csv(filename.strip())
            thermalization_nmeas = np.ceil(therm_ntrajs/meas_every)
            df = df.tail(-int(thermalization_nmeas))
            dfs_to_concatenate.append(df)

        dataframes[idx] = pd.concat(dfs_to_concatenate,axis='index')

    return dataframes 

            
def scan_for_blocking(df_dict,observable,analysis_settings):
    for k,v in df_dict.items():
        n_meas = len(v[observable])
        bmeassize_range = range(1,n_meas // 5,2) 
        mean_errs = [ blockingMeanErr(v[observable],bsize) for bsize in bmeassize_range]
        y = [ a for a,b in mean_errs]
        ye = [ b for a,b in mean_errs]

        plt.title(k)
        meas_every = analysis_settings.measevery[k].drop_duplicates()[0]
        bsize_range = np.array(bmeassize_range) * meas_every
        plt.errorbar(bsize_range,y,ye)
        plt.show()

def get_values(df_dict,observable,analysis_settings):
    values = pd.DataFrame(index = analysis_settings.index)
    values[observable] = np.zeros_like(values.index)
    values[observable+'Err'] = np.zeros_like(values.index)
    
    bmeas_sizes = analysis_settings.blocksize/analysis_settings.measevery

    bmeas_sizes = bmeas_sizes.reset_index().drop_duplicates()
    bmeas_sizes = bmeas_sizes.set_index(['Ls','beta','mass'])  

    print(bmeas_sizes)

    for k,v in df_dict.items():
        print(k)

        mean,err = blockingMeanErr(v[observable],int(bmeas_sizes[0][k]))

        values[observable][k] = mean
        values[observable+'Err'][k] = err

    return values



def plot_observable(observable,Ls,data):
    for mass in np.arange(0.01,0.06,0.01): 
         condition = (data.Ls == 32) & (data.mass == mass)  
         plt.errorbar(data.beta[condition],
                 data[observable][condition],
                 yerr= data[observable+'Err'][condition],
                 label = 'm='+str(mass),
                 linestyle='None') 

    plt.legend()
    plt.show()



        
        
















