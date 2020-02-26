#!/usr/bin/env python3


def parse_midout(midout_file_name):
    '''
    This function parses the midout file, in the format:
    0.04    0.24  1.0  0.01   3    25     200  40000
    dt       beta am3  am   imass iterl  iter2  wallclock
    '''
    with open(midout_file_name, 'r') as f:
        lines = f.readlines()

    vs = lines[0].split()  # values
    ks = lines[1].split()  # keys

    # renaming am -> m
    ks[ks.index('am')]='m'

    return dict(zip(ks, vs))


def parse_output(output_filename):
    '''
    Parses output and returns only L and Ls.
    '''
    import re
    res = dict()
    with open(output_filename, 'r') as f:
        t = f.read()

    # L
    L_re = r"ksize\s*=\s*([0-9]{1,3})"
    all_finds = set(re.findall(L_re, t))
    assert len(
        all_finds) == 1, f"L is ambiguously defined in {output_filename}"
    res['L'] = int(all_finds.pop())

    # Ls
    Ls_re = r"kthird\s*=\s*([0-9]{1,3})"
    all_finds = set(re.findall(Ls_re, t))
    assert len(
        all_finds) == 1, f"Ls is ambiguously defined in {output_filename}"
    res['Ls'] = int(all_finds.pop())

    return res

def get_run_parameter_from_dir_content(dirname):
    import os
    midout_file_name = os.path.join(dirname,'midout')
    output_file_name = os.path.join(dirname,'output')

    try:
        res = parse_midout(midout_file_name)
        res.update(parse_output(output_file_name))
    except :
        res = None
    return res

