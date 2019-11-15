#!/usr/bin/env 
'''
   It turned out that I attributed to L=12 some runs that actually were for L=16
   (and it was visible in the "out" files). 
   This was corrected in single_dir_simon.sh, but fort.200.analysis.set was
   pointing at directories that did not exist.
   This script summarises the steps done for fixing that.
'''
import lib
import pandas as pd
import os
settings = lib.filelist_parser('fort.200.analysis.set')
wrong_filenames = [ filename for filename in settings.filename if not os.path.exists(filename) ] 

settings = settings.reset_index().set_index('filename')
settings.loc[wrong_filenames, 'L'] = 16
settings = settings.reset_index()
for k,v in zip(wrong_filenames,[ filename.replace('/12/','/16/') for filename in wrong_filenames ]):
    settings.loc[settings.filename == k,'filename'] = v

settings.to_csv('fort.200.analysis.set.corrected',sep='\t')
