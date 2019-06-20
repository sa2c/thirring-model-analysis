#!/usr/bin/env python
import lib 
from sys import argv
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import leastsq,brentq
import numpy as np
import argparse as ap

parser = ap.ArgumentParser(description="An utility to plot and fit the condensate data for a single value of Ls.")

parser.add_argument('analysis_settings_filename',
        type=str,
        help="The name of the file containing the thermalization and the block sizes")

parser.add_argument('Ls',type=int,help='The chosen value of Ls')

parser.add_argument('--savefig',action='store_true',help='flag to save figure instead of showing it')

args = parser.parse_args()

analysis_settings = lib.filelist_parser(args.analysis_settings_filename)
Ls = args.Ls
df_dict = lib.cut_and_paste(analysis_settings)

print("Number of measurements per run:")
for k,v in df_dict.items():
    print(k,len(v))


values_and_errors = lib.get_values_and_errors(df_dict,'psibarpsi',analysis_settings)

for mass in set(values_and_errors.mass):
    filename = f'cond_m0{int(mass/0.01)}_Ls{Ls}'
    selection = (values_and_errors.Ls == Ls) & (values_and_errors.mass == mass)
    dftosave = values_and_errors.loc[selection,['beta','psibarpsi','psibarpsiErr']]
    print(f"Writing {filename}")
    cols = list(dftosave.columns)
    cols[0] = '#beta' # dirty trick
    dftosave.columns = cols 
    dftosave = dftosave.set_index('#beta') # dirty trick
    dftosave.to_csv(filename,sep = '\t')
    



condition = values_and_errors.Ls == Ls

values_and_errors = values_and_errors.loc[condition,:]

lib.plot_observable('psibarpsi',Ls,values_and_errors)

def equation_of_state(psibarpsi,beta,am,A,betac,p,B,delta):
    """Powerlaw equation of state - lhs"""
    return np.array(A*(beta-betac)*psibarpsi**p+B*psibarpsi**delta-am,dtype=float)

nbootstrap = 500
np.random.seed(seed=42)
bootstrap_values = np.random.normal(size=nbootstrap)

def error_on_equation_of_state(psibarpsi,psibarpsiErr,beta,am,A,betac,p,B,delta):
    """Error on Powerlaw equation of state - lhs"""
    eqerrors = []
    for i in range(nbootstrap): # bootstrap with 10 samples
        pbp = psibarpsi + psibarpsiErr * bootstrap_values[i]
        eqerrors.append(equation_of_state(pbp,beta,am,A,betac,p,B,delta))

    return np.vstack(eqerrors).std(axis=0)


def residuals(params,beta,psibarpsi,psibarpsiErr,am):
    A,betac,p,B,delta = params
    return equation_of_state(psibarpsi,beta,am,A,betac,p,B,delta)/\
            error_on_equation_of_state(psibarpsi,
                    psibarpsiErr,beta,am,A,betac,p,B,delta)


#a0 = np.array((2.0,0.3,1.0,12.0,3.0)) # array of intial guesses for fit
#actual results from fit 
if Ls == 32:
    a0 = np.array([2.90937512,0.24170218,1.0349304,9.66141308,3.85308926])
elif Ls == 40:
    a0 = np.array([3.30445818,0.25055222,1.06456595,32.29585502,4.64339238])
elif Ls==48:
    a0 = np.array([3.11646997,0.25647005,1.0538188,11.59937539,3.94485828])
print("Fitting (this may take a while)...")
output = leastsq(func = residuals,x0 = a0,args = (
    values_and_errors.beta,
    values_and_errors.psibarpsi,
    values_and_errors.psibarpsiErr,
    values_and_errors.mass 
    ),full_output = 1)


found_params = output[0]
A,betac,p,B,delta = found_params
print("Found params",found_params)

final_residuals = output[2]['fvec']
#reduced_chi_square  
num = (final_residuals**2).sum()
den = (len(final_residuals)-len(found_params))
plt.title(f"Ls={Ls}, X^2/ndof = {num:1.2f}/{den}")

iterables = [np.arange(0.01,0.06,0.01),np.arange(0.25,0.6,0.004)]
index = pd.MultiIndex.from_product(iterables,names = ['mass','beta'])

psibarpsi = pd.Series(index = index )
for mass,beta in psibarpsi.index:
    psibarpsi[(mass,beta)] = brentq(f = lambda y : 
            equation_of_state(y,beta,mass,*found_params),
            a= 0.0,
            b= 0.5)

for mass in np.arange(0.01,0.06,0.01):
    plt.plot(psibarpsi[mass],label = f'm={mass}',color = 'black',linestyle = '--')

if args.savefig :
    filename = f'fitLs{Ls}.png' 
    print(f"Writing {filename}")
    plt.savefig(filename)

else:
    plt.show()

