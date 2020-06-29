#Notes

This directory contains the data computed with the new code, parallelised in
the "third" dimension and the results of the analysis of correctness of said 
code. 

The data files (contained in the directories `Data/Ls*`) have been partially 
produced with the old code and partially produced with the new code.

The files `Data/linecount_fort*.txt` contain the line counts of the data file
before switching to the new code, allowing an easy comparison.
These files have been produced with the script `Data/linecount.sh`. 

**NOTE**: The collected data is **not** under version control.

Data can be retrieved from the Dirac machine with the `Data/sync.sh` script.
Results (pictures) can be reproduced with `make`, using `Analysis/Makefile`.


#Old Notes

*The following text comes from the README file in the RUNS5.4SRNO directory on
the peta4 DiRAC machine in Cambridge. That directory contains another 
directory, "all_dirs", which contains the directories that are now in 
Data.*


This directory had been created as a copy of the ~/RUNS4 directory, with the command

```bash
rsync -av --include=*/ --exclude=slurm*.out --exclude=program_status.?????* --exclude=con.?????* --exclude=random_seed.?????* ../RUNS4/all_dirs .
``` 
Notable changes:
- `bulk_rhmc moved to point at `~/thiring-rhmc2/bulk_rhmc48_b5f4ce_SRNO`
- job names changed. (only the suffix, from `_4` to something new.)

In this case, the program has been changed making sure that all the ranks are 
starting with the same momenta (it should have already been so) and SITERANDOM is NOT used.
Also, 4 ranks are used in the "third" direction.
(This information should be seen in the commit history up to b5f4ce).

