from mpi4py import MPI
import numpy as np
import sys

def calculate_pi(darts):
    """approximate pi by throwing darts at a board"""
    np.random.seed() # we need to set the random seed... see what happens if you comment this line out
    x = np.random.uniform(-1, 1, darts)
    y = np.random.uniform(-1, 1, darts)
    r_sq = x**2 + y**2
    return 4*np.sum(r_sq<1)/darts

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

# Allreduce
darts = 100000
mypi = calculate_pi(darts)
local = np.array( [mypi])
all = np.zeros(1, 'double')

comm.Allreduce(local, all, op=MPI.SUM)
if rank == 0:
  print(all/nprocs)



