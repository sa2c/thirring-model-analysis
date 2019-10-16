#!/bin/bash
dir=$1
machine=$2
FILETYPE=$3

declare -A HEADERS
HEADERS[fort.100]=""
HEADERS[fort.200]="psibarpsi susclsing"
HEADERS[fort.11]="isweep gaction paction"

declare -A SIMON_NAMES
SIMON_NAMES[fort.100]=conds
SIMON_NAMES[fort.200]=condensate
SIMON_NAMES[fort.11]=bose


read beta Ls m <<< $(echo $dir | sed -r 's|.*b_(.*)/Ls_(.*)/m_(.*)|\1 \2 \3|')

newdir=simon/$machine/Ls$Ls.beta$(echo $beta | awk '{printf("%.2f",$1)}').m$m
mkdir -p $newdir

rm -f $newdir/$FILETYPE
echo 'Reading $(shell find '$dir' -name '"'"${SIMON_NAMES[$FILETYPE]}'_*'"'"')'
echo Writing $newdir/$FILETYPE
echo ${HEADERS[$FILETYPE]} > $newdir/$FILETYPE
for file in $dir/${SIMON_NAMES[$FILETYPE]}_* 
do 
    cat $file >> $newdir/$FILETYPE
done
