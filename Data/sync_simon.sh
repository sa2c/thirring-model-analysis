#!/bin/bash

source $1 

echo "L=16, peta4(dirac), only RUNS2"
rsync -av   --include '*/' --include-from included_simon.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:'/home/dc-hand4/thirring/thiring-rhmc/b_*'  ./simon/dirac

rsync -av   --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:'/home/dc-hand4/thirring/newcode/runs/b_*'  ./simon/dirac_newcode
