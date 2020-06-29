#!/bin/bash
filename=$1
#filename=fort.200

linecount_file=linecount_$filename.txt

echo "Directory TotLength ReferenceLength Difference" > $linecount_file 
for dir in Ls48.beta0.*
do 
	echo $dir $(cat $dir/$filename |wc -l) $(cat ~/RUNS4/all_dirs/$dir/$filename | wc -l)
done | awk '{print $1,$2,$3,$2-$3}' >> $linecount_file
