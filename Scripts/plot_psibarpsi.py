#!/usr/bin/env python3

import lib 
from sys import argv
import pandas as pd
from matplotlib import pyplot as plt


analysis_settings = lib.filelist_parser(argv[1])
df_dict = lib.cut_and_paste(analysis_settings)

values_and_errors = lib.get_values_and_errors(df_dict,'psibarpsi',analysis_settings)


plt.title("Ls=32")
lib.plot_observable('psibarpsi',32,values_and_errors)

plt.show()


