#!/bin/bash

deal_with_all_files(){
    prefix=$1
    FILETYPE=$2

    for file in $(find ../Data/$prefix -name $FILETYPE)
    do 
        ../ProtocolUtils/log ../Scripts/runs2.0.michele.single.sh $file $prefix $FILETYPE
    done 

}

for FILETYPE in fort.100 fort.200 fort.11
do
    deal_with_all_files peta4_RUNS2_L16  $FILETYPE || exit 1
    deal_with_all_files peta4_RUNS3_L16  $FILETYPE || exit 1
    deal_with_all_files peta4_RUNS4_L16  $FILETYPE || exit 1
    deal_with_all_files peta4_RUNS64_L16  $FILETYPE || exit 1
    deal_with_all_files sunbird_thirring_runs3_L12 $FILETYPE || exit 1
done 
