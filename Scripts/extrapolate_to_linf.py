#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.optimize import leastsq, brentq
from sys import argv
import lib
from tabulate import tabulate


def fit_exp(df):

    if (len(df) < 3):
        return None

    df = df.sort_values(by='Ls')
    x = df['Ls']
    y = df['psibarpsi']
    ye = df['psibarpsiErr']

    def residuals(par, x, y, ye):
        alpha, constant = par
        ytheo = np.exp(-alpha * x) + constant
        return (y - ytheo) / ye

    yl = list(y)
    xl = list(x)

    constant = yl[-1]
    last_pbp = constant
    last_pbp_e = list(ye)[-1]
    alpha = -np.log((yl[-3] - yl[-1]) / (yl[-2] - yl[-1])) / (xl[-3] - xl[-2])

    if np.isnan(alpha):
        alpha = 0.0

    res = leastsq(
        func=residuals,
        x0=np.array([alpha, constant]),
        args=(x, y, ye),
        full_output=1)

    c = res[0][1]
    alpha = res[0][0]

    cs = list()

    nboot = 10
    print('Boostrapping...')
    for _ in range(nboot):
        yresampled = np.random.normal(y, ye)
        res = leastsq(
            func=residuals,
            x0=np.array([alpha, constant]),
            args=(x, yresampled, ye),
            full_output=1)

        cs.append(res[0][1])

    c_e = np.std(np.array(cs))
    data = np.array([[last_pbp, last_pbp_e, c, c_e]])

    return pd.DataFrame(
        data=data, columns=['last_pbp', 'last_pbp_e', 'psibarpsi_inf', 'psibarpsi_infErr'])


print(f'Reading {lib.pbp_values_and_error_filename}')
values_and_errors = pd.read_csv(lib.pbp_values_and_error_filename, sep='\t')

extrapolation = values_and_errors.groupby(
    by=['L', 'beta', 'mass']).apply(fit_exp)




def plot_fit_exp(df_multi):
    from matplotlib import pyplot as plt
    plt.figure()

    L = df_multi.L.drop_duplicates().values[0]
    m = df_multi.mass.drop_duplicates().values[0]

    first_called = False # workaround for calling apply with a side effectful f

    def plot_fit_exp_single(df):
        # workaround for calling apply with a side effectful f
        nonlocal first_called
        if not first_called:
            first_called = True
            return None

        beta = df.beta.drop_duplicates().values[0]
        if (len(df) < 3):
            return None
    
        df = df.sort_values(by='Ls')
        x = df['Ls']
        y = df['psibarpsi']
        ye = df['psibarpsiErr']
    
        def residuals(par, x, y, ye):
            alpha, constant = par
            ytheo = np.exp(-alpha * x) + constant
            return (y - ytheo) / ye
    
        yl = list(y)
        xl = list(x)
    
        constant = yl[-1]
        last_pbp = constant
        last_pbp_e = list(ye)[-1]
        alpha = -np.log((yl[-3] - yl[-1]) / (yl[-2] - yl[-1])) / (xl[-3] - xl[-2])
    
        if np.isnan(alpha):
            alpha = 0.0
    
        res = leastsq(
            func=residuals,
            x0=np.array([alpha, constant]),
            args=(x, y, ye),
            full_output=1)
        c = res[0][1]
        alpha = res[0][0]

        plt.errorbar(x,y,yerr=ye)
        xplot = np.arange(min(x),max(x),(max(x)-min(x))/100)
        plt.plot(xplot,np.exp(-alpha*xplot)+c, label = f'{beta}')

    df_multi.groupby(by=['beta']).apply(plot_fit_exp_single)
    plt.legend()

    output_filename = f'pbpextrL{L}_m{m}.png'
    print(f'Writing {output_filename}')
    plt.savefig(output_filename)



values_and_errors.groupby(by=['L','mass']).apply(plot_fit_exp)

output_filename = lib.pbp_inf_filename
print(f"Writing {output_filename}")
extrapolation.to_csv(path_or_buf=output_filename, sep='\t')

output_filename_pretty = lib.pbp_inf_filename_pretty
print(f"Writing {output_filename_pretty}")
with open(output_filename_pretty, 'w') as f:
    f.write(
        tabulate(
            extrapolation.reset_index().drop(labels='level_3',axis='columns'),
            headers='keys',
            showindex=False,
            tablefmt='psql'))
