#!/bin/bash

FILE_TO_SPLIT=$1

echo Reading $FILE_TO_SPLIT
for L in 12 16 
do 
    for LsBetaM in $(tail -n+2 $FILE_TO_SPLIT | sed -r 's/.*(Ls..\.beta0\..*.m0\.0.).*/\1/' | sort -u)
    do 
        if (grep $LsBetaM $FILE_TO_SPLIT | grep $L &>/dev/null)
        then
            ../ProtocolUtils/log ../Scripts/single_analysis_file_splitter.sh $FILE_TO_SPLIT $L $LsBetaM
        fi
    done 
done

