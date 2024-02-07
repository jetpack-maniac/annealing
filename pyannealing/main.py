from __future__ import annotations
from time import perf_counter

from pyannealing.classes.solver import Solver

def solve(point_count: int = 20, map_size: int = 10, temp: int = 10000,
          temp_mult_factor: float = 0.98, max_iterations: int = 1000,
          min_temp: float = 0.5) -> Solver:
    start_time = perf_counter()
    solver = Solver(point_count, map_size, temp, temp_mult_factor)
    solver.solve(max_iterations, min_temp)
    solver.perf_time = perf_counter() - start_time
    return solver

def test():
    solver = Solver(5)
    solver.points = list(zip(range(5), [0]*5))
    solver.current_solution.reverse_segment(2, 3)
    print(solver.current_solution.point_indices)
    output = solver.current_solution.calculate_distance(solver.points)
    print(output)

if __name__ == '__main__':
    solve()