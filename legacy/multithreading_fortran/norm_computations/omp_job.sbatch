#!/bin/bash

#Here is a comment

#SBATCH --job-name=MyJob
#SBATCH --output=MyJob-%j.out
#SBATCH --error=MyJob-%j.err
#SBATCH --time=1:00:00
#SBATCH --account=pi-neiman
#SBATCH --partition=caslake
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem=16000  #Per Node
##SBATCH --mem-per-cpu=2000 #Per CPU

module load gcc/9.2.0
make -f Makefile

export OMP_NUM_THREADS=8 
#Run your code
./norm_prog 

