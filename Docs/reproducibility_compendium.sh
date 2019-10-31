#!/bin/bash
####################################
###  REPRODUCIBILITY COMPENDIUM  ###
####################################

# there is a file named 'condensdate_1' instead of 'condensate_1',
# fixing it, almost in place.

../ProtocolUtils/log ../Scripts/fix_wrong_simon.sh || exit 1 

# we aggregate and move Simon's data to the format/layout 
# (directory names, file names) that are used with the rest of the analysis
# an we log out action on each directory (identified by machine, beta, Ls, m)
# THIS IS FOR THE 'simon' directory and PARTIALLY for the simon_oldstuff directory
../Scripts/global_simon_script1.sh & #|| exit 1 # stream 1 
# TODO: we need to take care of the parts of 'simon_olfstuff' directory
#       which to not fit the known patterns.

# we aggregate Michele's data - old
../Scripts/stitch_everything.sh & #|| exit 1 # stream 2 

# we strap a header on new michele's data
../Scripts/runs2.0.michele.sh & #|| exit 1 # stream 3

# splitting the global analysis setting file 
# the command calls a lot of smaller commands and logs them
../Scripts/global_analysis_file_splitter.sh fort.200.analysis.set& #|| exit 1  # stream 4

# each file in  analysis_setting_split is processed separately and 
# the value of the condensate, with the error, is obtained.
wait
for file in analysis_setting_split/L1*
do 
    ../ProtocolUtils/log ../Scripts/pbp_data_processing_v2.py $file || exit 1# stream 1,2,3,4
done 


# We do the separate fits for each Ls.
# we use the last version of eos_fit. 
MINBETA=0.3
(for L in 12 16 
do 
    for Ls in 8 16 24 32 40 48 
    do 
        # notice: this does not actually read fort.200.analysis.set, but the files 
        # that have been created by the splitting
        ../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set $Ls $L $MINBETA --savefig || exit 1 
    done 
done )  & #|| exit 1

#doing extrapolation to Ls-> inf
# extrapolate everything separately, save values into file

# we neglect beta=1.0
NBOOT=30 # This is small.
for L in 12 16 
 do 
     grep -E '^'$L fort.200.analysis.set |  sed -r 's/.*Ls([0-9]+).beta(0.[0-9]+).m(0.[0-9]+).*/\2 \3/' | sort -u |  (
 while read beta m 
 do 
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_v2.py fort.200.analysis.set $m $beta $L $NBOOT || exit 1
 done )
done 


# read extrapolated parameters and make plots (grouping by (L,mass) which 
#    means many betas per plot.
( for L in 12 16
 do 
     for m in $(seq 0.01 0.01 0.05)
 do 
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_plot.py fort.200.analysis.set $m $L || exit 1
 done 
done  )  & #|| exit 1 

# plotting extrapolated values of psibarpsi together with their errors.
( for L in 12 16
do
    ../ProtocolUtils/log ../Scripts/plot_psibarpsi_extrapolated.py fort.200.analysis.set $L
done)  & #|| exit 1

# Todo : fit the extrapolated values (once they become reasonable)
