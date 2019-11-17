#!/usr/bin/env python3
import re

def isLcandidate(path,L):
    patterns = [f'L{L}',f'/{L}/']
    return any([re.search(pattern,path) is not None for pattern in patterns])
    
import os
dirs  = set([ dirpath for (dirpath,_,filenames) in os.walk('.') if 'fort.200' in filenames ])

cand12 = set([ directory for directory in dirs if isLcandidate(directory,12)])
cand16 = set([ directory for directory in dirs if isLcandidate(directory,16)])

assert cand12.intersection(cand16) == set()
assert dirs.difference(cand12).difference(cand16) == set()
assert len(dirs) == len(cand12) + len(cand16)

import pandas as pd
df = pd.DataFrame(data=[os.path.join(dirpath,'fort.200') for dirpath in dirs] ,columns=['filename'])

def getL(dirname):
    return 12 if dirname in cand12 and dirname not in cand16 else 16 if dirname in cand16 and dirname not in cand12 else None

df['L'] = [getL(os.path.dirname(filepath)) for filepath in df.filename ] 
df['thermalization'] = 100
df['blocksize'] = 100
df['measevery'] = 5

outfile = 'fort.200.analysis.set.synthetic'
print(f"Writing {outfile}")
df.sort_values(by='filename').to_csv(outfile,sep='\t',index = False)

