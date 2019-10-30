#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import lib
from tabulate import tabulate
import argparse as ap
import os
import glob
import extrapolation_library as el



def residuals(par, x, y, ye):
    A, alpha, constant = par
    ytheo = el.expexpression(A, alpha, constant, x)
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


def fit_exp(df,nboot):

    output_columns = el.output_columns

    if (len(df) < 4):
        return pd.DataFrame(data=None, columns=output_columns)

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
        [[last_pbp, last_pbp_e, constant, constant_e, alpha, alpha_e, A, A_e, beta, L , mass]])

    res = pd.DataFrame(data=data, columns=output_columns)

    return res


def aggregate_psibarpsi_dataframes(L, mass, beta, analysis_settings_filename):
    """
    See single_analysis_file_splitter, the $filename variable.
    Collects all relevant analysis setting files, grouped by L, beta and mass.
    """
    glob_expression = os.path.join(
        lib.pbpdir, lib.pbp_values_and_error_filename +
        f"L{L}Ls??.beta{float(beta):1.6f}.m{float(mass):1.6f}.{analysis_settings_filename}")
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
parser.add_argument('beta', type=str, help='The chosen value of beta')
parser.add_argument('L', type=str, help='The chosen value of L')
parser.add_argument('nboot', type=int, help='Number of boostrap resampling')

args = parser.parse_args()

values_and_errors = aggregate_psibarpsi_dataframes(
    L=args.L,
    mass=args.mass,
    beta=args.beta,
    analysis_settings_filename=args.analysis_settings_filename)

print("All values considered:")
print(values_and_errors)

extrapolation = fit_exp(values_and_errors,args.nboot)
os.makedirs(lib.pbp_inf_dir, exist_ok=True)

output_filename = el.fit_output_filename_format( args.analysis_settings_filename,args.L,args.beta,args.mass)

assert len(extrapolation) is not 0 or len(values_and_errors) < 4

if len(extrapolation) is 0:
    exit()

print(f"Writing {output_filename}")
extrapolation.to_csv(path_or_buf=output_filename, sep='\t')

print("Extrapolation:")
print(extrapolation)
