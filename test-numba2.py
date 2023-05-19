#https://towardsdatascience.com/supercharging-numpy-with-numba-77ed5b169240

from numba import njit
from numba.np.ufunc import parallel
import numpy as np
from time import perf_counter

from numba import prange # to force explicit parallel runs of the loop


# if using notebook replace this with %%timeit
def timer(f,*args):
    start = perf_counter()
    f(*args)
    return 1000 * (perf_counter() - start)


# example 1.1 Native Python code
def trace_normal(a): # native python function
    trace = 0.0
    for i in range(a.shape[0]):  
        trace += a[i, i] 
    return a + trace     

# example 1.2 mumpy code
# baseline operation that we will replicate in numba
def pure_numpy_trace(a):
    return (np.trace(x) + x)

# Example 1.3 numba optimized code (nopython)
@njit
def trace_numba(a): # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):   # Numba likes loops
        trace += a[i, i] # Numba likes NumPy functions
    return a + trace              # Numba likes NumPy broadcasting


@njit(parallel=True)
def trace_numba_parallel(a):
    trace = 0.0
    for i in range(a.shape[0]):
        trace += a[i, i] 
    return a + trace    

if __name__=="__main__":

  # Samples
  large_x = np.arange(1000000).reshape(1000, 1000)
  small_x = np.arange(10000).reshape(100, 100)

  # Try with the large matrix
  x = large_x
  # runtime in ms 
  t1 = 1000 * np.mean([timer(trace_normal,x) for _ in range(1000)])
  print(f'Native python  = {t1}')
  t2 = 1000 * np.mean([timer(pure_numpy_trace,x) for _ in range(1000)])
  print(f'Pure numpy     = {t2}')
  t3 = 1000 * np.mean([timer(trace_numba,x) for _ in range(1000)])
  print(f'numba          = {t3}')
  t4 = 1000 * np.mean([timer(trace_numba_parallel,x) for _ in range(1000)])
  print(f'numba parallel = {t4}')

  # to check what automatic optimisations has numba done for us
  # As the name suggests works only for the case of  
  #trace_numba_parallel.parallel_diagnostics(level=4)