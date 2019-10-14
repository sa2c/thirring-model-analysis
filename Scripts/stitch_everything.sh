#!/bin/bash

# This might be actually simpler than using the makefile for this.
for dir in ../Data/thirring_runs1/all_dirs/Ls* 
do 
    . ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log stitch_together_wrapper $dir 1
done
for dir in ../Data/thirring_runs2/all_dirs/Ls* 
do
    . ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log stitch_together_wrapper $dir 2
done
for dir in ../Data/16/all_dirs/Ls* 
do
    . ../Scripts/lib.sh&&cd .&&../ProtocolUtils/log stitch_together_wrapper $dir 1
done


#find all_dirs/ | xargs cat 2>/dev/null| md5sum
