
import lib
import os

output_columns = [
        'last_pbp', 'last_pbp_e', 'constant', 'constant_e', 'alpha', 'alpha_e',
        'A', 'A_e','beta','L','mass'
    ]

def fit_output_filename_format(analysis_settings_filename,L,beta,mass):
    return os.path.join(
    lib.pbp_inf_dir,
    f'{analysis_settings_filename}_{L}_{beta}_{mass}')
