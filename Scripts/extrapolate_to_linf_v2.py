#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.optimize import leastsq, brentq
from sys import argv
import lib
from tabulate import tabulate
import argparse as ap
import os
import glob


def expexpression(A, alpha, constant, x):
    return A * np.exp(-alpha * x) + constant


def residuals(par, x, y, ye):
    A, alpha, constant = par
    ytheo = expexpression(A, alpha, constant, x)
    return (y - ytheo) / ye


def fit_exp_single(df):

    df = df.sort_values(by='Ls')
    x = df['Ls']
    y = df['psibarpsi']
    ye = df['psibarpsiErr']

    yl = list(y)
    xl = list(x)

    constant = yl[-1]
    last_pbp = constant
    last_pbp_e = list(ye)[-1]
    alpha = 0.1

    A = (yl[0] - constant) * np.exp(alpha * xl[0])

    #alpha = -np.log((yl[-3] - yl[-1]) / (yl[-2] - yl[-1])) / (xl[-3] - xl[-2])
    #if np.isnan(alpha) or alpha < 0:
    #    alpha = 0.0

    res = leastsq(func=residuals,
                  x0=np.array([A, alpha, constant]),
                  args=(x, y, ye),
                  full_output=1)

    A = res[0][0]
    alpha = res[0][1]
    constant = res[0][2]

    return A, alpha, constant


def fit_exp(df):

    print("Fitting df:")
    print(df.sort_values(by='Ls'))
    if(len(df)<4):
        return pd.DataFrame(data=None,
                       columns=[
                           'last_pbp', 'last_pbp_e', 'psibarpsi_inf',
                           'psibarpsi_infErr', 'alpha', 'alpha_e', 'A', 'A_e'
                       ])


    # bootstrap
    As = list()
    alphas = list()
    constants = list()

    df = df.sort_values(by='Ls')
    x = df['Ls']
    y = df['psibarpsi']
    ye = df['psibarpsiErr']

    yl = list(y)
    xl = list(x)

    constant = yl[-1]
    last_pbp = constant
    last_pbp_e = list(ye)[-1]

    A, alpha, constant = fit_exp_single(df)

    nboot = 10
    L = df.L.drop_duplicates().values[0]
    beta = df.beta.drop_duplicates().values[0]
    mass = df.mass.drop_duplicates().values[0]

    for _ in range(nboot):
        yresampled = np.random.normal(y, ye)

        if np.any(np.diff(yresampled) < 0) and np.all(np.diff(yresampled) > 0):
            continue

        res = leastsq(func=residuals,
                      x0=np.array([A, alpha, constant]),
                      args=(x, yresampled, ye),
                      full_output=1)

        As.append(res[0][0])
        alphas.append(res[0][1])
        constants.append(res[0][2])

    constant_e = np.std(np.array(constants))
    A_e = np.std(np.array(As))
    alpha_e = np.std(np.array(alphas))
    data = np.array(
        [[last_pbp, last_pbp_e, constant, constant_e, alpha, alpha_e, A, A_e]])

    res = pd.DataFrame(data=data,
                       columns=[
                           'last_pbp', 'last_pbp_e', 'psibarpsi_inf',
                           'psibarpsi_infErr', 'alpha', 'alpha_e', 'A', 'A_e'
                       ])

    print("Results:")
    print(res)

    return res


def aggregate_psibarpsi_dataframes(L, mass, analysis_settings_filename):
    """
    See single_analysis_file_splitter, the $filename variable.
    """
    glob_expression = os.path.join(
        lib.pbpdir, lib.pbp_values_and_error_filename +
        f"L{L}Ls??.beta?.*.m{mass}.{analysis_settings_filename}")
    filenames = glob.glob(glob_expression)

    if len(filenames) is 0:
        print("No filenames matching expression:")
        print(glob_expression)
        exit()

    def read_table(filename):
        print(f"Reading {filename}")
        return pd.read_table(filename, sep=r'\s+', header=0)

    dfs = [read_table(filename) for filename in filenames]
    return pd.concat(dfs)


parser = ap.ArgumentParser(
    description="An utility to extrapolate the condensate data to Ls->+inf.")

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help="The original name of the file containing the thermalization \n"
    "and the block sizes. Used to find the names of the condensate files")

parser.add_argument('mass', type=str, help='The chosen value of the mass')
parser.add_argument('L', type=str, help='The chosen value of L')

args = parser.parse_args()

values_and_errors = aggregate_psibarpsi_dataframes(
    args.L, args.mass, args.analysis_settings_filename)

print("All values considered:")
print(values_and_errors.sort_values(by=['L','beta','mass','Ls']))

extrapolation = values_and_errors.groupby(by=['L','beta','mass']).apply(fit_exp)
os.makedirs(lib.pbp_inf_dir,exist_ok=True)
output_filename = os.path.join(
    lib.pbp_inf_dir,
    f'{args.analysis_settings_filename}_{args.L}_{args.mass}')
print(f"Writing {output_filename}")
extrapolation.to_csv(path_or_buf=output_filename, sep='\t')

print("Extrapolation:")
print(extrapolation)

print("Plotting")

def plot_fit_exp(df_multi):
    from matplotlib import pyplot as plt
    plt.figure()
    plt.xlim([20, 56])

    L = df_multi.L.drop_duplicates().values[0]
    m = df_multi.mass.drop_duplicates().values[0]

    pfes_first_called = False  # workaround for calling apply with a side effectful f

    def plot_fit_exp_single(df):
        # TODO: Check if this is still necessary.
        # workaround for calling apply with a side effectful f
        #nonlocal pfes_first_called
        #if not pfes_first_called:
        #    pfes_first_called = True
        #    return None

        beta = df.beta.drop_duplicates().values[0]

        if (len(df) < 3):
            return None

        df = df.sort_values(by='Ls')
        x = df['Ls']
        y = df['psibarpsi']
        ye = df['psibarpsiErr']

        yl = list(y)
        xl = list(x)

        constant = yl[-1]
        last_pbp = constant
        last_pbp_e = list(ye)[-1]

        A, alpha, constant = fit_exp_single(df)

        print(beta, A, alpha, constant)  #res[0])

        plt.errorbar(x, y, yerr=ye, linestyle='None')
        xplot = np.arange(min(x), max(x), (max(x) - min(x)) / 100)
        p = plt.plot(xplot,
                     expexpression(A, alpha, constant, xplot),
                     label=f'{beta}')
        #plt.plot(xplot,np.ones_like(xplot)*constant,color = p[0].get_color(),linestyle = '--')

    df_multi.groupby(by=['beta']).apply(plot_fit_exp_single)
    plt.legend()
    
    output_filename = os.path.join( lib.pbp_inf_dir, f'pbpextrL{L}_m{m}.png')
    print(f'Writing {output_filename}')
    plt.savefig(output_filename)


values_and_errors.groupby(by=['L', 'mass']).apply(plot_fit_exp)



