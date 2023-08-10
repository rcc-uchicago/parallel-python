# Demo: Strong scaling performance with multiprocessing
import os
import multiprocessing as mp
from multiprocessing import Pool
import functools

from timeit import timeit
import numpy as np

import matplotlib.pyplot as plt

# ensure not to oversubscribe the CPU cores
os.environ["OMP_NUM_THREADS"] = "1"

nmax_cores = mp.cpu_count()
#print(f"Max number of cores: {nmax_cores}")

def calculate_pi(darts):
    """approximate pi by throwing darts at a board"""
    np.random.seed() # we need to set the random seed... see what happens if you comment this line out
    x = np.random.uniform(-1, 1, darts)
    y = np.random.uniform(-1, 1, darts)
    r_sq = x**2 + y**2
    return 4*np.sum(r_sq<1)/darts

# brute force reduction
def calculate_pi_parallel(darts_per_process, Ncores):
  with Pool(Ncores) as pool:
    results = pool.map(calculate_pi, [darts_per_process for i in range(Ncores)])
  return np.sum(results)/Ncores

# generalized combination for reduction
def combine_operator(a, b):
  return (a + b)

def calculate_pi_parallel_reduce(darts_per_process, Ncores):
  with Pool(Ncores) as pool:
    results = pool.map(calculate_pi, [darts_per_process for i in range(Ncores)])
  return functools.reduce(combine_operator, results)/Ncores
  #return functools.reduce(lambda a, b: a+b, results)/Ncores

if __name__=="__main__":

  # total number of darts to distribute across the procs: do some experiemtn
  # TODO: try different values of N for elapsed times
  
  N = 10000000

  # iterate over several Ncores
  Ncores = range(1, 8)
  times = np.array([timeit(lambda: calculate_pi_parallel_reduce(int(N/Nc), Nc), number=1) for Nc in Ncores])

  # strong scaling
  #plt.gca().set(xlabel='Ncores', ylabel='Time, sec', xticks=Ncores)
  #plt.plot(Ncores, times)
  #plt.show()

  # actual speedup vs theoretical (linear strong scaling)
  speedup = times[0]/times
  plt.plot(Ncores, Ncores, 'o-', label='theoretical')
  plt.plot(Ncores, speedup, 'v-', label='actual')
  plt.gca().set(xlabel='Ncores', ylabel='Speedup', xticks=Ncores, yticks=Ncores)
  plt.grid()
  plt.legend()
  plt.show()


