
import os
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool, Process
import functools

#import cProfile
from pyinstrument import Profiler

# ensure not to oversubscribe the CPU cores
os.environ["OMP_NUM_THREADS"] = "1"

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

# put the result in a queue instead of returning
def calculate_pi_serial(darts, queue):
    """approximate pi by throwing darts at a board"""
    np.random.seed() # we need to set the random seed... see what happens if you comment this line out
    x = np.random.uniform(-1, 1, darts)
    y = np.random.uniform(-1, 1, darts)
    r_sq = x**2 + y**2
    queue.put(4*np.sum(r_sq<1)/darts)

# calculate pi with queue
def calculate_pi_parallel_queue(darts_per_process, Ncores):
  processes = []
  queue = []
  for i in range(Ncores):
    q = mp.Queue()
    p = Process(target=calculate_pi_serial, args=(darts_per_process, q))
    p.start()
    processes.append(p)
    queue.append(q)
  for p in processes:
    p.join()

  # get the result from the queues
  total = 0
  for q in queue:
    total += q.get()
  return np.sum(total)/Ncores

# generalized combination for reduction
def combine_operator(a, b):
  return (a + b)

def calculate_pi_parallel_reduce(darts_per_process, Ncores):
  with Pool(Ncores) as pool:
    results = pool.map(calculate_pi, [darts_per_process for i in range(Ncores)])
  return functools.reduce(combine_operator, results)/Ncores
  #return functools.reduce(lambda a, b: a+b, results)/Ncores

if __name__=="__main__":

  # max number of cores
  nmax_cores = mp.cpu_count()
  print(f"Max number of cores: {nmax_cores}")


  N = 10000000
  Ncores = 4

  #profiler = Profiler()
  #profiler.start()
  #a = calculate_pi_parallel_queue(darts_per_process, Ncores)
  #print(a)
  
  a = calculate_pi_parallel_reduce(N//Ncores, Ncores)
  print(a)

  #profiler.stop()
  #profiler.print()



