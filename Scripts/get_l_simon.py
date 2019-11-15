#!/usr/bin/env python3
'''
   This script gets the value of L by looking at the 'out*' files
   (simon's original style, where there are more than one out file)
'''

import os
import glob
import re
from sys import argv

directory = argv[1]
filenames = glob.glob(os.path.join(directory,'out*'))
Ls = [] 
for filename in filenames: 
    with open(filename,'r') as f:
        found = re.search('ksize\s*=\s*([0-9]+)\s*ksizet\s*=\s*([0-9]+)',f.read())
        if found is not None:
            ksize, ksizet = found.groups()
            assert int(ksize) == int(ksizet)
            Ls.append(ksize)
assert len(set(Ls)) == 1 

print(Ls[0])
    
