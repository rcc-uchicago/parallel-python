# Demo: numba with different decorators for on-the-fly optimization
from numba import(jit, vectorize, float32)

import numpy as np
import time
import matplotlib.pyplot as plt

# x and y are two arrays

#@vectorize([float32(float32,float32)], target='parallel')
@jit(nopython=True,parallel=True)
def rel_diff_cpu(x,  y):
  return 2 * (x - y) / (x + y)

np.seterr(divide='ignore')
numpy_cpu_times = []
numba_cpu_times = []
size_list = [1000, 10000, 100000, 1000000, 10000000]
for size in size_list:
  x=np.random.randn(size).astype(np.float32)
  y=np.random.randn(size).astype(np.float32)
  start_time_numpy = time.monotonic()
  2 * (x - y) / (x + y)
  numpy_cpu_times += [(time.monotonic() - start_time_numpy)]

  start_time_numba = time.monotonic()
  rel_diff_cpu(x, y)
  numba_cpu_times += [(time.monotonic() - start_time_numba)]

#print(numpy_cpu_times)
#print(numba_cpu_times)
plt.plot(size_list, numba_cpu_times, 'o-', label="numba CPU")
plt.plot(size_list, numpy_cpu_times, '-o', label="numpy")
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Array size")
plt.ylabel("Time elapsed")
plt.show()

