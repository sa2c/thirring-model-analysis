#!/usr/bin/env python3
'''
    This script finds the directories with data.
'''
import re
import os
import glob
import logging
import pandas as pd
import get_l_simon
import stitch_lib as sl


### 
simon_pattern = re.compile(
    r'b_?(?P<beta>[01]\.[0-9]+)(?P<copy>[a-zA-Z]*).*Ls_?(?P<Ls>[0-9]+).*m_?(?P<m>0\.[0-9]+)'
)

fort100cols =['real_psibarpsi1','aimag_psibarpsi1','real_psibarpsi2','aimag_psibarpsi2']
fort200cols =["psibarpsi","susclsing"]
fort11cols =['isweep','gaction','paction']


simon_filename_info = [('conds', r'conds_([0-9]+)', r'fort.100', fort100cols),
                       ('condensate', r'condensate_([0-9]+)', r'fort.200', fort200cols),
                       ('bose', r'bose_([0-9]+)', r'fort.11', fort11cols),
                       ('out', r'out_([0-9]+)', r'output',None)]
simon_filename_info = pd.DataFrame(
    data=simon_filename_info, columns=['filetype', 'regexp',
                                       'fortran_name', 'column_names']).set_index('filetype')

simon_filename_info['compiled_regexp'] = pd.Series(
    [re.compile(v) for v in simon_filename_info.regexp],
    index=simon_filename_info.index)

def match_directory_name_simon(dirpath):
    match = re.search(simon_pattern, dirpath)
    try:
        resdict = {
            'beta': float(match.group('beta')),
            'Ls': int(match.group('Ls')),
            'm': float(match.group('m')),
            'copy': match.group('copy')
        }
        return resdict
    except:
        return None


def filenames_found_per_type_fun_simon(dirpath):
    filelist = os.listdir(dirpath)

    return dict([(k, [
        os.path.join(dirpath,filename) for filename in filelist if re.match(v, filename) is not None
    ]) for (k, v) in zip(simon_filename_info.index,
                         simon_filename_info.compiled_regexp)])


def contains_files_simon_old(dirpath):
    filenames_found_per_type = filenames_found_per_type_fun_simon(dirpath)

    if len(set([len(v)
                for (k, v) in filenames_found_per_type.items()])) is not 1:
        logging.warning(
            f"In dir {dirpath} not all file species are equally represented.")

    return len(filenames_found_per_type['condensate']) > 0


def simon_suspect(dirpath):
    return (match_directory_name_simon(dirpath) is None
            and contains_files_simon_old(dirpath)) or (
                match_directory_name_simon(dirpath) is not None
                and not contains_files_simon_old(dirpath))

def simon_paste_all(dirpath):
    return sl.paste_all(dirpath,simon_filename_info,filenames_found_per_type_fun_simon)

def simon_get_newdir_name(prefix, L, copy, Ls, beta, m):
    return os.path.join('simon',
            sl.get_newdir_name(prefix, L, copy, Ls, beta, m))
 
def process_simon_directory(directory,prefix):
    sl.process_directory(directory,prefix,get_l_simon.find_L,match_directory_name_simon,
            simon_get_newdir_name,simon_paste_all,simon_filename_info)

   
if __name__ == '__main__':

    for directory,_,_ in os.walk('../Data/simon/'):
        if match_directory_name_simon(directory) and contains_files_simon_old(directory):
            process_simon_directory(directory,'')

    for directory,_,_ in os.walk('../Data/simon_oldstuff/'):
        if match_directory_name_simon(directory) and contains_files_simon_old(directory):
            process_simon_directory(directory,'old')


