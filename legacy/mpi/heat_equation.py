import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from timeit import timeit

# 1D grid to solve the heat equation on
N = 500
x = np.linspace(-3, 3, N)
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

    return T_next

# time solutions (1 timestep)
time = timeit(lambda: update_python(initial), number=100)/100*1e3
print(f'python update time: {time:.3f} ms')
time = timeit(lambda: update_numpy(initial), number=100)/100*1e3
print(f'numpy update time: {time:.3f} ms')

# solve heat equation over time (many timesteps)
states = []
state = np.copy(initial)
for i in range(10000):
    state = update_numpy(state)
    if i % 100 == 0:
        states.append(state)

# create an animation of the solution
fig, ax = plt.subplots()
plot = ax.plot(x, initial, lw=2)[0]

def update_plot(i):
    global plot
    plot.set_ydata(states[i])

ax.set_ylim(0, 1)
anim = animation.FuncAnimation(fig, update_plot, len(states), interval=30)

plt.show()
