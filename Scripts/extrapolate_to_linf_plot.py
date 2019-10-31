#!/usr/bin/env python3
import numpy as np
import pandas as pd
import lib
from tabulate import tabulate
import argparse as ap
import os
import extrapolation_library as el


def plot_fit_exp(df_psibarpsi_multi, df_fitres_multi):
    from matplotlib import rc
    rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    ## for Palatino and other serif fonts use:
    #rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    from matplotlib import pyplot as plt
    plt.figure(figsize=(7.0,6.0))
    xmin = min(df_psibarpsi_multi['Ls'])
    xmax = max(df_psibarpsi_multi['Ls'])
    plt.xlim([xmin - 8, xmax + 4])

    L = df_psibarpsi_multi.L.drop_duplicates().values[0]
    m = df_psibarpsi_multi.mass.drop_duplicates().values[0]

    #pfes_first_called = False  # workaround for calling apply with a side effectful f

    def plot_fit_exp_single(df_psibarpsi, df_fitres_multi):
        # TODO: Check if this is still necessary.
        # workaround for calling apply with a side effectful f
        #nonlocal pfes_first_called
        #if not pfes_first_called:
        #    pfes_first_called = True
        #    return None

        beta = df_psibarpsi.beta.drop_duplicates().values[0]

        df_psibarpsi = df_psibarpsi.sort_values(by='Ls')
        x = df_psibarpsi['Ls']
        y = df_psibarpsi['psibarpsi']
        ye = df_psibarpsi['psibarpsiErr']

        print("Fitres:")
        print(df_fitres_multi)
        print(f"beta: {beta}")

        condition = df_fitres_multi['beta'] == beta
        A = df_fitres_multi.A[condition].values[0]
        alpha = df_fitres_multi.alpha[condition].values[0]
        constant = df_fitres_multi.constant[condition].values[0]
        redchisq = df_fitres_multi.redchisq[condition].values[0]

        print(beta, A, alpha, constant)

        xplot = np.arange(min(x), max(x), (max(x) - min(x)) / 100)
        p = plt.plot(xplot,
                     el.expexpression(A, alpha, constant, xplot),
                     label=f'$\\beta:{beta:1.2f},\chi^2/n_{{dof}}:{redchisq:1.1f}$')
        plt.errorbar(x, y, yerr=ye, linestyle='None', color = p[0].get_color())
        plt.plot(x, y, linestyle='None', marker='+', color = p[0].get_color())

    df_psibarpsi_multi.loc[df_psibarpsi_multi.beta.isin(
        df_fitres_multi.beta), :].groupby(by=['beta', 'mass', 'L']).apply(
            lambda x: plot_fit_exp_single(x, df_fitres_multi))

    plt.xlabel(r'$L_s$')
    plt.ylabel(r'$\bar{\psi}\psi$')
    plt.title(r'Exponential Extrapolation: $\lim_{{L_s\rightarrow \infty }} \bar{{\psi}}\psi(L_s)$ , $L={L}$ , $m={m}$'.format(L=L,m=m))

    plt.legend(loc='upper left')

    output_filename = os.path.join(lib.pbp_inf_dir, f'pbpextrL{L}_m{m}.png')
    print(f'Writing {output_filename}')
    plt.savefig(output_filename)


def aggregate_psibarpsi_dataframes(L, mass, analysis_settings_filename):
    """
    See single_analysis_file_splitter, the $filename variable.
    Collects all relevant analysis setting files, grouped by L and mass.
    Values for multiple beta will be plotted in the same figure.
    """
    import glob
    glob_expression = os.path.join(
        lib.pbpdir, lib.pbp_values_and_error_filename +
        f"L{L}Ls*.beta0.*.m{float(mass):1.6f}.{analysis_settings_filename}")
    filenames = glob.glob(glob_expression)

    if len(filenames) is 0:
        print("No filenames matching expression:")
        print(glob_expression)
        print(
            f"analysis_settings_filename: {analysis_settings_filename} L: {L}, mass: {mass}"
        )
        exit()

    def read_table(filename):
        print(f"Reading {filename}")
        return pd.read_table(filename, sep=r'\s+', header=0)

    dfs = [read_table(filename) for filename in filenames]
    return pd.concat(dfs)


def aggregate_fit_inf_dataframes(L, mass, analysis_settings_filename):
    """
    Collects all relevant fit result files, grouped by L and mass.
    """
    import glob

    glob_expression = el.fit_output_filename_format(
        analysis_settings_filename=analysis_settings_filename,
        L=L,
        beta=r'0.*',
        mass=mass)

    filenames = glob.glob(glob_expression)
    print(glob_expression)

    if len(filenames) is 0:
        print("No filenames matching expression:")
        print(glob_expression)
        print(
            f"analysis_settings_filename: {analysis_settings_filename} L: {L}, beta : '0.*' mass: {mass}"
        )
        exit()

    def read_table(filename):
        print(f"Reading {filename}")
        return pd.read_table(filename, sep=r'\s+', header=0)

    dfs = [read_table(filename) for filename in filenames]
    return pd.concat(dfs)


parser = ap.ArgumentParser(
    description=
    "An utility to plot the extrapolation of the condensate data to Ls->+inf.")

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help="The original name of the file containing the thermalization \n"
    "and the block sizes. Used to find the names of the condensate files")

parser.add_argument('mass', type=str, help='The chosen value of the mass')
parser.add_argument('L', type=str, help='The chosen value of L')

args = parser.parse_args()

values_and_errors = aggregate_psibarpsi_dataframes(
    L=args.L,
    mass=args.mass,
    analysis_settings_filename=args.analysis_settings_filename)

fit_inf_params = aggregate_fit_inf_dataframes(
    L=args.L,
    mass=args.mass,
    analysis_settings_filename=args.analysis_settings_filename)

print("Values of the condensate:")
print(values_and_errors)

print("Values of the fitted parameters:")
print(fit_inf_params)

plot_fit_exp(values_and_errors, fit_inf_params)
