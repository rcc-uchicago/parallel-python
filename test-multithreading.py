#https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/

import time, os
from threading import Thread, current_thread
from multiprocessing import Process, current_process
import pandas as pd

COUNT = 200000000
SLEEP = 5

def read_file(filename):
  df = pd.read_csv(filename)
  #print(df.to_string())

def io_bound(sec):

  pid = os.getpid()
  threadName = current_thread().name
  processName = current_process().name
  print(f"{pid} * {processName} * {threadName} ---> Start sleeping...")

  # sleep() is used to model IO bound executations where the CPU is idle
  time.sleep(sec)
  #read_file('iris.csv')

  print(f"{pid} * {processName} * {threadName} 	---> Finished sleeping...")

def cpu_bound(n):

  pid = os.getpid()
  threadName = current_thread().name
  processName = current_process().name

  print(f"{pid} * {processName} * {threadName} ---> Start counting...")
  while n > 0:
    n -= 1

  print(f"{pid} * {processName} * {threadName} ---> Finished counting...")

if __name__=="__main__":
  start = time.time()
  # multithreading helps with IO bound tasks
  t1 = Thread(target = io_bound, args = (SLEEP, ))
  t2 = Thread(target = io_bound, args = (SLEEP, ))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  end = time.time()
  print('IO bound: Time taken in seconds -', end - start)

  start = time.time()
  t1 = Thread(target = cpu_bound, args = (COUNT, ))
  t2 = Thread(target = cpu_bound, args = (COUNT, ))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  end = time.time()
  print('CPU bound: Time taken in seconds -', end - start)


