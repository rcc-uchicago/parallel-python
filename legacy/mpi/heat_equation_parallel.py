import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from timeit import timeit
from mpi4py import MPI

comm = MPI.COMM_WORLD
mpi_rank = comm.Get_rank()
mpi_size = comm.Get_size()

# 1D grid to solve the heat equation on
N = 500 // mpi_size
x_width = 6.0/mpi_size
xmin = -3 + mpi_rank*x_width
xmax = xmin + x_width
x = np.linspace(xmin, xmax, N)
dx = x[1] - x[0]

# initial temperature (Gaussian)
initial = np.exp(-(x**2))

# Diffusion coefficient
D = 8

# time-step (chosen such that solution is stable)
dt = .5*dx**2/D

# solve heat equation
def update_python(T):
    """given T at timestep i, return T at timestep i+1"""
    T_next = np.copy(T)
    for i in range(1, N-1):
        T_next[i] = T[i] + D*dt/dx**2*(T[i+1] - 2*T[i] + T[i-1])

    return T_next

def update_numpy(T):
    """given T at timestep i, return T at timestep i+1"""
    T_next = np.copy(T)

    T_next[1:-1] = T[1:-1] + D*dt*(
        (T[2:] - 2*T[1:-1] + T[:-2])/dx**2 )

    ### We need to send and receive our left and right edges

    # send right edge and receive left edge
    if mpi_rank < mpi_size - 1:
        comm.send(T[-1], dest=mpi_rank+1)
    if mpi_rank > 0:
        T_left = comm.recv(source=mpi_rank-1)
        T_next[0] = T[0] + D*dt/dx**2*(T[1] - 2*T[0] + T_left)

    # send left edge and receive right edge
    if mpi_rank > 0:
        comm.send(T[0], dest=mpi_rank-1)
    if mpi_rank < mpi_size - 1:
        T_right = comm.recv(source=mpi_rank+1)
        T_next[-1] = T[-1] + D*dt/dx**2*(T[-2] - 2*T[-1] + T_right)

    return T_next

# solve heat equation over time (many timesteps)
states = []
state = np.copy(initial)
for i in range(10000):
    state = update_numpy(state)
    if i % 100 == 0:
        states.append(state)

# communicate back solution to rank 0
x = np.linspace(-3, 3, N*mpi_size)
all_states = []
for i in range(len(states)):
    T = None
    if mpi_rank == 0:
        T = np.empty(N*mpi_size, dtype=float)

    comm.Gather(states[i], T, root=0)

    if mpi_rank == 0:
        all_states.append(T)

# create an animation of the solution
if mpi_rank == 0:
    fig, ax = plt.subplots()
    plot = ax.plot(x, all_states[0], lw=2)[0]

    def update_plot(i):
        global plot
        plot.set_ydata(all_states[i])

    ax.set_ylim(0, 1)
    anim = animation.FuncAnimation(fig, update_plot, len(all_states), interval=30)

    for x_rank in np.linspace(-3, 3, mpi_size+1):
        plt.axvline(x_rank, color='red', alpha=.3)

    plt.show()
