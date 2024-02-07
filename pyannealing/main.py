from __future__ import annotations
import matplotlib.pyplot as plt

from pyannealing.classes.solver import Solver

def draw_map(title: str, points: list[tuple], point_indices: list[int]) -> None:
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
        
def solve(point_count: int = 20, map_size: int = 10, temp: int = 10000,
          temp_mult_factor: float = 0.98, max_iterations: int = 1000,
          min_temp: float = 0.5) -> Solver:
    solver = Solver(point_count, map_size, temp, temp_mult_factor)
    solver.solve(max_iterations, min_temp)
    return solver
    draw_map('Before', solver.points, solver.current_solution.point_indices)
    print(solver.current_solution.point_indices)
    print(solver.best_solution.point_indices)
    draw_map('Current', solver.points, solver.current_solution.point_indices)
    input('Ready')
    draw_map('Best', solver.points, solver.best_solution.point_indices)

def test():
    solver = Solver(5)
    solver.points = list(zip(range(5), [0]*5))
    solver.current_solution.reverse_segment(2, 3)
    print(solver.current_solution.point_indices)
    output = solver.current_solution.calculate_distance(solver.points)
    print(output)

if __name__ == '__main__':
    solve()