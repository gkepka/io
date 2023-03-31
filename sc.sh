#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time=05:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu
./setup-environment.sh
curl https://cran.r-project.org/src/base/R-4/R-4.2.3.tar.gz -o R-4.2.3.tar.gz
tar xf R-4.2.3.tar.gz
R --no-save < start.R