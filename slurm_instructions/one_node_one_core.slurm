#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=0-00:10:00
#SBATCH --partition=interactive
#SBATCH -o ../FinalOutputs/1-node-1-core-output.%a.out

# Load required modules
module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4

# Launch multiple process python code
echo "------ 1-node-1-core --------"
time mpiexec -n 1 python3 -m mpi4py ../app.py ../data/bigTwitter.json ../data/sydGrid.json ../data/lang.json ../data/tmp
