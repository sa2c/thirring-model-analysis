#!/usr/bin/env python3
import global_michele_script1 as gms
import os
import global_simon_script1 as gss1
import pandas as pd
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


def aggregate_runs(filenames):
    '''
    Aggregates dataframes removing thermalisation from each of them.
    '''
    meas_every = 5
    hits = 10

    thermalisation = 100 # trajectories
    
    return pd.concat([ (pd.read_csv(filename,sep='\s+')
                          .iloc[int(thermalisation/meas_every * hits) :,:])
                        for filename in filenames ])

def compute_meanerrs(df):
    from lib import blockingMeanErr
    meas_every = 5
    hits = 10

    blocksize = 100 # trajectories

    return dict([(col,blockingMeanErr(df[col],int(blocksize/meas_every*hits)))  
                  for col in df.columns])

def aggregate(fort100_info_df):
    '''
    '''
    thermalisation = 100
    keys = ['L','Ls','m','beta']
    res = []
    for keyvals, files in fort100_info_df.groupby(keys)['dirpath']:
        print(keyvals,files)
        meanerrs = compute_meanerrs(aggregate_runs(files))
        parvalues = dict(zip(keys,keyvals))
        parvalues.update(meanerrs)
        res.append(parvalues)

    return pd.DataFrame(res)



from lib import blockingMeanErr
