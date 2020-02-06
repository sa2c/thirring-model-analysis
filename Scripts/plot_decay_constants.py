#!/usr/bin/env python3
import pandas as pd
from glob import glob
from matplotlib import pyplot as plt
import extrapolation_library as el
import os


filenames = glob(os.path.join(el.pbp_inf_dir,'fort.200.analysis.set*'))

for filename in filenames:
    print(f"Reading {filename}")

data = pd.concat([ pd.read_csv(filename, sep='\s+') for filename in filenames ])

def process(data,L):
    plt.figure() 
    plt.title(f"Decay constants, {L}")
    plt.xlabel('mass')
    plt.ylabel('alpha')
    data = data.loc[(data.L == L )& (data.beta < 0.45),:]
    print(f"For L={L}, data points: {len(data)}")
    nbetas = len(data.beta.drop_duplicates())
    shift = 0.01 / 3 /  nbetas
    
    for i,(beta,df) in enumerate(data.groupby('beta')):
        df = df.sort_values(by='mass')
        error = df.alpha_e 
        value = df.alpha 
        x= df.mass + (i-nbetas/2)*shift
        color = plt.plot(x,value, 
                label = f"m = {beta}",
                marker = 'o',
                linestyle = 'none')[0].get_color()
        plt.errorbar(x,value,yerr = error, linestyle = 'none',color = color) 
        
    plt.xlim([0,None])
    plt.ylim([0,None])
    plt.grid()
    plt.legend()
    filename = os.path.join(el.pbp_inf_dir,f"decay_constants_{L}.png")
    print(f"Writing {filename}")
    plt.savefig(filename)

process(data,12)
process(data,16)
