from __future__ import annotations
import matplotlib.pyplot as plt

# Local
from pyannealing import Solver, Solution

from numpy import ndarray

# Jupyter
from IPython.display import clear_output


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


def draw_solution_map(solution: Solution, solver: Solver, title: str) -> None:
    draw_map(f'{title}: {solution.dist}', solver.points, solution.point_indices)

def draw_maps(solver: Solver):
    clear_output(wait=True)
    draw_solution_map(solver.current_solution, solver, 'Current')
    draw_solution_map(solver.best_solution, solver, 'Best')
    draw_solution_map(solver.worst_solution, solver, 'Worst')