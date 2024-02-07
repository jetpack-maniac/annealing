# Solver Module

# Python Modules
from random import randint, random
from math import e
from time import perf_counter

# Third-Party Modules
import numpy as np
from polars import DataFrame

# Local Modules
from pyannealing.classes.solution import Solution


class Solver:
    def __init__(self, point_count: int = 20, map_size: int = 10,
                 temp: int = 100000, temp_mult_factor: float = 0.98) -> None:
        self.point_count = point_count
        self.temp = temp
        self.temp_mult_factor = temp_mult_factor

        # Records
        self.perf_time = None
        self.history = None
        self.working_history = []


        self.points = np.zeros((point_count*2,), dtype=np.int64)
        point_indices = np.zeros((point_count,), dtype=np.int64)
        for i in range(point_count*2):
            self.points[i] = randint(0, map_size)
        for i in range(point_count):
            point_indices[i] = i

        self.points = self.points.reshape(-1, 2)

        self.current_solution = Solution(point_indices)
        self.current_solution.calculate_distance(self.points)
        self.worst_solution = self.current_solution
        self.best_solution = self.current_solution

    def solve(self, max_iterations: int = 1000, min_temp: float = 0.5,
              print_status: bool = False) -> None:
        total_iterations = 0
        max_iterations = max_iterations
        while self.temp > min_temp and total_iterations < max_iterations:
            self.solve_step(print_status)
            self.temp = self.temp * self.temp_mult_factor
            total_iterations += 1

        self.history = DataFrame(self.working_history)
        del self.working_history

    def solve_step(self, print_status: bool = False) -> None:
        moves_to_attempt = 100 * self.point_count
        max_changes = 10 * self.point_count
        change_count = 0
        
        for i in range(moves_to_attempt):
            index1 = randint(0, self.point_count-2)
            index2 = randint(index1+1, self.point_count)

            clone = self.current_solution.clone()
            start_time = perf_counter()
            clone.reverse_segment(index1, index2)
            new_dist = clone.calculate_distance(self.points)
            cost = new_dist - self.current_solution.dist
            clone.perf_time = perf_counter() - start_time

            if clone.dist > self.worst_solution.dist:
                self.worst_solution = clone

            if not self.should_replace(cost):
                continue
            self.current_solution = clone

            if clone.dist < self.best_solution.dist:
                self.best_solution = clone
            change_count = change_count + 1

            if change_count > max_changes:
                break

        self.working_history.append({
            'temperature': self.temp,
            'current distance': self.current_solution.dist,
            'best distance': self.best_solution.dist,
            'worst distance': self.worst_solution.dist,
            'change count': change_count,
        })

        if print_status:
            print(f'T: {self.temp:.5f} - Curr: {self.current_solution.dist:.3f} - Best: {self.best_solution.dist:.3f} - Worst: {self.worst_solution.dist:.3f} - Changes: {change_count}')

    def should_replace(self, cost: float) -> bool:
        if cost < 0:
            return True
        risk_power = e ** (-cost/self.temp)
        return risk_power > random()