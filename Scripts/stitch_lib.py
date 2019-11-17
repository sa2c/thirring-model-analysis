#!/usr/bin/env python3
import os
import logging

def join_consecutive_lines(text,nfields):
    values = text.split()
    return '\n'.join([ ' '.join(values[i*4:i*4+4]) for i in range(len(values)//4) ])
    
def paste_all(dirpath,filename_info,filenames_found_per_type_fun):
    for filetype in filename_info.index:
        print(f'Reading $(shell find {dirpath} -regex {filename_info.regexp[filetype]} ')

    filenames_found_per_type = filenames_found_per_type_fun(dirpath)

    res =  dict([(filetype, ''.join(
        [ ' '.join(filename_info.column_names[filetype])+'\n' if filename_info.column_names[filetype] is not None else '' ] + 
        [
        open(filename).read() for filename in sorted(filelist)
    ]).replace('\n\n','\n')) for (filetype, filelist) in filenames_found_per_type.items()])

    # fixing fort.100 where lines are split
    res['conds'] = join_consecutive_lines(res['conds'], len(filename_info.column_names['conds']))

    for k,v in res.items():
        if filename_info.column_names[k] is not None:
            for line in v.split('\n'):
                assert len(line) is 0 or len(line.split()) == len(filename_info.column_names[k]) , f"{dirpath} : {k}: '{line}'"

    return res

def get_newdir_name(prefix, L, copy, Ls, beta, m):
    return os.path.normpath(
        os.path.join(prefix if len(prefix) is not 0 else '.',
                     f'{L:02d}',
                     copy if len(copy) is not 0 else '.',
                     f'Ls{Ls:02d}.beta{beta}.m{m}'))


def process_directory(directory,prefix,find_L,match_directory_name,
            get_newdir_name,paste_all,filename_info):
    '''
    Collects all files in directory, joins them and writes into
    a new directory.
    Prefix is prepended to the new directory name.
    '''
 
    L =  int(find_L(directory))
    info = match_directory_name(directory)

    newdir = get_newdir_name(prefix, L, info['copy'], info['Ls'], info['beta'], info['m'])
    
    os.makedirs(newdir,exist_ok = True)

    all_file_content = paste_all(directory)

    for k,v in all_file_content.items():
        newfilename = os.path.join(newdir,filename_info.fortran_name[k])
        print(f"Writing {newfilename}")
        with open(newfilename,'w') as f:
            f.write(v)
 
