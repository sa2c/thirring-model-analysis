import os
import numpy as np

pbp_inf_dir = 'psibarpsi_extrapolated'
pbp_inf_filename_pretty = 'psibarpsi_extrapolated_pretty'


output_columns = [
    'last_pbp', 'last_pbp_e', 'constant', 'constant_e', 'alpha', 'alpha_e',
    'A', 'A_e', 'beta', 'L', 'mass', 'chisq', 'ndof'
]


def fit_output_filename_format(analysis_settings_filename, L, beta, mass):
    return os.path.join(pbp_inf_dir,
                        f'{analysis_settings_filename}_{L}_{beta}_{mass}')


def expexpression(A, alpha, constant, x):
    return A * np.exp(-alpha * x) + constant

