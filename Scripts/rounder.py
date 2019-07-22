#!/usr/bin/env python3

def rounder(value,error):
    import math
    exp10val = math.floor(math.log10(math.fabs(value)))
    exp10err = math.floor(math.log10(error))

    maxexp = max(exp10val,exp10err)

    terr = error / (10**exp10err)
    if terr < 3:
        terr *= 10
        texp10err = exp10err-1
    else:
        texp10err = exp10err

    tval = value /  (10**(texp10err))

    tval = round(tval)
    terr = round(terr)

    tval = tval / 10**(maxexp-texp10err)

    if exp10err == maxexp and terr > 9:
        terr = terr/10


    formatstring = '{0:1.'+str(maxexp-texp10err)+'f}({1})'
    string = formatstring.format(tval,terr)
    exp10 = maxexp
    return string,exp10



