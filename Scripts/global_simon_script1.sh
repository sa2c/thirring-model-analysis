#!/bin/bash 
# for simon's data.
# FIXME : b=0.3 -> b=0.30 (and 0.4)

for machine in dirac sunbird
do
    for filetype in fort.100 fort.11 fort.200
    do
        for dir in  ../Data/simon/$machine/b_0.*/Ls_*/m_0.0?
        do 
            ../ProtocolUtils/log ../Scripts/single_dir_simon1.sh $dir $machine $filetype
        done 
    done 
done


