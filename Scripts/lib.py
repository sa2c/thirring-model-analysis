#!/usr/bin/env python3
import numpy as np
import pandas as pd
from os import path
import numpy as np
import matplotlib
matplotlib.use("AGG")
from itertools import cycle
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from matplotlib import pyplot as plt
import re
import fort_colnames as fc

numeric_types = [np.int, np.int64, np.float, np.float64]

pbp_values_and_error_filename = 'psibarpsi'
pbp_values_and_error_pretty_filename = 'psibarpsi.pretty'
pbpdir = 'psibarpsi'
eos_fit_dir = 'eos_fit'

# name of the column in the output from pbp_data_processing.py 
pbpcol = fc.fort200cols[0]

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
            / (xblocks -1) ) # -1 for bias correction

    return mean, standardError


def parameters_from_dirname(dirname):
    match = re.search(
        'Ls(?P<Ls>[0-9]+)\.beta(?P<beta>0\.[0-9]+)\.m(?P<mass>0\.0[0-9]+)',
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
    analysis_settings = pd.read_table(
        filename, sep=r'\s+', comment='#', header=0)

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

    return analysis_settings.set_index(parnames)


def read_all_files(analysis_settings):
    ''' 
    Takes as input dataframe containing the same information, indexed by 
    L,Ls,beta,mass. Returns a dictionary, where each datafile has been split 
    into 2 parts, the thermalisation and the proper data after that.
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

        for filename, therm_ntrajs, meas_every in zip(
                filename_data, therm_ntrajs_data, meas_every_data):
            print(f"Reading {filename}")
            df = pd.read_table(filename.strip(), sep=r'\s+', header=0)
            thermalization_nmeas = np.ceil(therm_ntrajs / meas_every)
            print(f"Nmeas before cut: {len(df)}")
            df_sane = df.tail(-int(thermalization_nmeas))
            df_therm = df.head(int(thermalization_nmeas))
            print(f"Nmeas to append: {len(df_sane)}")
            df = {'therm': df_therm, 'sane': df_sane}

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
        meas_every = meas_every_data.drop_duplicates().values[0]

        for filename, therm_ntrajs in zip(filename_data, therm_ntrajs_data):
            print(f"Reading {filename}")
            df = pd.read_table(filename.strip(), sep=r'\s+', header=0)
            thermalization_nmeas = np.ceil(therm_ntrajs / meas_every)
            print(f"Nmeas before cut: {len(df)}")
            df = df.tail(-int(thermalization_nmeas))
            print(f"Nmeas to append: {len(df)}")

            dfs_to_concatenate.append(df)

        df_dict[idx] = pd.concat(
            dfs_to_concatenate, axis='index', sort = True).reset_index()

        print(f"Total nmeas: {len(df_dict[idx])}")

    return df_dict


def get_n_meas(analysis_settings):
    ''' 
    Takes as input dataframe containing the same information, indexed by 
    L,Ls,beta,mass. Returns a data frame with number of valid measures, block
    size, L,Ls,beta,mass.
    '''
    df_data = []

    for idx in set(analysis_settings.index):
        L, Ls, beta, mass = idx

        filename_data = analysis_settings.loc[[idx], 'filename']
        therm_ntrajs_data = analysis_settings.loc[[idx], 'thermalization']
        meas_every_data = analysis_settings.loc[[idx], 'measevery']

        assert len(meas_every_data.drop_duplicates()) == 1
        meas_every = meas_every_data.drop_duplicates().values[0]
        blocksize = analysis_settings.loc[[idx],
                                          'blocksize'].drop_duplicates()[0]

        nlines = 0
        nfiles = 0
        for filename, therm_ntrajs in zip(filename_data, therm_ntrajs_data):
            print(f"Reading {filename}")
            with open(filename.strip()) as f:
                nlines += len(f.readlines()) - 1
            thermalization_nmeas = np.ceil(therm_ntrajs / meas_every)
            nlines -= thermalization_nmeas
            nfiles += 1

        df_data.append((L, Ls, beta, mass, int(nlines * meas_every), blocksize,
                        int(nlines * meas_every) / blocksize, nfiles))

    return pd.DataFrame(
        data=df_data,
        columns=[
            'L', 'Ls', 'beta', 'mass', 'ntraj', 'blocksize', 'ratio', 'nfiles'
        ])


def scan_for_blocking(df_dict, df_dict_cut, observable, analysis_settings):

    import threading
    list_need_more_statistics = open('need_more_statistics.txt', 'w')

    with open('new_analysis_settings.set', 'w') as f:
        f.write('L\t')
        for col in analysis_settings.columns:
            f.write(f'{col}\t')
        f.write('\n')

        # plot all runs with a certain parameter
        for k in sorted(df_dict.keys()):
            vs_both = df_dict[k]
            measevery_data = analysis_settings.measevery[k]
            measevery = measevery_data if type(
                measevery_data
            ) in numeric_types else measevery_data.drop_duplicates()[0]

            assert type(measevery_data) in numeric_types or len(
                measevery_data.drop_duplicates()) is 1

            count = 1
            for v_both in vs_both:

                v = v_both['sane']
                therm = v_both['therm']

                plt.title("{}-{}".format(k, observable))
                x = np.arange(len(therm[observable])) * measevery
                plt.plot(x, therm[observable], label=str(count) + '_therm')
                x = (np.arange(len(v[observable])) + len(
                    therm[observable])) * measevery
                plt.plot(x, v[observable], label=str(count))
                count += 1

            plt.legend()
            # get new thermalisation values, for all runs with the same parameters
            new_thermalizations = []
            need_more_statistics = False

            def work1():
                nonlocal new_thermalizations
                nonlocal analysis_settings
                nonlocal x
                nonlocal need_more_statistics
                count = 1
                thermalizations = analysis_settings.loc[[k], 'thermalization']
                print(f"Parameters {k}")
                for thermalization in thermalizations:
                    print(
                        f"copy no {count}, current thermalisation: {thermalization}. ",
                        end='')
                    print("new thermalisation:", end='')
                    c = input()
                    try:
                        if c == 'N':
                            need_more_statistics = True
                            new_thermalization = thermalization
                        else:
                            new_thermalization = int(c)
                    except:
                        new_thermalization = thermalization
                    print("New value: ", new_thermalization)
                    new_thermalizations.append(new_thermalization)
                    count += 1

            x = threading.Thread(target=work1)
            x.start()

            plt.show()
            x.join()
            print(f"New thermalizations - post join: {new_thermalizations}")

            # computing error vs blocksize
            v = df_dict_cut[k]
            n_meas = len(v[observable])
            bmeassize_range = range(1, n_meas // 5, 2)
            mean_errs = [
                blockingMeanErr(v[observable], bsize)
                for bsize in bmeassize_range
            ]
            y = [a for a, b in mean_errs]
            ye = [b for a, b in mean_errs]

            plt.title("{}-{}".format(k, observable))
            bsize_range = np.array(bmeassize_range) * measevery
            plt.errorbar(bsize_range, y, ye)

            # plotting current value
            current_blocksize_data = analysis_settings.blocksize[k]
            current_blocksize = current_blocksize_data if type(
                current_blocksize_data
            ) in numeric_types else current_blocksize_data.drop_duplicates()[0]

            y_current, ye_current = blockingMeanErr(
                v[observable], int(current_blocksize / measevery))
            plt.errorbar([current_blocksize], [y_current], [ye_current])

            # show error vs blocksize
            print(f"current block size: {current_blocksize}")

            new_blocksize = current_blocksize

            def work2():
                nonlocal need_more_statistics
                nonlocal new_blocksize
                print("new blocksize:", end='')
                c = input()
                try:
                    if c == 'N':
                        need_more_statistics = True
                        new_blocksize = current_blocksize
                    else:
                        new_blocksize = int(c)
                except:
                    new_blocksize = current_blocksize
                print("New value: ", new_blocksize)

            x = threading.Thread(target=work2)
            x.start()
            plt.show()
            x.join()
            print("New value - post-join: ", new_blocksize)

            L, Ls, beta, mass = k
            filenames = analysis_settings.loc[[k], 'filename']
            measeverys = analysis_settings.loc[[k], 'measevery']

            for new_thermalization, filename in zip(new_thermalizations,
                                                    filenames):

                for thing in [
                        L, filename, new_thermalization, new_blocksize,
                        measevery
                ]:
                    f.write(f'{thing}\t')
                f.write('\n')

            if need_more_statistics:
                list_need_more_statistics.write(str(k))
                list_need_more_statistics.write('\n')

    list_need_more_statistics.close()


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


def plot_observable(observable, values_and_error_selected,lateral_shift = False):
    nmasses = len(values_and_error_selected.mass.drop_duplicates())
    colors = cycle(['black','red','blue'])
    markers = cycle(['*','o','^','D','v',])
    for i,mass in enumerate(sorted(values_and_error_selected.mass.drop_duplicates())):
        condition = (values_and_error_selected.mass == mass)
        x = values_and_error_selected.beta[condition]

        xsorted = sorted(x.values)
        maxshift = (xsorted[1] - xsorted[0])/4
        x_shifted = x + maxshift*(i/nmasses-0.5)

        y = values_and_error_selected[observable][condition]
        plt.errorbar(
            x if not lateral_shift else x_shifted,
            y,
            yerr=values_and_error_selected[observable + 'Err'][condition],
            label=f'$m={mass}$',
            linestyle='None',
            color  = next(colors),
            marker = next(markers))

    plt.legend()
