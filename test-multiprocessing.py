# ref: https://www.anyscale.com/blog/parallelizing-python-code
import os
import math
import numpy as np
from timebudget import timebudget
from multiprocessing import Pool

iterations_count = round(1e7)

# just repeat the same operation exp(x)*sinh(x) for iterations_count times with x = 1
def complex_operation(input_index):
  print("Complex operation. Input index: {:2d}\n".format(input_index))
  [math.exp(i) * math.sinh(i) for i in [1] * iterations_count]

def complex_operation_numpy(input_index):
  print("Complex operation. Input index: {:2d}\n".format(input_index))
  data = np.ones(iterations_count)
  np.exp(data) * np.sinh(data)

# Using for loop
#@timebudget
#def run_complex_operations(operation, input):
#  for i in input:
#    operation(i)

# Using pool
@timebudget
def run_complex_operations(operation, input, pool):
  pool.map(operation, input)

processes_count = 8

if __name__ == '__main__':
  print('Number of CPUs in the systems: {}'.format(os.cpu_count()))
#  run_complex_operations(complex_operation, range(10))
  input = range(10)
  print(input)
  processes_pool = Pool(processes_count)
  print("Without numpy")
  run_complex_operations(complex_operation, range(10), processes_pool)
  print("With numpy")
  run_complex_operations(complex_operation_numpy, range(10), processes_pool)
