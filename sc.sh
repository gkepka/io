#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time=05:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

# module add scipy-bundle/2021.10-foss-2021b
module add r/4.2.0-foss-2021b
module add python/3.8.2-gcccore-9.3.0

chmod +x ./start.R
./setup-environment.sh
R --no-save < start.R
