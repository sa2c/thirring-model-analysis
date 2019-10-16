#!/usr/bin/env python3

import lib 
from sys import argv


analysis_settings = lib.filelist_parser(argv[1])
df_dict = lib.read_all_files(analysis_settings)
df_dict_cut = lib.cut_and_paste(analysis_settings)

lib.scan_for_blocking(df_dict,df_dict_cut,'psibarpsi',analysis_settings)
