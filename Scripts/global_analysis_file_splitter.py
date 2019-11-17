#!/usr/bin/env python3
import pandas as pd
from sys import argv
import os
import lib

data = lib.filelist_parser(argv[1]).reset_index()


def filenameoutput(df, analysis_settings_filename):
    L = df.L.values[0]
    Ls = df.Ls.values[0]
    beta = df.beta.values[0]
    mass = df.mass.values[0]

    return f'L{L}Ls{Ls}.beta{beta:1.6f}.m{mass:1.6f}.{analysis_settings_filename}'


def savedf(df):
    filename = os.path.join(
        'analysis_setting_split', filenameoutput(df, argv[1]))
    print(f"Writing {filename}")
    print(len(df))
    df.to_csv(filename, sep='\t')


os.makedirs('analysis_setting_split',exist_ok=True)
data.groupby(by=['L', 'Ls', 'beta', 'mass']).apply(savedf)
