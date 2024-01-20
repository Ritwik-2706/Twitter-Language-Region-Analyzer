## Cloud Computing Assignment - 1
## Nithin Mathew - 1328669 , Ritwik Giri - 1301272

# Twitter Language Region Analyzer

The python package analyzes the region-wise tweets and identifies the total languages used in the particular location grid.


## 1 Node 1 Core SLURM Instructions
```bash
#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=0-00:10:00
#SBATCH --partition=interactive
#SBATCH -o ../FinalOutputs/1-node-1-core-output.%a.out

module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4

time mpiexec -n 1 python3 -m mpi4py ../app.py ../data/bigTwitter.json ../data/sydGrid.json ../data/lang.json ../data/tmp
```
## 1 Node 8 Cores
```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=0-00:04:00
#SBATCH --partition=interactive
#SBATCH -o ../FinalOutputs/1-node-8-cores-output.%a.out

module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4

time mpiexec -n 8 python3 -m mpi4py ../app.py ../data/bigTwitter.json ../data/sydGrid.json ../data/lang.json ../data/tmp
```


## 2 Nodes 8 Cores SLURM Instructions
```bash
#!/bin/bash
# 2 nodes, 4 tasks per node = 8 cores
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=0-00:10:00
#SBATCH --partition=interactive
#SBATCH -o ../FinalOutputs/2-node-8-cores-output.%a.out

module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4

time mpiexec -n 8 python3 -m mpi4py ../app.py ../data/bigTwitter.json ../data/sydGrid.json ../data/lang.json ../data/tmp
```


## Load Required Modules along with SLURM instructions

```bash
module load mpi4py/3.0.2-timed-pingpong
module load protobuf-python/3.10.0-python-3.7.4
```

## Execution
Load symbolic link to bigTwitter.json and sydGrid.json to data folder

```bash
ln -s /data/projects/COMP90024/bigTwitter.json ./data/
ln -s /data/projects/COMP90024/sydGrid.json ./data/
```

app.py is invoked by SLURM instructions located in the slurm_instructions folder

1 Node 1 Core
```bash
cd slurm_instructions
sbatch one_node_one_core.slurm
```
1 Node 8 Core
```bash
cd slurm_instructions
sbatch one_node_eight_cores.slurm
```

2 Node 8 Core
```bash
cd slurm_instructions
sbatch two_nodes_eight_cores.slurm
```
