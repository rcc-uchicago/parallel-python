#https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/

import time, os
from threading import Thread, current_thread
from multiprocessing import Process, current_process
import pandas as pd

# counting down from this number
COUNT = 100000000
# sleeping for this number of seconds
SLEEP = 5

def copy_file(src, dst):
  cmd = f"cp {src} {dst}"
  os.system(cmd)
  # Q: Is reading files from hard drive IO bound?
  #df = pd.read_csv(src)
  #print(df.to_string())

def io_bound(sec):

  pid = os.getpid()
  threadName = current_thread().name
  processName = current_process().name
  print(f"  {pid} * {processName} * {threadName} ---> Start IO...")

  # IO bound executations such as copying files, dowloading files
  # and executing system commands
  # sleep() is used to model IO bound tasks  
  #time.sleep(sec)
  copy_file("iris.csv", "iris2.csv")

  print(f"  {pid} * {processName} * {threadName} 	---> Finished IO...")

def cpu_bound(n):

  pid = os.getpid()
  threadName = current_thread().name
  processName = current_process().name

  print(f"  {pid} * {processName} * {threadName} ---> Start counting...")
  while n > 0:
    n -= 1

  print(f"  {pid} * {processName} * {threadName} ---> Finished counting...")

if __name__=="__main__":
  print("Single thread executions:")
  start = time.time()
  io_bound(SLEEP)
  io_bound(SLEEP)
  end = time.time()
  print('+ IO bound: Time taken in seconds -', end - start)

  start = time.time()
  cpu_bound(COUNT)
  cpu_bound(COUNT)
  end = time.time()
  print('+ CPU bound: Time taken in seconds -', end - start)

  print("\nMultithreaded executions:")
  start = time.time()
  # multithreading helps with IO bound tasks
  t1 = Thread(target = io_bound, args = (SLEEP, ))
  t2 = Thread(target = io_bound, args = (SLEEP, ))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  end = time.time()
  print('+ IO bound: Time taken in seconds -', end - start)

  start = time.time()
  t1 = Thread(target = cpu_bound, args = (COUNT, ))
  t2 = Thread(target = cpu_bound, args = (COUNT, ))
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  end = time.time()
  print('+ CPU bound: Time taken in seconds -', end - start)


