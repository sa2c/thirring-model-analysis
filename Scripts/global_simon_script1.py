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


def filenames_found_per_type_fun(dirpath):
    filelist = os.listdir(dirpath)

    return dict([(k, [
        filename for filename in filelist if re.match(v, filename) is not None
    ]) for (k, v) in zip(simon_filename_info.index,
                         simon_filename_info.compiled_regexp)])


def contains_files_simon_old(dirpath):
    filenames_found_per_type = filenames_found_per_type_fun(dirpath)

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


def join_consecutive_lines(text,nfields):
    values = text.split()
    return '\n'.join([ ' '.join(values[i*4:i*4+4]) for i in range(len(values)//4) ])
    

def simon_paste_all(dirpath):
    for filetype in simon_filename_info.index:
        print(f'Reading $(shell find {dirpath} -regex {simon_filename_info.regexp[filetype]} ')

    filenames_found_per_type = filenames_found_per_type_fun(dirpath)

    res =  dict([(filetype, ''.join(
        [ ' '.join(simon_filename_info.column_names[filetype])+'\n' if simon_filename_info.column_names[filetype] is not None else '' ] + 
        [
        open(os.path.join(dirpath, filename)).read() for filename in sorted(filelist)
    ]).replace('\n\n','\n')) for (filetype, filelist) in filenames_found_per_type.items()])

    # fixing fort.100 where lines are split
    res['conds'] = join_consecutive_lines(res['conds'], len(simon_filename_info.column_names['conds']))

    for k,v in res.items():
        if simon_filename_info.column_names[k] is not None:
            for line in v.split('\n'):
                assert len(line) is 0 or len(line.split()) == len(simon_filename_info.column_names[k]) , f"{dirpath} : {k}: '{line}'"

    return res

def get_newdir_name(prefix, L, copy, Ls, beta, m):
    return os.path.normpath(
        os.path.join('simon', 
                     prefix if len(prefix) is not 0 else '.',
                     f'{L:02d}',
                     copy if len(copy) is not 0 else '.',
                     f'Ls{Ls:02d}.beta{beta}.m{m}'))


  
def process_simon_directory(directory,prefix):
    '''
    Collects all files in directory, joins them and writes into
    a new directory.
    Prefix is prepended to the new directory name.
    '''

    L =  int(get_l_simon.find_L(directory))
    info = match_directory_name_simon(directory)

    newdir = get_newdir_name(prefix, L, info['copy'], info['Ls'], info['beta'], info['m'])
    
    os.makedirs( newdir,exist_ok = True)

    all_file_content = simon_paste_all(directory)

    for k,v in all_file_content.items():
        newfilename = os.path.join(newdir,simon_filename_info.fortran_name[k])
        print(f"Writing {newfilename}")
        with open(newfilename,'w') as f:
            f.write(v)
    
if __name__ == '__main__':

    for directory,_,_ in os.walk('../Data/simon/'):
        if match_directory_name_simon(directory) and contains_files_simon_old(directory):
            process_simon_directory(directory,'')

    for directory,_,_ in os.walk('../Data/simon_oldstuff/'):
        if match_directory_name_simon(directory) and contains_files_simon_old(directory):
            process_simon_directory(directory,'old')


