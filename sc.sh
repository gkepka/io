#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time=05:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu
./setup-environment.sh
R --no-save < start.R