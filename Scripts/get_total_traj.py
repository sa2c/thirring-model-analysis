#!/usr/bin/env python3
import lib
from sys import argv
from tabulate import tabulate

print(f'Reading {argv[1]}')
filelist = lib.filelist_parser(argv[1])

output_filename = 'nmeas_' + argv[1]
print(f'Writing {output_filename}')
out = lib.get_n_meas(filelist)
with open(output_filename, 'w') as f:
    f.write(
        tabulate(
            out.sort_values(by='ntraj'),
            headers='keys',
            showindex=False,
            tablefmt='psql'))

output_filename = 'sortable' + output_filename
print(f'Writing {output_filename}')
out.sort_values(by='ntraj').to_csv(
    output_filename, sep='\t', float_format='%1.3f')
