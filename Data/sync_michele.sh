#!/bin/bash

source $1 

echo "L=12, Sunbird, only thirring_runs3 "
rsync -av  --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $SUNBIRD_LOGIN:/scratch/s.michele.mesiti/thirring_runs3/all_dirs  ./sunbird_thirring_runs3_L12 

echo "L=16, peta4(dirac), only RUNS2"
rsync -av   --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:/home/dc-mesi1/RUNS2/all_dirs  ./peta4_RUNS2_L16

echo "L=16, peta4(dirac), only RUNS3"
rsync -av   --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:/home/dc-mesi1/RUNS3/all_dirs  ./peta4_RUNS3_L16

echo "L=16, peta4(dirac), only RUNS4"
rsync -av   --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:/home/dc-mesi1/RUNS4/all_dirs  ./peta4_RUNS4_L16

echo "L=16, Ls64, peta4(dirac), only RUNS64"
rsync -av   --include '*/' --include-from included171019.txt --exclude '*' --prune-empty-dirs $PETA4_LOGIN:/home/dc-mesi1/RUNS64/alldirs  ./peta4_RUNS64_L16
