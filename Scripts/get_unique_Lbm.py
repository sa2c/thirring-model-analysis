#!/usr/bin/env python3
import lib

data = lib.filelist_parser('fort.200.analysis.set')
    
for tup in data.reset_index().loc[:,['L','beta','mass']].drop_duplicates().itertuples():
    print(tup.L,tup.beta,tup.mass)
    
