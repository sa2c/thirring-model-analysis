#!/usr/bin/env python3
import lib
import pandas as pd
import numpy as np
import argparse as ap
from tabulate import tabulate
import os 
parser = ap.ArgumentParser(
    description="An utility compute and store the condensate data for all runs."
)

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help=
    "The name of the file containing the thermalization and the block sizes")

args = parser.parse_args()

# Parsing analysis settings, getting dataframe dictionary
analysis_settings = lib.filelist_parser(args.analysis_settings_filename)
df_dict = lib.cut_and_paste(analysis_settings)

# computing the values of pbp and pbp_err FOR ALL known data point in
# analysis_settings
values_and_errors = lib.get_values_and_errors(df_dict, 'psibarpsi',
                                              analysis_settings)

basename = os.path.basename(args.analysis_settings_filename)

print(f"Creating lib.pbpdir, {lib.pbpdir}") 
os.makedirs(lib.pbpdir,exist_ok=True)

values_and_error_filename = os.path.join(lib.pbpdir,lib.pbp_values_and_error_filename+basename)
print(f"Writing {values_and_error_filename}")
data_to_write = values_and_errors.set_index(['L', 'Ls', 'beta', 'mass'])
data_to_write.to_csv(values_and_error_filename, sep='\t')
