#!/bin/bash 
# for simon's data.

for machine in dirac sunbird
do
    PREFIX=""
    for filetype in fort.100 fort.11 fort.200
    do
        for dir in  ../Data/simon/$machine/b_0.*/Ls_*/m_0.0?
        do 
            ../ProtocolUtils/log ../Scripts/single_dir_simon1.sh $dir $filetype $PREFIX
        done 
    done 
done


# old stuff
for filetype in fort.100 fort.11 fort.200
do
    PREFIX=old
    for dir in  ../Data/simon_oldstuff/b_0.*/Ls_*/m_0.0?
    do 
        ../ProtocolUtils/log ../Scripts/single_dir_simon1.sh $dir $filetype $PREFIX 
    done 
done 

