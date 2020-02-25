#!/usr/bin/env python3
from rounder import rounder
import lib
import libsusc
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
from pbp_data_processing_v2 import aggregate_psibarpsi_dataframes

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

parser.add_argument('--savefig',
                    action='store_true',
                    help='flag to save figure instead of showing it')

args = parser.parse_args()

# Parsing analysis settings, getting dataframe
Ls = args.Ls
L = args.L

values_and_errors = aggregate_psibarpsi_dataframes(
    L=L, Ls=Ls, analysis_settings_filename=args.analysis_settings_filename)

# Saving pbp and pbp_err in different files for each mass
# for each Ls and L
os.makedirs(libsusc.suscdir,exist_ok=True)
for mass in set(values_and_errors.mass.drop_duplicates()):
    filename = os.path.join(libsusc.suscdir,f'susc_m{mass:1.3f}_Ls{Ls}_L{L}')
    selection = (values_and_errors.mass == mass) 
    dftosave = values_and_errors.loc[selection,
                                     ['beta', libsusc.susccol, libsusc.susccol+'Err']]
    print(f"Writing {filename}")
    cols = list(dftosave.columns)
    cols[0] = '#beta'  # dirty trick
    dftosave.columns = cols
    dftosave = dftosave.set_index('#beta')  # dirty trick
    dftosave.to_csv(filename, sep='\t')

lib.plot_observable(libsusc.susccol, values_and_errors)

plt.title(f"$L={L}, L_s={Ls}$")

if args.savefig:
    filename = os.path.join(libsusc.suscdir,f'Ls{Ls}L{L}.png')
    print(f"Writing {filename}")
    plt.savefig(filename)

else:
    plt.show()
