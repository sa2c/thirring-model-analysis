#!/bin/bash
dir=$1
machine=$2

read beta Ls m <<< $(echo $dir | sed -r 's|.*b_(.*)/Ls_(.*)/m_(.*)|\1 \2 \3|')

newdir=simon/$machine/Ls$Ls.beta$(echo $beta | awk '{printf("%.2f",$1)}').m$m
mkdir -p $newdir

rm -f $newdir/fort.100
rm -f $newdir/fort.200 
rm -f $newdir/fort.11  
for file in $dir/conds_*      
do 
    echo Reading $file
    cat $file >> $newdir/fort.100 
done
echo Writing $newdir/fort.100 
for file in $dir/condensate_* 
do 
    echo Reading $file
    cat $file >> $newdir/fort.200 
done
echo Writing $newdir/fort.200 
for file in $dir/bose_*       
do 
    echo Reading $file
    cat $file >> $newdir/fort.11  
done
echo Writing $newdir/fort.11  

