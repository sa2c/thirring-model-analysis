#!/bin/bash

FILE_TO_SPLIT=$1

source $(dirname ${BASH_SOURCE[0]})/dirname_lib.sh

# this is ugly. There should not be need for scanning also in L, as a lot 
# of data points have been taken only for a specific L.
# Anyway, the action of this script in not logged completely.
echo Reading $FILE_TO_SPLIT
for L in 12 16 
do 
    while read Ls beta m 
    do 
        LsBetaM=$(dirLsBetaM_from_LsBetaM $Ls $beta $m)
        echo LsBetaM $LsBetaM
        if (select_lines_matching_LsBetaM $LsBetaM $FILE_TO_SPLIT | grep $L &>/dev/null)
        then
            ../ProtocolUtils/log ../Scripts/single_analysis_file_splitter.sh $FILE_TO_SPLIT $L $LsBetaM
        else 
           echo Nothing found for LsBetaM $LsBetaM and L $L, no log will be produced
        fi
    done <<< $(tail -n+2 $FILE_TO_SPLIT | sed -r 's/.*(Ls[0-9]+\.beta[01]\.[0-9]+.m0\.[0-9]+).*/\1/' | LsBetaM_from_dirLsBetaM | sort -u )
done

