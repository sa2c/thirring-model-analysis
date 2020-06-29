#!/usr/bin/env python3
'''
This script is used to check that the new code optimized
by Makis Kappas produces results that are compatible with 
the ones produced by the old code.

This requires computing mean and error of the quantities 
before and after the change. In order to compute the error, one needs
to estimate the block size first.
'''
from lib import blockingMeanErr
import os
from glob import glob
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import threading
from yaml import load,dump,Loader,Dumper
from itertools import cycle

def get_all_data(basename):
    '''
    Get all the data in all the files of a given type (e.g. fort.200), with 
    their directories and parameters.
    '''
    pattern = "Ls(?P<Ls>.*)\.beta(?P<beta>.*)\.m(?P<m>.*)"

    filenames = glob(f"*/{basename}")
    return [ dict(**re.search(pattern,os.path.dirname(f)).groupdict(),
              data = np.loadtxt(f),
              directory = os.path.dirname(f)) for f in filenames ]

def plot_mean_err(trajcol,datacol):
    '''
    Plot the usual diagram error vs blocking.
    trajcol and datacol must be 1d arrays.
    '''
    maxblock = len(datacol)//5
    valerrs = [(bsize,*blockingMeanErr(datacol,bsize)) for bsize in range(1,maxblock)]
    valerrs = np.array(valerrs)

    x = valerrs[:,0]
    y = valerrs[:,1]
    yerr = valerrs[:,2]

    plt.errorbar(x,y,yerr=yerr)

    return (y-yerr).min(),(y+yerr).max() 


trajcolidxs = { 'fort.200':0, 'fort.11': 1}

try:
    with open("blocksizes.txt",'r') as f:
        blocksizes = load(f,Loader=Loader)
except:
    blocksizes = {}

def check_block_sizes():
    plotandcheck = True 
    for basename in ['fort.200', 'fort.11']:
        for d in get_all_data(basename):
            data = d['data']
            trajcolidx = trajcolidxs[basename]
            trajcol = data[:,trajcolidx]
            for datacolidx in range(trajcolidx+1,data.shape[1]):
                datacol = data[:,datacolidx]
                directory = d['directory']
                key = (basename,directory,datacolidx)
    
                if plotandcheck:
                    plt.figure()
                    ymin, ymax = plot_mean_err(trajcol,datacol)
        
                    def work():
                        #nonlocal key
                        blocksize = input(f"{key} - blocksize:")
                        try:
                            if blocksize == 'n':
                                pass
                            else:
                                blocksizes[key] = int(blocksize)
                        except:
                            pass
        
                    x = threading.Thread(target = work)
                    x.start()
                    plt.title(key)
                    if key in blocksizes:
                        xl = blocksizes[key]
                        plt.plot([xl,xl],[ymin,ymax],color = "red")
                    plt.show()
                    x.join()
                else :
                    blocksizes[key] = 100
    
    with open("blocksizes.txt",'w') as f:
        dump(blocksizes,f,Dumper=Dumper)
    

def read_linecounts(basename):
    '''
    Read the line counts for the files of a given type (e.g., fort.11).
    The line counts are in a file called "linecount_<filetype>.txt"
    '''
    return pd.read_csv(f"linecount_{basename}.txt", sep = "\s+").set_index("Directory")

def process_data():
    points = []
    for basename in ['fort.200', 'fort.11']:
        linecounts = read_linecounts(basename)

        for d in get_all_data(basename):
            data = d['data']
            trajcolidx = trajcolidxs[basename]
            trajcol = data[:,trajcolidx]
            for datacolidx in range(trajcolidx+1,data.shape[1]):
                datacol = data[:,datacolidx]
                directory = d['directory']
                key = (basename,directory,datacolidx)
                blocksize = blocksizes[key]

                original_data_len = linecounts.loc[directory,'ReferenceLength'] 
                original_data = datacol[blocksize:original_data_len]
                new_data = datacol[original_data_len+blocksize:]

                oldval,olderr = blockingMeanErr(original_data,blocksize)
                newval,newerr = blockingMeanErr(new_data,blocksize)

                new_points = { 'basename' : basename,
                               'colidx' : datacolidx,
                               'oldval' : oldval,
                               'olderr' : olderr,
                               'newval' : newval,
                               'newerr' : newerr}

                new_points.update(d)
                points.append(new_points)

    res = pd.DataFrame(points)

    res.m = res.m.astype(float)
    res.beta = res.beta.astype(float)
    return res


def plot_all_data(data):


    def plot_single_fig(df):
        # for a column of a single data type
        basename = df.basename.iloc[0]
        colidx = df.colidx.iloc[0]
        marker_cycle = cycle(['+','^','>','o','*'])

        def plot_single_m(dfm):
            m = dfm.m.iloc[0]
            x = dfm.beta

            ynew = dfm.newval
            yenew = dfm.newerr

            yold = dfm.oldval
            yeold = dfm.olderr

            xsorted = x.sort_values()

            shift = (xsorted.iloc[1]-xsorted.iloc[0])/10
            marker = next(marker_cycle)
            plt.errorbar(x-shift,yold,yerr =yeold, label = f"m={m} (old)",linestyle = "none", marker = marker)
            plt.errorbar(x+shift,ynew,yerr =yenew, label = f"m={m} (new)",linestyle = "none", marker = marker)

        plt.figure()
        df.groupby('m').apply(plot_single_m)
        plt.title(f"{basename} - column:{colidx}")
        plt.legend()
        plt.savefig(f"{basename}_{colidx}.png")

    data.groupby(['basename','colidx']).apply(plot_single_fig)

def plot_all_data_diff(data):
    def plot_single_fig(df):
        # for a column of a single data type
        plt.figure()
        basename = df.basename.iloc[0]
        colidx = df.colidx.iloc[0]
        m = df.m.iloc[0]

        x = df.beta

        ynew = df.newval
        yenew = df.newerr

        yold = df.oldval
        yeold = df.olderr

        ydiff = ynew - yold
        yss = np.hypot(yeold,yenew)

        plt.plot(x,np.zeros_like(x))
        plt.errorbar(x,ydiff,yerr = yss,linestyle = "none")

        plt.title(f"{basename} - column:{colidx} - m={m} (new-old)")
        plt.ylabel("\Delta Y/\sqrt(dy_1^2+dy_2^2)")
        plt.xlabel("\beta")
        plt.savefig(f"diff_{basename}_{colidx}_m{m}.png")


    data.groupby(['basename','colidx','m']).apply(plot_single_fig)


if __name__ == "__main__":
    data = process_data()
    plot_all_data(data)
    plot_all_data_diff(data)













