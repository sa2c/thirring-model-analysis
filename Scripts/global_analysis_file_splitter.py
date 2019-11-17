#!/usr/bin/env python3
import pandas as pd
from sys import argv
import os
import lib
from functools import reduce
import numpy as np
from collections import namedtuple


def filenameoutput(df, analysis_settings_filename):
    L = df.L.values[0]
    Ls = df.Ls.values[0]
    beta = df.beta.values[0]
    mass = df.mass.values[0]

    return f'L{L}Ls{Ls}.beta{beta:1.6f}.m{mass:1.6f}.{analysis_settings_filename}'


def savedf(df, directory):
    filename = os.path.join(directory, filenameoutput(df, argv[1]))
    print(f"Writing {filename}")
    print(len(df))
    df.to_csv(filename, sep='\t', index=False)


def get_parameter_groups(analysis_settings_df):
    return analysis_settings_df.loc[:, ['L', 'Ls', 'beta', 'mass'
                                        ]].drop_duplicates().itertuples()


def select_relevant_runs(analysis_settings_df: pd.DataFrame,
                         params: namedtuple ):
    conditions = [
        analysis_settings_df[name] == getattr(params, name)
        for name in params._fields if name in analysis_settings_df.columns
    ]

    return analysis_settings_df.loc[reduce(np.logical_and, conditions[1:],
                                           conditions[0]), :]


def separate_all_runs(analysis_settings_df):
    return [
        select_relevant_runs(analysis_settings_df, params)
        for params in get_parameter_groups(analysis_settings_df)
    ]


if __name__ == '__main__':
    directory = 'analysis_setting_split'
    data = lib.filelist_parser(argv[1]).reset_index()
    os.makedirs(directory, exist_ok=True)

    for df in separate_all_runs(data):
        savedf(df,directory)

    #data.groupby(
    #    by=['L', 'Ls', 'beta', 'mass']).apply(lambda df: savedf(df, directory))
