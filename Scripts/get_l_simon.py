#!/usr/bin/env python3
'''
   This script gets the value of L by looking at the 'out*' files
   (simon's original style, where there are more than one out file)
'''
import os
import glob
import re

def find_L(directory):
    filenames = glob.glob(os.path.join(directory,'out*'))
    Lvalues = [] 
    for filename in filenames: 
        with open(filename,'r') as f:
            found = re.search('ksize\s*=\s*([0-9]+)\s*ksizet\s*=\s*([0-9]+)',f.read())
            if found is not None:
                ksize, ksizet = found.groups()
                assert int(ksize) == int(ksizet)
                Lvalues.append(ksize)
    assert len(set(Lvalues)) == 1 , f'Problems in {directory}'
    return Lvalues[0]

if __name__ == "__main__":
    from sys import argv
    print(find_L(argv[1]))
    
