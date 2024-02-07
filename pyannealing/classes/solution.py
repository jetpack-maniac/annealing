# Solver Module

# Python Modules
from copy import deepcopy

# Third-Party Modules
import numpy as np

class Solution:
    def __init__(self, point_indices: np.ndarray) -> None:
        self.point_indices = point_indices
        self.dist = None
        self.perf_time = None

    def calculate_distance(self, points: np.ndarray) -> float:
        reordered_points = points[self.point_indices]
        diffs = np.diff(reordered_points, axis=0, append=[reordered_points[0]])
        distances = np.sqrt((diffs ** 2).sum(axis=1))
        self.dist = distances.sum()
        return self.dist

    def clone(self) -> 'Solution':
        return deepcopy(self)
    
    def swap_points(self, point_index1: int, point_index2: int) -> None:
        point1 = self.point_indices[point_index1]
        point2 = self.point_indices[point_index2]
        self.point_indices[point_index2] = point1
        self.point_indices[point_index1] = point2

    def reverse_segment(self, starting_index: int, ending_index: int) -> None:
        starting_segment = self.point_indices[starting_index:ending_index+1]
        flipped_segment = starting_segment[::-1]
        self.point_indices[starting_index:ending_index+1] = flipped_segment