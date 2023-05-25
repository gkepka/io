#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks-per-node=48
#SBATCH --time=08:00:00
#SBATCH --mem=5G
#SBATCH --partition=plgrid
#SBATCH --account=plgintobllab
#SBATCH --output="log.txt"
#SBATCH --error="err.txt"

module add r/4.2.0-foss-2021b

virtualenv .venv
source .venv/bin/activate
pip install deap
pip install OptimizationTestFunctions

chmod +x ./start.R
R --no-save < start.R
