import os
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD

me = comm.Get_rank()
nprocs = comm.Get_size()

total_tasks = nprocs
n_samples_per_task = int(sys.argv[1])

if me == 0:
  print(f"number of samples per task = {n_samples_per_task}")
  print(f"total_tasks = {total_tasks}")

for i in range(n_samples_per_task):
  sample = me * n_samples_per_task + i
  cmd = f"echo {sample}"
  #os.system(cmd)
  if me == 1:
    print(cmd)

comm.Barrier()