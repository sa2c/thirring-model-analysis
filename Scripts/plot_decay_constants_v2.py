#!/usr/bin/env python3
import pandas as pd
from glob import glob
import matplotlib
matplotlib.use("AGG")
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)   
from matplotlib import pyplot as plt
from itertools import cycle
import extrapolation_library as el
import os


filenames = glob(os.path.join(el.pbp_inf_dir,'fort.200.analysis.set*'))

for filename in filenames:
    print(f"Reading {filename}")

data = pd.concat([ pd.read_csv(filename, sep='\s+') for filename in filenames ])

print("Collated data")
def process(data,L):
    plt.figure() 
    plt.xlabel(r'$am$')
    plt.ylabel(r'$\\\Delta$')
    data = data.loc[(data.L == L )& (data.beta < 0.45),:]
    print(f"For L={L}, data points: {len(data)}")
    nbetas = len(data.beta.drop_duplicates())
    shift = 0.01 / 3 /  nbetas

    markers = cycle(['*','o','^','D','v',])
    colors = cycle(['blue','red','black'])
    facecolorfuns = cycle([lambda x:x , lambda x : None])

    for i,(beta,df) in enumerate(data.groupby('beta')):
        df = df.sort_values(by='mass')
        error = df.alpha_e 
        value = df.alpha 
        x= df.mass + (i-nbetas/2)*shift

        marker = next(markers)
        color = next(colors)
        facecolorfun = next(facecolorfuns)
        plt.plot(x,value,
                 label = f"$\\beta:{beta:1.2f}$",
                 marker = marker,
                 linestyle = 'none',
                 markeredgecolor = color,
                 markerfacecolor = facecolorfun(color) )
        plt.errorbar(x,value,yerr = error, linestyle = 'none',color = color) 
        
    plt.xlim([0,None])
    plt.ylim([0,None])
    plt.grid()
    plt.legend()
    filename = os.path.join(el.pbp_inf_dir,f"decay_constants_{L}_v2.pdf")
    print(f"Writing {filename}")
    plt.savefig(filename)

process(data,12)
process(data,16)
