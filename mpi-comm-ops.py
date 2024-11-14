# Demo: Point-to-point and collective communications with mpi4py
# mpirun -np 4 python mpi-comm-ops.py

from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

# non-blocking send, and receive
if rank == 0:
  data = {'a': 7, 'b': 3.14}
  comm.isend(data, dest=1, tag=11)
elif rank == 1:
  req = comm.irecv(source=0, tag=11)
  data = req.wait()
  print(data)

# blocking send and receive
if rank == 0:
  data = np.arange(1000, dtype='i')
  comm.Send([data, MPI.INT], dest=1, tag=88)
elif rank == 1:
  data = np.empty(1000, dtype='i')
  comm.Recv([data, MPI.INT], source=0, tag=88)

# Bcast
# allocate array properly on all procs
if rank == 0:
  data = np.arange(100, dtype='i')
else:
  data = np.empty(100, dtype='i')

comm.Bcast(data, root=0)
for i in range(100):
  assert data[i] == i

# Scatter
sendbuf = None
M = 10
if rank == 0:
  # root rank should have nprocs rows by M cols data
  sendbuf = np.empty([nprocs, M], dtype='f')
  sendbuf.T[:,:] = range(nprocs)

# all procs each have recv buf with M elements
recvbuf = np.empty(M, dtype='f')

comm.Scatter(sendbuf, recvbuf, root=0)
assert np.allclose(recvbuf, rank)
if rank == 2:
  print(recvbuf)

# Exercise: Gather (Google yourself) 

# Allreduce
local = np.array( [rank, rank+1])
all = np.zeros(2, 'int')

comm.Allreduce(local, all, op=MPI.SUM)
if rank == 2:
  print(all)



