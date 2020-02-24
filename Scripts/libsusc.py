import numpy as np
import pandas as pd

def blockingDiscSuscErr(psibarpsi, susclsing, blockSize, volume):
    '''
    Computes disconnected part of the susceptibility with the 
    formula
    susc = 1/V (< (Tr M)^2 > - < Tr M >^2 )
    where:
      - per-conf estimate of Tr M -> V* psibarpsi
      - per-conf estimate of (Tr M)^2, unbiased -> V * susclsing
    Notice that, given the correlations, < Tr M >^2 is biased.
    We remove the bias and compute errors with the jackknife method.
    '''

    def susc_disc(psibarpsi,susclsing,volume):
        return np.mean(susclsing) - volume * np.mean(psibarpsi)**2

    # susceltibility on the whole dataset
    suscN = susc_disc(psibarpsi,susclsing,volume)

    sampleSize = data0.shape[0]
    xblocks = sampleSize / blockSize
    leftovers = sampleSize % blockSize
    nblocks = int(np.ceil(xblocks))

    # susceptibility removing one block at a time
    suscNms = []
    def cut_out_block(data,i,blockSize):
        start = i*blockSize
        end = (i+1)*blockSize
        return np.concatenate(( data[:start], data[end:]))

    for i in range(nblocks):
        tmpSusclsing  = cut_out_block(susclsing,i,blockSize)
        tmpPsibarpsi  = cut_out_block(psibarpsi,i,blockSize)
        suscNms.append(susc_disc(tmpPsibarpsi,tmpSusclsing,volume))

    suscNm = np.mean(np.array(suscNms))

    # jackknife: error computation (*on biased estimates) 
    suscNm_err = np.std(np.array(suscNms))

    # jackknife: extrapolation to nblocks->infty 
    # (standard jackknife technique to remove biases \propto 1/nblocks)
    susc = nblocks * suscN - (nblocks-1)*suscNm

    return susc, suscNm_err

def get_susc_and_errors(df_dict, output_name, psibarpsi_name, susclsing_name, analysis_settings):
    observable = output_name
    values_and_errors = pd.DataFrame(
        index=analysis_settings.index.drop_duplicates())
    values_and_errors[observable] = np.zeros_like(values_and_errors.index)
    values_and_errors[observable + 'Err'] = np.zeros_like(
        values_and_errors.index)

    bmeas_sizes = analysis_settings.blocksize / analysis_settings.measevery

    bmeas_sizes = bmeas_sizes.reset_index().drop_duplicates()
    bmeas_sizes = bmeas_sizes.set_index(['L', 'Ls', 'beta', 'mass'])

    for k, v in df_dict.items():
        try:
            L, Ls, beta, mass = k
            mean, err = blockingDiscSuscErr(psibarpsi=v[psibarpsi_name],
                    susclsing= v[susclsing_name],
                    blockSize= int(bmeas_sizes[0][k]),
                    volume = L**3)
            values_and_errors.loc[k, observable] = mean
            values_and_errors.loc[k, observable + 'Err'] = err
        except TypeError:
            with open('errors.txt', 'a') as f:
                f.write(f'Error: {k} {bmeas_sizes[0][k]} \n')
                print('Error, fix analysis settings file (check errors.txt)')

    return values_and_errors.reset_index()



