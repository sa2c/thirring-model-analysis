#!/bin/bash

FILE_TO_SPLIT=$1
L=$2
LsBetaM=$3

DIR_OUTPUT=analysis_setting_split

TMP_FILE=$DIR_OUTPUT/tmp

mkdir -p $DIR_OUTPUT

echo Reading $FILE_TO_SPLIT
head -n 1 $FILE_TO_SPLIT > $TMP_FILE
grep -E "^$L.*$LsBetaM.*" $FILE_TO_SPLIT >> $TMP_FILE

filename=$DIR_OUTPUT/L$L$LsBetaM.$FILE_TO_SPLIT 

echo Writing $filename
if test -r "$filename" -a -z "$REDOANYWAY"
then 
    cmp $TMP_FILE $filename && echo "Nothing to be done for $filename" || mv $TMP_FILE $filename
else 
    mv $TMP_FILE $filename
fi

rm -f $TMP_FILE
