#!/usr/bin/env python3
'''
This script finds the directories with data for Simon runs,
in the new format where there is only one file.
'''
import global_simon_script1 as gss1
from get_l_simon import find_L
import stitch_lib as sl
import shutil
import os
import fort_colnames as fc

if __name__ == '__main__':
    prefix = 'simon_dirac_newcode'
    for directory, _, _ in os.walk('../Data/simon/dirac_newcode'):
        if gss1.match_directory_name_simon(directory):
            L = int(find_L(directory))
            info = gss1.match_directory_name_simon(directory)
            newdir = sl.get_newdir_name(prefix, L, info['copy'], info['Ls'],
                                        info['beta'], info['m'])

            os.makedirs(newdir, exist_ok=True)
            for filename in gss1.simon_filename_info.fortran_name:
                origin_name = os.path.join(directory, filename)
                destination_name = os.path.join(newdir, filename)
                if os.path.exists(origin_name):
                    with open(origin_name,'r') as origin:
                        print(f"Reading {origin_name}")
                        t = origin.read()
                    with open(destination_name,'w') as destination:
                        print(f"Writing {destination_name}")
                        header = ' '.join(fc.cols[filename]) if filename in fc.cols else ''
                        destination.write(header)
                        destination.write('\n')
                        destination.write(t)


