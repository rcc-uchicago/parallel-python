# Demo: creating new processes with multiprocessing
# ref: https://www.anyscale.com/blog/parallelizing-python-code
import os
import math
import numpy as np
import time
from timebudget import timebudget
from multiprocessing import Process, Pool

iterations_count = round(1e7)

# just repeat the same operation exp(x)*sinh(x) for iterations_count times with x = 0.1
def complex_operation(input_index):
  print("Complex operation. Input index: {:2d}".format(input_index))
  [math.exp(i) * math.sinh(i) for i in [0.1] * iterations_count]

def complex_operation_numpy(input_index):
  print("Complex operation. Input index: {:2d}\n".format(input_index))
  data = np.ones(iterations_count)
  np.exp(data) * np.sinh(data)

# Using for loop
#@timebudget
#def run_complex_operations(operation, input):
#  for i in input:
#    operation(i)

# Using pool and map
@timebudget
def run_complex_operations(operation, input, pool):
  pool.map(operation, input)

processes_count = 8

if __name__ == '__main__':
  print('Number of CPUs in the systems: {}'.format(os.cpu_count()))
#  run_complex_operations(complex_operation, range(10))
  input = range(4)
  #print(input)
  
  print("Iterate 4 times")
  start = time.time()
  for i in input:
    complex_operation(i)
  end = time.time()
  print('Elapsed time (seconds): ', end - start)

  print("Create 4 processes..")
  start = time.time()
  p1 = Process(target=complex_operation, args=(1,))
  p2 = Process(target=complex_operation, args=(2,))
  p3 = Process(target=complex_operation, args=(3,))
  p4 = Process(target=complex_operation, args=(4,))
  #
  p1.start()
  p2.start()
  p3.start()
  p4.start()
  p1.join()
  p2.join()
  p3.join()
  p4.join()
  end = time.time()
  print('Elapsed time (seconds): ', end - start)

  #processes_pool = Pool(processes_count)
  #print("Without numpy")
  #run_complex_operations(complex_operation, range(10), processes_pool)
  #print("With numpy")
  #run_complex_operations(complex_operation_numpy, range(10), processes_pool)
