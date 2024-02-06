from random import randint, random
from math import e

from pyannealing.classes.solution import Solution


class Solver:
    def __init__(self, point_count: int = 20, map_size: int = 10) -> None:
        self.point_count = point_count
        self.temp = 10000000
        self.temp_mult_factor = 0.98

        points, point_indices = [], []
        for i in range(point_count):
            points.append([randint(0, map_size), randint(0, map_size)])
            point_indices.append(i)

        self.points = points
        self.current_solution = Solution(point_indices)
        self.current_solution.calculate_distance(points)
        self.best_solution = self.current_solution

    def solve(self):
        total_iterations = 0
        max_iterations = 1000
        min_temp = 0.5
        while self.temp > min_temp and total_iterations < max_iterations:
            self.solve_step()
            self.temp = self.temp * self.temp_mult_factor
            total_iterations = total_iterations + 1

    def solve_step(self):
        moves_to_attempt = 1000 * self.point_count
        max_changes = 10 * self.point_count
        change_count = 0
        
        for i in range(moves_to_attempt):
            point_index1 = randint(0, self.point_count)
            point_index2 = randint(0, self.point_count)
            if point_index1 == point_index2:
                if point_index2 + 1 < self.point_count:
                    point_index2 = point_index2 + 1
                else:
                    point_index1 = point_index1 - 1
            if point_index1 > point_index2:
                point_index1, point_index2 = point_index2, point_index1

            clone = self.current_solution.clone()
            clone.reverse_segment(point_index1, point_index2)
            new_dist = clone.calculate_distance(self.points)
            dist = self.current_solution.dist
            cost = new_dist - dist
            if not self.should_replace(cost):
                continue
            self.current_solution = clone
            if clone.dist < self.best_solution.dist:
                self.best_solution = clone
                print(self.best_solution.point_indices)
            change_count = change_count + 1
            if change_count > max_changes:
                break
        print(f'Temp: {self.temp:.5f} - Current Distance: {self.current_solution.dist:.5f} - Best Distance: {self.best_solution.dist:.5f} - Changes: {change_count}')

    def should_replace(self, cost) -> bool:
        if cost < 0:
            return True
        risk_power = e ** (-cost/self.temp)
        anaylsis = (risk_power > random())
        return anaylsis