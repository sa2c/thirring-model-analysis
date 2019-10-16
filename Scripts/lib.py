#!/usr/bin/env python3
import numpy as np
import pandas as pd
from os import path
import numpy as np
from matplotlib import pyplot as plt
import re

numeric_types = [np.int, np.int64, np.float, np.float64]

pbp_values_and_error_filename = 'psibarpsi'
pbp_values_and_error_pretty_filename = 'psibarpsi.pretty'
pbp_inf_dir = 'psibarpsi_extrapolated'
pbp_inf_filename_pretty = 'psibarpsi_extrapolated_pretty'

pbpdir = 'psibarpsi'
eos_fit_dir = 'eos_fit'


def mean_square(series, blocksize):
    '''
    Takes a 1D array and a blocksize as input and returns an unbiased 
    estimator of the square mean, removing the products of terms that might 
    be correlated.
    '''
    return np.triu(np.outer(series, series)[:-blockSize, blocksize:]).sum() / (
        (series.size - blocksize) * (series.size - blocksize + 1) / 2)


def variance(series, blocksize):
    '''
    Takes a 1D array and a block size as input and returns an unbiased estimator
    of the variance.
    '''

    return (series**2).mean() - mean_square(series, blocksize)


# stupid blocking, for mean and error
def blockingMeanErr(data0, blockSize):
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

    xblocks = sampleSize / blockSize
    leftovers = sampleSize % blockSize
    nblocks = int(np.ceil(xblocks))

    data = np.resize(data0, (nblocks, blockSize))

    blockMeans = np.mean(data, axis=1)

    if (leftovers) != 0:
        blockMeans[nblocks - 1] = np.mean(data[nblocks - 1, 0:leftovers])

    blockedDataWeigths = np.zeros(nblocks) + blockSize
    if (leftovers) != 0:
        blockedDataWeigths[nblocks - 1] = leftovers


    standardError = np.sqrt(np.average((blockMeans - mean )**2, weights = blockedDataWeigths)\
            / xblocks)

    return mean, standardError


def parameters_from_dirname(dirname):
    match = re.search(
        'Ls(?P<Ls>[0-9]{2})\.beta(?P<beta>0\.[0-9][0-9])\.m(?P<mass>0\.0[0-9])',
        dirname)

    Ls = int(match['Ls'])
    beta = float(match['beta'])
    mass = float(match['mass'])

    return {'Ls': Ls, 'beta': beta, 'mass': mass}


def filelist_parser(filename):
    '''
    Takes as input a tab separated value file with analysis settings.
    Returns dataframe containing the same information, indexed by L,Ls,beta,mass.
    '''
    print(f"Reading {filename}")
    analysis_settings = pd.read_table(filename,
                                      sep=r'\s+',
                                      comment='#',
                                      header=0)

    run_params_list = [{
        'L':
        L,
        **(parameters_from_dirname(path.basename(path.dirname(filename))))
    } for filename, L in zip(analysis_settings.filename, analysis_settings.L)]

    parnames = ['L', 'Ls', 'beta', 'mass']
    for parname in parnames:
        analysis_settings[parname] = [
            run_params[parname] for run_params in run_params_list
        ]

    print(analysis_settings.set_index(parnames))
    return analysis_settings.set_index(parnames)

def read_all_files(analysis_settings):
    ''' 
    Takes as input dataframe containing the same information, indexed by 
    L,Ls,beta,mass. Returns a dictionary of df_dict with thermalization removed,
    merged by L,Ls,beta,mass
    '''
    df_dict = dict()

    for idx in set(analysis_settings.index):
        L, Ls, beta, mass = idx

        dfs = []
        print("Concatenating dfs...")
        filename_data = analysis_settings.loc[[idx], 'filename']
        therm_ntrajs_data = analysis_settings.loc[[idx], 'thermalization']
        meas_every_data = analysis_settings.loc[[idx], 'measevery']

        assert len(meas_every_data.drop_duplicates()) == 1

        for filename, therm_ntrajs, meas_every in zip(filename_data,
                                                      therm_ntrajs_data,
                                                      meas_every_data):
            print(f"Reading {filename}")
            df = pd.read_table(filename.strip(), sep=r'\s+', header=0)
            thermalization_nmeas = np.ceil(therm_ntrajs / meas_every)
            print(f"Nmeas before cut: {len(df)}")
            df_sane = df.tail(-int(thermalization_nmeas))
            df_therm = df.head(int(thermalization_nmeas))
            print(f"Nmeas to append: {len(df_sane)}")
            df = {'therm' :  df_therm, 'sane' : df_sane }

            dfs.append(df)

        df_dict[idx] = dfs

    return df_dict


def cut_and_paste(analysis_settings):
    ''' 
    Takes as input dataframe containing the same information, indexed by 
    L,Ls,beta,mass. Returns a dictionary of df_dict with thermalization removed,
    merged by L,Ls,beta,mass
    '''
    df_dict = dict()

    for idx in set(analysis_settings.index):
        L, Ls, beta, mass = idx

        dfs_to_concatenate = []
        print("Concatenating dfs...")
        filename_data = analysis_settings.loc[[idx], 'filename']
        therm_ntrajs_data = analysis_settings.loc[[idx], 'thermalization']
        meas_every_data = analysis_settings.loc[[idx], 'measevery']

        assert len(meas_every_data.drop_duplicates()) == 1

        for filename, therm_ntrajs, meas_every in zip(filename_data,
                                                      therm_ntrajs_data,
                                                      meas_every_data):
            print(f"Reading {filename}")
            df = pd.read_table(filename.strip(), sep=r'\s+', header=0)
            thermalization_nmeas = np.ceil(therm_ntrajs / meas_every)
            print(f"Nmeas before cut: {len(df)}")
            df = df.tail(-int(thermalization_nmeas))
            print(f"Nmeas to append: {len(df)}")

            dfs_to_concatenate.append(df)

        df_dict[idx] = pd.concat(dfs_to_concatenate,
                                 axis='index').reset_index()

        print(f"Total nmeas: {len(df_dict[idx])}")

    return df_dict


def scan_for_blocking(df_dict,df_dict_cut, observable, analysis_settings):
    for k in sorted(df_dict.keys()):
        vs_both  = df_dict[k]
        count = 1
        for v_both in vs_both:
            v = v_both['sane']
            therm = v_both['therm']

            plt.title("{}-{}".format(k, observable))
            x = np.arange(len(therm[observable]))
            plt.plot(x,therm[observable], label = str(count)+'_therm')
            x = np.arange(len(v[observable])) + len(therm[observable])
            plt.plot(x, v[observable], label = str(count))
            count += 1

        plt.show()
        v = df_dict_cut[k]
        n_meas = len(v[observable])
        bmeassize_range = range(1, n_meas // 5, 2)
        mean_errs = [
            blockingMeanErr(v[observable], bsize) for bsize in bmeassize_range
        ]
        y = [a for a, b in mean_errs]
        ye = [b for a, b in mean_errs]

        plt.title("{}-{}".format(k, observable))
        meas_every_data = analysis_settings.measevery[k]
        meas_every = meas_every_data if type(
            meas_every_data
        ) in numeric_types else meas_every_data.drop_duplicates()[0]
        bsize_range = np.array(bmeassize_range) * meas_every
        plt.errorbar(bsize_range, y, ye)
        plt.show()


def get_values_and_errors(df_dict, observable, analysis_settings):
    values_and_errors = pd.DataFrame(
        index=analysis_settings.index.drop_duplicates())
    values_and_errors[observable] = np.zeros_like(values_and_errors.index)
    values_and_errors[observable + 'Err'] = np.zeros_like(
        values_and_errors.index)

    bmeas_sizes = analysis_settings.blocksize / analysis_settings.measevery

    bmeas_sizes = bmeas_sizes.reset_index().drop_duplicates()
    bmeas_sizes = bmeas_sizes.set_index(['L', 'Ls', 'beta', 'mass'])

    for k, v in df_dict.items():
        try:
            mean, err = blockingMeanErr(v[observable], int(bmeas_sizes[0][k]))
            values_and_errors.loc[k, observable] = mean
            values_and_errors.loc[k, observable + 'Err'] = err
        except TypeError:
            with open('errors.txt', 'a') as f:
                f.write(f'Error: {k} {bmeas_sizes[0][k]} \n')
                print('Error, fix analysis settings file (check errors.txt)')

    return values_and_errors.reset_index()


def plot_observable(observable, values_and_error_selected):
    for mass in np.arange(0.01, 0.06, 0.01):
        condition = (values_and_error_selected.mass == mass)
        plt.errorbar(values_and_error_selected.beta[condition],
                     values_and_error_selected[observable][condition],
                     yerr=values_and_error_selected[observable +
                                                    'Err'][condition],
                     label='m=' + str(mass),
                     linestyle='None',
                     marker='+')

    plt.legend()
