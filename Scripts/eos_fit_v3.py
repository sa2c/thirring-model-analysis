#!/usr/bin/env python3
from rounder import rounder
import lib
import pandas as pd
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from matplotlib import pyplot as plt
from scipy.optimize import leastsq, brentq
import numpy as np
import argparse as ap
from sys import stdout, exit
from tabulate import tabulate
import os
import glob


def aggregate_psibarpsi_dataframes(Ls, L, analysis_settings_filename):
    """
    See single_analysis_file_splitter, the $filename variable.
    Collect all relevant analysis setting files, grouped by L and Ls.
    """
    glob_expression = os.path.join(
        lib.pbpdir, lib.pbp_values_and_error_filename +
        f"L{L}Ls{Ls}.beta0.*m0.0*.{analysis_settings_filename}")
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
    description=
    "An utility to plot and fit the condensate data for a single value of Ls.")

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help="The original name of the file containing the thermalization \n"
    "and the block sizes. Used to find the names of the condensate files")

parser.add_argument('Ls', type=str, help='The chosen value of Ls')

parser.add_argument('L', type=int, help='The chosen value of L')

parser.add_argument('min_beta', type=float, help='The minimum value of beta for the fits.')
parser.add_argument('max_beta', type=float, help='The maximum value of beta for the fits.')

parser.add_argument('--savefig',
                    action='store_true',
                    help='flag to save figure instead of showing it')

args = parser.parse_args()

# Parsing analysis settings, getting dataframe
Ls = args.Ls
L = args.L
min_beta = args.min_beta
max_beta = args.max_beta

values_and_errors = aggregate_psibarpsi_dataframes(
    L=L, Ls=Ls, analysis_settings_filename=args.analysis_settings_filename)

# Saving pbp and pbp_err in different files for each mass
# for each Ls and L
os.makedirs(lib.eos_fit_dir,exist_ok=True)
for mass in set(values_and_errors.mass):
    filename = os.path.join(lib.eos_fit_dir,f'cond_m0{int(mass/0.01)}_Ls{Ls}_L{L}')
    selection = (values_and_errors.mass == mass) 
    dftosave = values_and_errors.loc[selection,
                                     ['beta', 'psibarpsi', 'psibarpsiErr']]
    print(f"Writing {filename}")
    cols = list(dftosave.columns)
    cols[0] = '#beta'  # dirty trick
    dftosave.columns = cols
    dftosave = dftosave.set_index('#beta')  # dirty trick
    dftosave.to_csv(filename, sep='\t')

# Selecting values of interest
condition = (values_and_errors.beta >= min_beta) & (values_and_errors.beta <= max_beta) 


values_and_errors_selected = values_and_errors.loc[condition, :]
lib.plot_observable('psibarpsi', values_and_errors_selected)

import eos_fit_lib as efl

output = leastsq(func=efl.residuals,
                 x0=efl.initial_guesses[L][Ls],
                 args=(values_and_errors_selected.beta,
                       values_and_errors_selected.psibarpsi,
                       values_and_errors_selected.psibarpsiErr,
                       values_and_errors_selected.mass),
                 full_output=1, maxfev=5000)

found_params = output[0]
A, betac, p, B, delta = found_params
print("Found params", found_params)

final_residuals = output[2]['fvec']
cov = output[1]
residual_variance = final_residuals.var()

#reduced_chi_square
num = (final_residuals**2).sum()
den = (len(final_residuals) - len(found_params))

if cov is not None:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
    #  To obtain the covariance matrix of the parameters x,
    #  cov_x must be multiplied by the variance of the residuals
    A_err, betac_err, p_err, B_err, delta_err = np.sqrt(
        np.diag(cov) * residual_variance)

    def valerr_string(val, err):
        string, exp10 = rounder(val, err)
        return f"{string}\cdot10^{{{exp10}}}" if exp10 is not 0 else f"{string}"
    
    
    betac_str = valerr_string(betac, betac_err)
    delta_str = valerr_string(delta, delta_err)
    plt.title(
        f"$L_s={Ls}$,$L={L}$, $\chi^2/n_{{dof}} = {num:.2f}/{den}$, $b={betac_str}$,$d={delta_str}$,$B={B:.2f}$"
    )
    # writing fit parameters
    filename = os.path.join(lib.eos_fit_dir,f'fitLs{Ls}L{L}.dat')
    columns = ["A", "A_err", "betac", "betac_err", "p", "p_err", "B", "B_err", "delta", "delta_err"]
    data = [A, A_err, betac, betac_err, p, p_err, B, B_err, delta, delta_err]
    df = pd.DataFrame(data = dict(zip(columns,data)), index = [0])
    print(f"Writing {filename}")
    df.to_csv(path_or_buf = filename, sep = '\t', index = False)

else: 
    plt.title(f"$L_s={Ls}$, $\chi^2/n_{{dof}} = {num:1.2f}/{den}$, $b={betac}$,$d={delta}$,$B={B}$")

iterables = [np.arange(0.01, 0.06, 0.01), np.arange(0.25, 0.6, 0.004)]
index = pd.MultiIndex.from_product(iterables, names=['mass', 'beta'])

psibarpsi = pd.Series(index=index)
for mass, beta in psibarpsi.index:
    psibarpsi[(mass, beta)] = brentq(
        f=lambda y: efl.equation_of_state(y, beta, mass, *found_params),
        a=0.0,
        b=0.5)

for mass in psibarpsi.index.levels[0]:
    plt.plot(psibarpsi[mass], color='black', linestyle='--')

if args.savefig:
    filename = os.path.join(lib.eos_fit_dir,f'fitLs{Ls}L{L}.png')
    print(f"Writing {filename}")
    plt.savefig(filename)

else:
    plt.show()
