import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

x = list(range(100))
y = list(range(0, -100, -1))

fig, ax = plt.subplots()


def animate(i):
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(-100, 0)
    line, = ax.plot(x[0:i], y[0:i], color='blue', lw=1)
    point, = ax.plot(x[i], y[i], marker='.', color='blue')
    return line, point


animation = FuncAnimation(fig, animate, interval=40, blit=True, repeat=True, frames=100)
animation.save("test.gif", dpi=300, writer=PillowWriter(fps=25))
