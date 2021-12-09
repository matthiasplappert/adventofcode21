from collections import Counter
import numpy as np


def filter_coordinate(shape, coordinate):
    if coordinate[0] < 0 or coordinate[0] >= shape[0]:
        return False
    if coordinate[1] < 0 or coordinate[1] >= shape[1]:
        return False
    return True


def get_neighbors(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


# Load data.
with open("day9.txt", "r") as f:
    data = np.array([[int(x) for x in l.strip()] for l in f.readlines()])
print(data.shape)

# Part 1: Compute local minima.
coordinates = [
    (x, y) for x in range(data.shape[0]) for y in range(data.shape[1])
]
local_minima_map = np.zeros(data.shape, dtype=bool)
for x, y in coordinates:
    neighbors = get_neighbors(x, y)
    neighbors = np.array(list(filter(
        lambda x: filter_coordinate(data.shape, x), neighbors
    )))
    deltas = data[neighbors[:, 0], neighbors[:, 1]] - data[x, y]
    assert deltas.shape[0] == neighbors.shape[0]
    local_minima_map[x, y] = np.all(deltas > 0)

risk_levels = np.zeros_like(data)
risk_levels = local_minima_map * (data + 1)
print(risk_levels.sum())

# Part 2: Find basins.
num_minima = local_minima_map.sum()
basins = np.ones_like(data) * -1
queue = list(
    zip(
        zip(*np.where(local_minima_map)),
        range(num_minima)
    )
)
while queue:
    (x, y), basin_idx = queue.pop(0)
    if basins[x, y] != -1:
        continue
    if data[x, y] == 9:
        continue
    basins[x, y] = basin_idx
    neighbors = filter(
        lambda x: filter_coordinate(data.shape, x),
        get_neighbors(x, y)
    )
    queue += [[[x_, y_], basin_idx] for x_, y_ in neighbors]
counter = Counter(filter(lambda x: x >= 0, basins.flatten()))
print(np.prod(list(sorted(counter.values(), key=lambda x: -x))[:3]))
