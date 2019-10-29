#!/bin/bash
dir=$1
FILETYPE=$2
PREFIX=$3

declare -A HEADERS
HEADERS[fort.100]=""
HEADERS[fort.200]="psibarpsi susclsing"
HEADERS[fort.11]="isweep gaction paction"

declare -A SIMON_NAMES
SIMON_NAMES[fort.100]=conds
SIMON_NAMES[fort.200]=condensate
SIMON_NAMES[fort.11]=bose

# finding out the machine
read machine <<< $(echo $dir |grep "dirac\|sunbird" | sed -r 's/.*(sunbird|dirac).*/\1/')
if [ -z "$machine" ] 
then
    machine=sunbird
fi

# This is for simon's directory layout
read betaraw Ls m <<< $(echo $dir | sed -r 's|.*/b_(.*)/Ls_(.*)/m_(.*)|\1 \2 \3|')

echo betaraw $betaraw dir $dir
# 'betaraw' can contain more than just numbers.
read beta copy L <<< $(echo $betaraw | sed -r 's/([01]\.[0-9]+)([a-zA-Z]*)(_16)*/"\1" "\2" "\3"/')

beta=$(echo $beta | tr -d \")
copy="$(echo $copy | tr -d \")"
L="$(echo $L | tr -d \" | tr -d _ )"


if [ -z "$L" ] 
then
    if [ "$machine" == "dirac" ]
    then 
        L=16
    elif [ "$machine" == "sunbird" ] 
    then
        L=12
    fi
fi

# creating newdir name incrementally
beta03=$(echo $beta | awk '{printf("%.3f",$1)}')
beta02=$(echo $beta | awk '{printf("%.2f",$1)}')
newdir=Ls$Ls.beta$beta.m$m
if [ ! -z "$copy" ] 
then
    echo copy: $copy
    newdir=$copy/$newdir
fi
newdir=$L/$newdir
if [ ! -z "$PREFIX" ]
then
    echo PREFIX: $PREFIX
    newdir=$PREFIX/$newdir
fi
newdir=simon/$newdir

# creating newdir
mkdir -p $newdir

rm -f $newdir/$FILETYPE
echo 'Reading $(shell find '$dir' -name '"'"${SIMON_NAMES[$FILETYPE]}'_*'"'"')'
echo Writing $newdir/$FILETYPE
echo ${HEADERS[$FILETYPE]} > $newdir/$FILETYPE
for file in $dir/${SIMON_NAMES[$FILETYPE]}_* 
do 
    cat $file >> $newdir/$FILETYPE
done
