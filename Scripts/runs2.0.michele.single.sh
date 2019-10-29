#!/bin/bash

declare -A HEADERS
HEADERS[fort.100]="isweep_total real_psibarpsi1 aimag_psibarpsi1 real_psibarpsi2 aimag_psibarpsi2"
HEADERS[fort.200]="idx psibarpsi susclsing"
HEADERS[fort.11]="isweep_total_start isweep gaction paction"

declare -A NUMCOLS
NUMCOLS[fort.100]=5
NUMCOLS[fort.200]=3
NUMCOLS[fort.11]=4

source $(dirname ${BASH_SOURCE[0]})/file_checks.sh

file=$1
prefix=$2
FILETYPE=$3

newdir=$(dirname $file)
newdir=$(basename $newdir)
newdir=$prefix/$newdir
mkdir -p $newdir
newfile=$newdir/$(basename $file)
echo Reading $file
echo ${HEADERS[$FILETYPE]} > $newfile
if [ $FILETYPE == fort.100 ] 
then
    sed -r 's/(-[0-9]\.)/ \1/g' $file >> $newfile
else
    cat $file >> $newfile
fi
check_file_columns $newfile ${NUMCOLS[$FILETYPE]} && echo Writing $newfile || exit 1


