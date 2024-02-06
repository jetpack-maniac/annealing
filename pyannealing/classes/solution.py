from copy import deepcopy
from math import sqrt

class Solution:
    def __init__(self, point_indices: list[int]) -> None:
        self.point_indices = point_indices
        self.dist = None

    def calculate_distance(self, points: list[tuple]) -> int:
        journey = 0
        ordered_points = [points[i] for i in self.point_indices]
        ordered_points.append(ordered_points[0])
        for i, point in enumerate(points):
            x1, y1 = point
            x2, y2 = ordered_points[(i+1) % len(ordered_points)]
            dist = sqrt(((x2-x1)**2 + (y2-y1)**2))
            journey = journey + dist
        self.dist = journey
        return journey
    
    def clone(self) -> 'Solution':
        return deepcopy(self)
    
    def swap_points(self, point_index1: int, point_index2: int) -> None:
        self.point_indices[point_index2] = self.point_indices[point_index1]
        self.point_indices[point_index1] = self.point_indices[point_index2]

    def reverse_segment(self, starting_index: int, ending_index: int) -> None:
        starting_segment = self.point_indices[starting_index:ending_index+1]
        flipped_segment = starting_segment[::-1]
        self.point_indices[starting_index:ending_index+1] = flipped_segment