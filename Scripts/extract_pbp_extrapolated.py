#!/usr/bin/env python3
import extrapolation_library as el
import lib
import os
import argparse as ap
import pandas as pd

parser = ap.ArgumentParser(
    description="An utility compute and store the condensate data for all runs."
)

parser.add_argument(
    'analysis_settings_filename',
    type=str,
    help=
    "The name of the original file containing the thermalization and the block sizes")

parser.add_argument(
    'L',
    type=int,
    help=
    "The chosen value of L")

parser.add_argument(
    'beta',
    type=float,
    help=
    "The chosen value of beta")

parser.add_argument(
    'mass',
    type=float,
    help=
    "The chosen value of the mass")


args = parser.parse_args()

file_to_process = el.fit_output_filename_format(args.analysis_settings_filename,
        args.L,args.beta,args.mass)

print("Reading {file_to_process}")
extrapolation_data = pd.read_table(file_to_process,sep='\s+')

pbp_inf_data = extrapolation_data.loc[:,['constant','constant_e' ]]
pbp_inf_data.columns = ['psibarpsi','psibarpsiErr']
pbp_inf_data['L'] = [args.L]
pbp_inf_data['beta'] = [args.beta]
pbp_inf_data['mass'] = [args.mass]

pbp_inf_data = pbp_inf_data.set_index(['L', 'beta', 'mass'])

pbp_inf_data_filename = os.path.join(lib.pbpdir,lib.pbp_values_and_error_filename + 
        f"L{args.L}LsINF.beta{args.beta}m{args.mass}.{args.analysis_settings_filename}")

print(f"Writing {pbp_inf_data_filename}")
pbp_inf_data.to_csv(pbp_inf_data_filename, sep='\t')



