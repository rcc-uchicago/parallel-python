# parallel-python
Parallel programming with Python exercises

On Midway3, with an interactive job
```
  module load python/anaconda-2021.05 openmpi/4.1.2+gcc-7.4.0
  source activate parallel
```

This repo contains the following items:

Exercises:

* profiling.py             : using timers and profilers
* test-multiprocessing.py  : multiprocessing intro
* map-reduce-pi.py         : calculating pi with multiprocessing via map/reduce
* performance.py           : strong scaling performance
* mpi-comm-ops.py          : mpi4py communication between procs
* test-multithreading.py   : multithreading examples

legacy/                    : folder containing the examples from the past workshops
  - mpi/                   : scripts showing send/recv to solve the 1D heat equation with mpi4py
  - notebooks/             : jupyter notebooks for calculating pi with multiprocessing

Extra:
* test-numba.py, test-numba2.py: using numba JIT
* mpi-calculate-pi.py      : calculating pi using mpi4py

Slides:
* python-workshop.pdf
