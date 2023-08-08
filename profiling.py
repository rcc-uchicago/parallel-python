# running with pdb: python3 -m pdb profiling.py
import time
import numpy as np
import multiprocessing as mp
import pandas as pd

#from timeit import timeit
#import cProfile
from pyinstrument import Profiler

a = np.random.normal(size=(2000, 1000)).astype('float32')
b = np.random.normal(size=(1000, 200)).astype('float32')

def read_file(filename):
  df = pd.read_csv(filename)
  #print(df.to_string())

def iterate(N):
  for i in range(N):
    result = np.matmul(a, b)

def calculate_pi(darts):
    """approximate pi by throwing darts at a board"""
    np.random.seed() # we need to set the random seed... see what happens if you comment this line out
    x = np.random.uniform(-1, 1, darts)
    y = np.random.uniform(-1, 1, darts)
    r_sq = x**2 + y**2
    return 4*np.sum(r_sq<1)/darts

if __name__=="__main__":

  start = time.time()
  read_file('iris.csv')
  end =  time.time()
  print('Read a file (seconds): ', end - start)

  # Total number of darts
  # TODO: try different values of N for elapsed times
  N = 10000000

  start = time.time()
  a = calculate_pi(N)
  end =  time.time()
  print('Compute pi (seconds): ', end - start)
  
  # using timeit
  #t = timeit(lambda: calculate_pi(N), number=10)
  #print(f'Average elapsed time in seconds {t}')

  # using cProfile
  #prof = cProfile.Profile()
  #prof.enable()
  #a = calculate_pi(N)
  #prof.disable()
  #prof.print_stats()

  # using pyinstrument
  profiler = Profiler()

  profiler.start()
  a = calculate_pi(N)
  print(a)
  profiler.stop()
  profiler.print()

  # TODO: try iterate() instead of calculate_pi()
