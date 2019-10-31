#!/usr/bin/env python3
import extrapolation_library as el
from rounder import rounder
import lib
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import leastsq, brentq
import numpy as np
import argparse as ap
from sys import stdout
from tabulate import tabulate

parser = ap.ArgumentParser(
    description=
    "An utility to plot and fit the condensate data for a single value of L (Ls=inf)")

parser.add_argument('L', type=int, help='The chosen value of L')

parser.add_argument(
    '--savefig',
    action='store_true',
    help='flag to save figure instead of showing it')

args = parser.parse_args()

# Parsing analysis settings, getting dataframe
L = args.L

print(f'Reading {el.pbp_inf_filename}')
values_and_errors  = pd.read_table(el.pbp_inf_filename, sep=r'\s+',header=0)

# for each and L
for mass in set(values_and_errors.mass):
    filename = f'cond_m0{int(mass/0.01)}_LsINF_L{L}'
    selection = (values_and_errors.mass == mass) & (values_and_errors.L == L)

    dftosave = values_and_errors.loc[selection,
                                     ['beta', 'psibarpsi', 'psibarpsiErr']]
    print(f"Writing {filename}")
    cols = list(dftosave.columns)
    cols[0] = '#beta'  # dirty trick
    dftosave.columns = cols
    dftosave = dftosave.set_index('#beta')  # dirty trick
    dftosave.to_csv(filename, sep='\t')

# Selecting values of interest
condition = (values_and_errors.L == L)
values_and_errors_selected = values_and_errors.loc[condition, :]
lib.plot_observable('psibarpsi_inf', values_and_errors_selected)

import eos_fit_lib as efl


nboot = 100
found_paramss = []
for _ in range(nboot):
    yresampled = np.random.normal(values_and_errors_selected.psibarpsi_inf,
              values_and_errors_selected.psibarpsi_infErr)

    output = leastsq(
        func=efl.residuals,
        x0=efl.initial_guesses[L][48],
        args=(values_and_errors_selected.beta,
              yresampled,
              values_and_errors_selected.psibarpsi_infErr,
              values_and_errors_selected.mass)
        )

    found_params = output[0]
    found_paramss.append(found_params)

found_paramss = np.array(found_paramss)
found_params = found_paramss.mean(axis=0)
found_params_err = found_paramss.std(axis=0)

A, betac, p, B, delta = found_params
print("Found params", found_params)

output = leastsq(
    func=efl.residuals,
    x0=found_params,
    args=(values_and_errors_selected.beta,
          yresampled,
          values_and_errors_selected.psibarpsi_infErr,
          values_and_errors_selected.mass),
    full_output = 1
    )


final_residuals = output[2]['fvec']
A_err, betac_err, p_err, B_err, delta_err = found_params_err 

#reduced_chi_square
num = (final_residuals**2).sum()
den = (len(final_residuals) - len(found_params))


def valerr_string(val, err):
    string, exp10 = rounder(val, err)
    return f"{string}·10^({exp10})" if exp10 is not 0 else f"{string}"


betac_str = valerr_string(betac, betac_err)
delta_str = valerr_string(delta, delta_err)
plt.title(
    f"Ls=inf,L={L} X^2/ndof = {num:.2f}/{den}, b={betac_str},d={delta_str},B={B:.2f}"
)


iterables = [np.arange(0.01, 0.06, 0.01), np.arange(0.25, 0.6, 0.004)]
index = pd.MultiIndex.from_product(iterables, names=['mass', 'beta'])

psibarpsi = pd.Series(index=index)
for mass, beta in psibarpsi.index:
    psibarpsi[(mass, beta)] = brentq(
        f=lambda y: efl.equation_of_state(y, beta, mass, *found_params),
        a=0.0,
        b=0.5)

for mass in np.arange(0.01, 0.06, 0.01):
    plt.plot(psibarpsi[mass], label=f'm={mass}', color='black', linestyle='--')

if args.savefig:
    filename = f'fitLsinfL{L}.png'
    print(f"Writing {filename}")
    plt.savefig(filename)

else:
    plt.show()
