#!/usr/bin/env python3
import os
import re
import stitch_lib as sl
import pandas as pd
import logging
import fort_colnames as fc

michele_pattern = re.compile(
    r'Ls(?P<Ls>[0-9]+).*beta(?P<beta>0.[0-9]+).*m(?P<m>0.[0-9]+)$'
)  # this is just for the stem

michele_filename_info = [('conds',  r'fort.100', fc.fort100cols),
                       ('condensate', r'fort.200', fc.fort200cols),
                       ('bose', r'fort.11', fc.fort11cols),
                       ('out', r'output',None)]
michele_filename_info = pd.DataFrame(
    data=michele_filename_info, columns=['filetype',
                                       'fortran_name', 'column_names']).set_index('filetype')

michele_filename_info['regexp'] = michele_filename_info.fortran_name
michele_filename_info['compiled_regexp'] = pd.Series(
    [re.compile(v) for v in michele_filename_info.regexp],
    index=michele_filename_info.index)

def match_directory_name_michele(dirpath,copy):
    match = re.search(michele_pattern, dirpath)
    try:
        resdict = {
            'beta': float(match.group('beta')),
            'Ls': int(match.group('Ls')),
            'm': float(match.group('m')),
            'copy': copy 
        }
        return resdict
    except:
        return None

michele_additional_pattern = r'save[0-9]+/[0-9]{10}'
michele_additional_pattern = re.compile(michele_additional_pattern)

def filenames_found_per_type_fun_michele(dirpath):

    res =  dict([(filetype, [
        os.path.join(directory, fortran_name)
        for (directory, _, filenames) in os.walk(dirpath)
        if re.search(michele_additional_pattern,directory) is not None and fortran_name in filenames
    ]) for (filetype,fortran_name) in zip(
        michele_filename_info.index,
        michele_filename_info.fortran_name)])

    for k,v in res.items():
       print(f"Found {len(v)} {k} files")


    return res

def michele_paste_all(dirpath):
    logging.info('michele_paste_all')
    return sl.paste_all(dirpath,michele_filename_info,filenames_found_per_type_fun_michele)
 
def process_michele_directory(directory,prefix,Lfun,copy):
    sl.process_directory(directory,prefix,Lfun,
            lambda x : match_directory_name_michele(x, copy),
            sl.get_newdir_name,michele_paste_all,michele_filename_info)

if __name__ == '__main__':

    # TODO: Prefixes
    for directory,_,_ in os.walk('../Data/thirring_runs1/all_dirs/'):
        if match_directory_name_michele(directory,'1'):
            process_michele_directory(directory,'michele',lambda x: 12,'1')

    for directory,_,_ in os.walk('../Data/thirring_runs2/all_dirs/'):
        if match_directory_name_michele(directory,'2'):
            process_michele_directory(directory,'michele',lambda x: 12,'2')

    for directory,_,_ in os.walk('../Data/16/all_dirs/'):
        if match_directory_name_michele(directory,''):
            process_michele_directory(directory,'michele',lambda x: 16,'')



