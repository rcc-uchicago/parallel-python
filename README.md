# parallel-python
Parallel programming with Python exercises

On Midway3, with an interactive job
```
  module load python/anaconda-2021.05 openmpi/4.1.2+gcc-7.4.0
  source activate parallel
```

If you would like to clone the env `parallel`, first export
the packages installed into a text file
```
  conda env export > my-parallel-env.yml
```
modify the prefix in this text file, and then create your own env
in your own space:
```
  conda env create -f my-parallel-env.yml
```

This repo contains the following items:

Exercises discussed in the workshop:

* profiling.py             : using timers and profilers (Exercise 1)
* test-multiprocessing.py  : multiprocessing intro (Exercuse 2)
* map-reduce-pi.py         : calculating pi with multiprocessing via map/reduce (Exercise 3)
* performance.py           : strong scaling performance (Exercise 4)
* mpi-comm-ops.py          : mpi4py communication between procs (Exercise 5)
* test-multithreading.py   : multithreading examples (Exercise 6)

legacy/                    : folder containing the examples from the past workshops
  - mpi/                   : scripts showing send/recv to solve the 1D heat equation with mpi4py
  - notebooks/             : jupyter notebooks for calculating pi with multiprocessing

Extra stuffs:
* test-numba.py, test-numba2.py: using numba JIT
* mpi-calculate-pi.py      : calculating pi using mpi4py

Slides:
* python-workshop.pdf
