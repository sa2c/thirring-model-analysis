#!/usr/bin/env python3
# This file is used to compare old data, namely the cond* files from 
# ../Data/TARS/Eos.tar.from.simon.tar.gz, with the new cond* files.
# THIS IS NOT PART OF ANY WORKFLOW SO IT IS POORLY MAINTAINED.

import pandas as pd
import glob
import os
import numpy as np
from matplotlib import pyplot as plt

filelist = glob.glob('cond*')

def get_other_filename(filename,other_stem='../../Playground/eos_fit/'):
    fs = [filename.split('_')[i] for i in [0,1,3,2]]
    fs[3] = 'L'+fs[3]
    fs[2] = fs[2].replace('08','8')
    return os.path.join(other_stem,'_'.join(fs))

for filename in filelist:
    df_old = pd.read_table(filename,sep='\s+')
    df_old.columns = ['beta','pbp','pbp_e']
    filename_new = get_other_filename(filename)
    if os.path.exists(filename_new):
        df_new = pd.read_table(get_other_filename(filename),sep='\s+')
        df_new.columns = df_old.columns
        df_new = df_new.set_index('beta')
        df_old = df_old.set_index('beta')
        comparison = df_new.join(df_old,on='beta',lsuffix='_new',rsuffix='_old',how='inner')

        comparison['delta'] = np.abs(comparison.pbp_new - comparison.pbp_old)/(
                np.hypot(comparison.pbp_e_new,comparison.pbp_e_old))

        comparison = comparison.sort_index()
        
        comparison.to_csv('df'+filename,sep='\t',float_format='%1.5e')
        plt.figure()
        plt.errorbar(comparison.index-0.002,comparison.pbp_old, yerr = comparison.pbp_e_old,label='old')
        plt.errorbar(comparison.index+0.002,comparison.pbp_new, yerr = comparison.pbp_e_new,label='new')
        plt.legend()
        plt.title(f'check {filename}')
        plt.savefig(f'fig_{filename}.png')
        plt.close()
        comparison.loc[comparison.delta>1,:].to_csv('check_df'+filename,sep='\t',float_format='%1.5e')

        
        
        
        
 
