#!/bin/bash
# 2 nodes, 4 tasks per node = 8 cores
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=0-00:10:00
#SBATCH --partition=interactive
#SBATCH -o ../FinalOutputs/2-node-8-cores-output.%a.out

# Load required modules
module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4

# Launch multiple process python code
echo "------- 2-nodes-8-cores --------"
time mpiexec -n 8 python3 -m mpi4py ../app.py ../data/bigTwitter.json ../data/sydGrid.json ../data/lang.json ../data/tmp