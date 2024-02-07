from __future__ import annotations
import matplotlib.pyplot as plt

# Local
from pyannealing import Solver

from numpy import ndarray

# Jupyter
from IPython.display import clear_output

def draw_maps(solver: Solver):
    clear_output(wait=True)
    draw_map(f'Current: {solver.current_solution.dist}', solver.points, solver.current_solution.point_indices)
    draw_map(f'Best: {solver.best_solution.dist}', solver.points, solver.best_solution.point_indices)

def draw_map(title: str, points: ndarray, point_indices: ndarray) -> None:
    ordered_points = [points[i] for i in point_indices]
    x, y = zip(*ordered_points)
    x = x + (x[0],)
    y = y + (y[0],)

    plt.scatter(x, y, color='red', marker='o')
    plt.plot(x, y, color='blue', linestyle='-', linewidth=1)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(title)

    plt.show()