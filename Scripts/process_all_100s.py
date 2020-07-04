#!/usr/bin/env python3
'''
A script to compute all the values of delta once the fort.100 files
have been moved and stitched into the Analysis directory, and a header
has been strapped onto them.
Notice that file 
./simon/old/12/Ls08.beta0.3.m0.03/fort.100
may need to be corrected, as it has some garbage in it.
'''
import global_michele_script1 as gms
import os
import global_simon_script1 as gss1
import pandas as pd
import numpy as np 
import re

def get_l(dirpath):
    '''
    returns the value of L from the path in Analysis.
    '''
    if re.search('/12/',dirpath) or re.search('L12',dirpath):
        return 12
    if re.search('/16/',dirpath) or re.search('L16',dirpath):
        return 16

def get_files_and_parameters():
    '''
    Returns a dataframe where one column ('dirpath') is the path to the file,
    and the others are the parameters of the run.

    This function is supposed to be called in the Analysis directory
    where other scripts have already operated.
    '''
    fort100_list = []
    for dirpath,dirnames,filenames in os.walk('.'):
        for filename in filenames:
            if filename == 'fort.100':
                fort100_list.append( 
                        dict(dirpath=os.path.join(dirpath,'fort.100'),
                            **(gss1.match_directory_name_simon(dirpath) 
                                or 
                                gms.match_directory_name_michele(dirpath,None)
                                ),
                            L = get_l(dirpath)
                            )
                        )
    fort100_info_df = pd.DataFrame(fort100_list)
    return fort100_info_df


def fix_glued_columns(text):
    '''
    In some cases two columns are glued because there is a - sign between 
    the two, and the width of the field is not large enough.
    '''
    return re.subn("([0-9])-",lambda match : match.groups()[0] + ' -',text)[0]


def aggregate_runs(filenames):
    '''
    Aggregates dataframes removing thermalisation from each of them.
    '''
    from io import StringIO
    meas_every = 5
    hits = 10

    thermalisation = 100 # trajectories
    
    return pd.concat([ (pd.read_csv(
                            StringIO( print(f"Reading {filename}") or
                                fix_glued_columns(
                                    open(filename,'r').read()
                                    )
                                ),
                        sep='\s+',
                        engine = 'python')
                          .iloc[int(thermalisation/meas_every * hits) :,:])
                        for filename in filenames ])

def compute_meanerrs(df):
    from lib import blockingMeanErr
    meas_every = 5
    hits = 10

    blocksize = 100 # trajectories

    return dict([(k,v)
                  for col in df.columns
                  for k,v in zip(
                           (col,col+'Err'),
                           blockingMeanErr(df[col],int(blocksize/meas_every*hits))
                           )
                  ])

def aggregate(fort100_info_df):
    '''
    Compute the mean and error of all the columns in the dataframe
    '''
    thermalisation = 100
    keys = ['L','Ls','m','beta']
    res = []
    for keyvals, files in fort100_info_df.groupby(keys)['dirpath']:
        meanerrs = compute_meanerrs(aggregate_runs(files))
        parvalues = dict(zip(keys,keyvals))
        parvalues.update(meanerrs)
        res.append(parvalues)

    return pd.DataFrame(res).set_index(keys)


if __name__ == '__main__':
    fort100_info_df = get_files_and_parameters()
    # fort.100 mean errs
    f100me = aggregate(fort100_info_df) 

    delta = 0.5*(f100me.aimag_psibarpsi2 - f100me.aimag_psibarpsi1)
    deltaErr = 0.5*np.hypot(f100me.aimag_psibarpsi2Err,f100me.aimag_psibarpsi1Err)

    out_filename = "delta.tsv"
    print(f"Writing {out_filename}")
    pd.DataFrame(data = {'delta':delta,'err':deltaErr},index = delta.index).reset_index().to_csv(out_filename,sep = '\t',index = False)

    




