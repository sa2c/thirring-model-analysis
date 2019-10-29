#!/bin/bash

declare -A HEADERS
HEADERS[fort.100]=""
HEADERS[fort.200]="psibarpsi susclsing"
HEADERS[fort.11]="isweep gaction paction"

deal_with_all_files(){
    file=$1
    prefix=$2
    FILETYPE=$3

    for file in $(find ../Data/$prefix -name $FILETYPE)
    do 
    newdir=$(dirname $file)
    newdir=$(basename $newdir)
    newdir=$prefix/$newdir
    mkdir -p $newdir
    newfile=$newdir/$(basename $file)
    echo Reading $file
    echo ${HEADERS[$FILETYPE]} > $newfile
    echo Writing $newfile
    cat $file >> $newfile
done 
 
}

for FILETYPE in fort.100 fort.200 fort.11
do
    deal_with_all_files $file peta4_RUNS2_L16  $FILETYPE
    deal_with_all_files $file sunbird_thirring_runs3_L12 $FILETYPE
done 
