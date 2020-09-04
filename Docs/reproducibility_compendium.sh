#!/bin/bash
###
#SBATCH -A scw1379
#SBATCH -t 60
#SBATCH -n 1 
#SBATCH --job-name ThirringModelAnalysis
###
####################################
###  REPRODUCIBILITY COMPENDIUM  ###
####################################

# This is necessary on Sunbird
module load texlive
module load anaconda/2019.03
source activate
conda activate ../conda

# there is a file named 'condensdate_1' instead of 'condensate_1',
# fixing it, almost in place.

echo STEP: ../ProtocolUtils/log ../Scripts/fix_wrong_simon.sh
../ProtocolUtils/log ../Scripts/fix_wrong_simon.sh || exit 1 

# we aggregate and move Simon's data to the format/layout 
# (directory names, file names) that are used with the rest of the analysis
# an we log out action on each directory (identified by machine, beta, Ls, m)
# THIS IS FOR THE 'simon' directory and PARTIALLY for the simon_oldstuff directory
# Except Simon's run with the new code, that do no need stitching.
echo STEP ../Scripts/global_simon_script1.py 
../Scripts/global_simon_script1.py || exit 1 # stream 1 
# TODO: we need to take care of the parts of 'simon_olfstuff' directory
#       which to not fit the known patterns.

# we aggregate Michele's data - old
echo STEP ../Scripts/global_michele_script1.py
../Scripts/global_michele_script1.py || exit 1 # stream 2 

# we now strap a header on new Simon's data
echo STEP ../Scripts/global_simon_script2.py 
../Scripts/global_simon_script2.py || exit 1 # stream 3

# we strap a header on new michele's data
echo STEP ../Scripts/runs2.0.michele.sh 
../Scripts/runs2.0.michele.sh || exit 1 # stream 4

# we process all the fort.100 files, assuming constant thermalisation,
# blocking and measevery.
echo STEP ../Scripts/process_all_100s.py
../Scripts/process_all_100s.py || exit 1

# stream 1,2,3,4
echo STEP ../Scripts/create_fort.200_analysis_set.py 
../Scripts/create_fort.200_analysis_set.py && mv fort.200.analysis.set.synthetic fort.200.analysis.set || exit 1

# splitting the global analysis setting file 
# the command calls a lot of smaller commands and logs them
echo STEP ../Scripts/global_analysis_file_splitter.py fort.200.analysis.set
../Scripts/global_analysis_file_splitter.py fort.200.analysis.set|| exit 1  # stream 4

# each file in  analysis_setting_split is processed separately and 
# the values of the condensate and the susceptibility, with errors, are 
# obtained.
echo STEP pbp_data_processing
wait
for file in analysis_setting_split/L1*
do 
    ../ProtocolUtils/log ../Scripts/pbp_data_processing_v2.py $file || exit 1# stream 1,2,3,4
done 


# We do the separate fits for each Ls.
# we use the last version of eos_fit. 
MINBETA=0.3
MAXBETA=1.0

MINBETAPLOT=0.23
MAXBETAPLOT=0.60

echo STEP eos_fit, plot_susc
(for L in 12 16 
do 
    for Ls in 8 16 24 32 40 48 
    do 
        # notice: this does not actually read fort.200.analysis.set, but the files 
        # that have been created by the splitting
        echo L: $L Ls : $Ls
        echo ../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set $Ls $L $MINBETA $MAXBETA $MINBETAPLOT $MAXBETAPLOT --savefig 
        ../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set $Ls $L $MINBETA $MAXBETA $MINBETAPLOT $MAXBETAPLOT --savefig || exit 1 
        echo L: $L Ls : $Ls
        echo ../ProtocolUtils/log ../Scripts/plot_susc.py fort.200.analysis.set $Ls $L --savefig 
        ../ProtocolUtils/log ../Scripts/plot_susc.py fort.200.analysis.set $Ls $L --savefig || exit 1
    done 
done )  || exit 1

#doing extrapolation to Ls-> inf
# extrapolate everything separately, save values into file

# we neglect beta=1.0
echo "STEP l->inf extrapolation"
(
NBOOT=30 # This is small.
../Scripts/get_unique_Lbm.py fort.200.analysis.set | grep -v Reading | while read L beta m 
 do 
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_v2.py fort.200.analysis.set $m $beta $L $NBOOT || exit 1
 done
) || exit 1

# Plot the decay constants as a function of mass, grouped by beta
echo STEP ../Scripts/plot_decay_constants.py 
../Scripts/plot_decay_constants.py || exit 1
../Scripts/plot_decay_constants_v2.py || exit 1

# read extrapolated parameters and make plots (grouping by (L,mass) which 
#    means many betas per plot.
echo STEP plot extrapolation to "l->inf"
( for L in 12 16
 do 
     for m in $(seq 0.01 0.01 0.05)
 do 
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_plot.py fort.200.analysis.set $m $L || exit 1
    ../ProtocolUtils/log ../Scripts/extrapolate_to_linf_plot_v2.py fort.200.analysis.set $m $L || exit 1
 done 
done  && \
../ProtocolUtils/log ../Scripts/extrapolate_to_linf_plot.py fort.200.analysis.set 0.005 16 || exit 1
../ProtocolUtils/log ../Scripts/extrapolate_to_linf_plot_v2.py fort.200.analysis.set 0.005 16 || exit 1
)  || exit 1 

# plotting extrapolated values of psibarpsi together with their errors.
BETAMAX=0.44 # extrapolated values do not converge for high beta
echo STEP plot pbp extrapolated to "l->inf"
( for L in 12 16
do
    ../ProtocolUtils/log ../Scripts/plot_psibarpsi_extrapolated.py fort.200.analysis.set $L $BETAMAX
done || exit 1)  || exit 1

# extracting pbp values from fit results
echo STEP extract pbp extrapolated to "l->inf" and fit
(
ls psibarpsi_extrapolated/fort.200* | xargs -n 1 basename | tr '_' ' ' | while read file L beta m 
do 
    echo $file $L $beta $m
    ../ProtocolUtils/log ../Scripts/extract_pbp_extrapolated.py $file $L $beta $m || exit 1
done

# fit the extrapolated values (the reasonable ones) 
../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set INF 12 0.3 0.44 0.23 0.6 --savefig || exit 1

../ProtocolUtils/log ../Scripts/eos_fit_v3.py fort.200.analysis.set INF 16 0.3 0.44 0.23 0.6 --savefig || exit 1
)  ||exit 1

wait

