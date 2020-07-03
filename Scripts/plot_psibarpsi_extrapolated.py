#!/usr/bin/env python3
import numpy as np
import pandas as pd
import extrapolation_library as el
import argparse as ap
import matplotlib
matplotlib.use("AGG")
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from matplotlib import pyplot as plt
import os
import lib


def aggregate_fit_inf_dataframes(L, analysis_settings_filename):
    """
    Collects all relevant fit result files, grouped by L.
    """
    import glob

    glob_expression = el.fit_output_filename_format(
        analysis_settings_filename=analysis_settings_filename,
        L=L,
        beta=r'0.*',
        mass=r'0.*')

    filenames = glob.glob(glob_expression)
    print(glob_expression)

    if len(filenames) is 0:
        print("No filenames matching expression:")
        print(glob_expression)
        print(
            f"analysis_settings_filename: {analysis_settings_filename} L: {L}, beta : '0.*' mass: '0.*'"
        )
        exit()

    def read_table(filename):
        print(f"Reading {filename}")
        return pd.read_table(filename, sep=r'\s+', header=0)

    dfs = [read_table(filename) for filename in filenames]
    return pd.concat(dfs)


parser = ap.ArgumentParser(
    description="An utility to plot the condensate data in the limit Ls->+inf."
)

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help="The original name of the file containing the thermalization \n"
    "and the block sizes. Used to find the names of the condensate files")

parser.add_argument('L', type=str, help='The chosen value of L')
parser.add_argument('betamax', type=float, help='Maximum value for Beta')

args = parser.parse_args()

fit_inf_params = aggregate_fit_inf_dataframes(
    L=args.L, analysis_settings_filename=args.analysis_settings_filename)

masses = fit_inf_params.mass.drop_duplicates()

betas = fit_inf_params.beta.drop_duplicates().sort_values()
step = betas.values[1] - betas.values[0]
for mass in sorted(masses):
    condition = (fit_inf_params.mass == mass) & (fit_inf_params.beta <= args.betamax)
    df = fit_inf_params.loc[condition, :]
    offset = step / 3 * (mass / max(masses) - 0.5)
    print(mass, offset)
    p = plt.errorbar(x=df.beta + offset,
                     y=df.constant,
                     linestyle='None',
                     yerr=df.constant_e,
                     label=f'$m={mass}$')
    plt.plot(df.beta + offset,
             df.constant,
             linestyle='None',
             color=p[0].get_color(),
             marker=".")

plt.legend()
plt.xlabel(r'$\beta$')
plt.ylabel(r'$\bar{\psi}\psi_{\infty}$')
plt.title(f"$L={args.L}$ (tentative)")
output_filename = os.path.join(el.pbp_inf_dir, f'pbpextrL{args.L}.png')
print(f'Writing {output_filename}')
plt.savefig(output_filename)
