#!/usr/bin/env python3
import numpy as np
import pandas as pd
from scipy.optimize import leastsq, brentq
from sys import argv

input_filename = argv[1]
nboot = 100

print(f"Reading {input_filename}")
cond_filenames = pd.read_csv(input_filename, sep='\t', comment='#')


def get_dataframe_from_txt(filename, Ls):
    data = pd.DataFrame(
        data=np.loadtxt(filename), columns=['beta', 'pbp', 'pbp_e'])
    data['Ls'] = Ls
    return data


data = pd.concat([
    get_dataframe_from_txt(filename, Ls)
    for filename, Ls in zip(cond_filenames.Filename, cond_filenames.Ls)
])


def fit_exp(df):

    if (len(df) < 3):
        return None

    df = df.sort_values(by='Ls')
    x = df['Ls']
    y = df['pbp']
    ye = df['pbp_e']

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
        data=data, columns=['last_pbp', 'last_pbp_e', 'pbp_inf', 'pbp_inf_e'])


data = data.set_index(keys='beta')
extrapolation = data.groupby(level=[0]).apply(fit_exp)

output_filename =  input_filename + '_extrapolation'
print(f"Writing {output_filename}")
extrapolation.to_csv(path_or_buf= output_filename , sep = '\t')
