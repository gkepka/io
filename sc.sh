#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time=05:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add r/4.2.0-foss-2021b

virtualenv .venv
source .venv/bin/activate
pip install jmetalpy

chmod +x ./start.R
R --no-save < start.R
