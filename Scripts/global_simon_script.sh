#!/bin/bash 
# for simon's data.
# FIXME : b=0.3 -> b=0.30 (and 0.4)

for machine in dirac sunbird
do
    for dir in  ../Data/simon/$machine/b_0.*/Ls_*/m_0.0?
    do 
        ../ProtocolUtils/log ../Scripts/single_dir_simon.sh $dir $machine
    done 
done


