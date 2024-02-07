# Solver Module

# Python Modules
from random import randint, random
from math import e
from time import perf_counter_ns

# Third-Party Modules
from numpy import zeros, intc
from polars import DataFrame

# Local Modules
from pyannealing.classes.solution import Solution
from pyannealing.classes.general import Engine


class Solver:
    def __init__(self, point_count: int = 20, map_size: int = 10,
                 temp: float = 100000, temp_mult_factor: float = 0.98,
                 engine: Engine = Engine.PYTHON) -> None:
        self.engine = engine
        self.point_count = point_count
        self.temp = temp
        self.temp_mult_factor = temp_mult_factor
        self.map_size = map_size

        # Records
        self.perf_time: float = None
        self.history = [] # mutable list, will be converted to a DataFrame

        # Setting up the points
        self.points = zeros((point_count*2,), dtype=intc)
        point_indices = zeros((point_count,), dtype=intc)
        for i in range(point_count*2):
            self.points[i] = randint(0, map_size)
        for i in range(point_count):
            point_indices[i] = i

        self.points = self.points.reshape(-1, 2)

        # Initial solution preparation
        self.current_solution = Solution(point_indices)
        self.current_solution.calculate_distance(self.points)
        self.worst_solution = self.current_solution
        self.best_solution = self.current_solution

    def __repr__(self) -> str:
        map_str = f'{self.map_size}x{self.map_size}'
        return f'{self.engine.value} Solver: {self.point_count}P on {map_str}'
    
    @property
    def calculation_time(self) -> str:
        return f'{self.perf_time:.3f}'
        

    def solve(self, max_iterations: int = 1000, min_temp: float = 0.5) -> None:
        total_iterations = 0
        while self.temp > min_temp and total_iterations < max_iterations:
            self.solve_step()
            self.temp = self.temp * self.temp_mult_factor
            total_iterations += 1

        # Re-write history into a dataframe
        self.history = DataFrame(self.history)

    def solve_step(self) -> None:
        moves_to_attempt = 100 * self.point_count
        max_changes = 10 * self.point_count
        change_count = 0
        
        for _ in range(moves_to_attempt):
            index1 = randint(0, self.point_count-2)
            index2 = randint(index1+1, self.point_count)

            clone = self.current_solution.clone()
            start_time = perf_counter_ns()
            clone.reverse_segment(index1, index2)
            new_dist = clone.calculate_distance(self.points)
            cost = new_dist - self.current_solution.dist
            clone.perf_time_ns = perf_counter_ns() - start_time

            if clone.dist > self.worst_solution.dist:
                self.worst_solution = clone

            if not self.should_replace(cost):
                continue
            self.current_solution = clone

            if clone.dist < self.best_solution.dist:
                self.best_solution = clone
            change_count = change_count + 1

            if change_count == max_changes:
                break

        self.history.append({
            'temperature': self.temp,
            'current distance': self.current_solution.dist,
            'best distance': self.best_solution.dist,
            'worst distance': self.worst_solution.dist,
            'change count': change_count,
            'perf_time_ns': clone.perf_time_ns,
        })

    def should_replace(self, cost: float) -> bool:
        if cost < 0:
            return True
        risk_power = e ** (-cost/self.temp)
        return risk_power > random()