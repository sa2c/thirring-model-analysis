import os
import numpy as np

pbp_inf_dir = 'psibarpsi_extrapolated'
pbp_inf_filename_pretty = 'psibarpsi_extrapolated_pretty'

output_columns = [
    'last_pbp', 'last_pbp_e', 'constant', 'constant_e', 'alpha', 'alpha_e',
    'A', 'A_e', 'beta', 'L', 'mass', 'chisq', 'ndof'
]


def fit_output_filename_format(analysis_settings_filename, L, beta, mass):
    filename = f'{analysis_settings_filename}_{L}_'
   
    try:
        beta = float(beta)
    except:
        pass

    try:
        mass = float(mass)
    except:
        pass

    if type(beta) == float:
        filename += f'{beta:1.6f}_'
    elif type(beta) == str :
        filename += f'{beta}_'

    if type(mass) == float:
        filename += f'{float(mass):1.6f}'
    elif type(mass) == str :
        filename += f'{mass}'

    return os.path.join( pbp_inf_dir, filename )


def expexpression(A, alpha, constant, x):
    return A * np.exp(-alpha * x) + constant
