
import numpy as np
from random import randint

point_count = 20
map_size = 10

new_points = np.zeros((point_count*2,), dtype=np.int64)
for i in range(point_count*2):
    new_points[i] = randint(0, map_size)

new_points = new_points.reshape(-1, 2)

for i, coords in enumerate(new_points):
    print(f'{i}: {coords}')