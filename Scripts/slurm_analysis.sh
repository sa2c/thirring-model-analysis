#!/bin/bash
###
#SBATCH --job-name="ThirringAnalyis"
#SBATCH --account=scw1379
#SBATCH --ntasks=1
#SBATCH --time=120
#SBATCH --oversubscribe
#SBATCH -o ThirringAnalysis.out.%J
#SBATCH -e ThirringAnalysis.err.%J

mycondainit(){
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/apps/local/languages/anaconda/2019.03/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/apps/local/languages/anaconda/2019.03/etc/profile.d/conda.sh" ]; then
        . "/apps/local/languages/anaconda/2019.03/etc/profile.d/conda.sh"
    else
        export PATH="/apps/local/languages/anaconda/2019.03/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
}


date
module load anaconda/2019.03
cd /scratch/s.michele.mesiti/thirring_model_analysis/Analysis
mycondainit 
conda activate ../conda
../Docs/reproducibility_compendium.sh
