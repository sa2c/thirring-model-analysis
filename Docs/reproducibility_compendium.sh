#!/bin/bash
####################################
###  REPRODUCIBILITY COMPENDIUM  ###
####################################

# we aggregate and move Simon's data to the format/layout 
# (directory names, file names) that are used with the rest of the analysis
# an we log out action on each directory (identified by machine, beta, Ls, m)
../Scripts/global_simon_script.sh

# we aggregate Michele's data 
../Scripts/stitch_everything.sh

# splitting the global analysis setting file 
# the command calls a lot of smaller commands and logs them
../Scripts/global_analysis_file_splitter.sh fort.200.analysis.set

# each file in  analysis_setting_split is processed separately and 
# the value of the condensate, with the error, is obtained.
for file in analysis_setting_split/L1*
do 
    ../ProtocolUtils/log ../Scripts/pbp_data_processing_v2.py $file
done 


# We do the separate fits for each Ls.
# we use the last version of eos_fit. 
for L in 12 16 
do 
    for Ls in 24 32 40 48 
    do 
        ../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set $Ls $L --savefig
    done 
done 

# doing extrapolation to Ls-> inf
for L in 12 16 
 do 
     grep -E '^'$L fort.200.analysis.set |  sed -r 's/.*Ls([0-9]{2}).beta(0.[0-9]*).m(0.[0-9]*).*/\3/' | sort -u | (
 while read m 
 do 
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_v2.py fort.200.analysis.set $m  $L
 done )
done 

# still need to fit said extrapolations
