## Serial
Solve the heat equation in serial
```
python heat_equation.py
```

## Parallel
A partial MPI implementation that uses `comm.Gather` but not `comm.send` or `comm.recv` to communicate during the timestep
```
mpirun -np 4 python heat_equation_parallel_partial.py
```

The full MPI solution
```
mpirun -np 4 python heat_equation_parallel.py
```

## Package dependency
On Midway3,
```
module load python/anaconda-2021.05
conda activate mpi4py
```
