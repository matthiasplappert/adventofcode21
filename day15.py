import numpy as np
from collections import defaultdict
import heapq


def parse_line(l):
    return [int(x) for x in l.strip()]


def get_neighbors(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def filter_neighbor(coordinate, shape):
    x, y = coordinate
    if x < 0 or y < 0 or x >= shape[0] or y >= shape[1]:
        return False
    return True


with open("day15.txt", "r") as f:
    costs = np.array(list(map(parse_line, f.readlines())))


def dijkstra(costs, source, sink):
    dist = defaultdict(lambda: np.inf)
    dist[(0, 0)] = 0
    prev = {}

    # Dijkstra time.
    q = [(0, source)]
    visited = set([(0, 0)])
    while q and sink not in visited:
        _, (x, y) = heapq.heappop(q)
        neighors = list(filter(lambda n: filter_neighbor(n, costs.shape), get_neighbors(x, y)))
        for (x_, y_) in neighors:
            if (x_, y_) in visited:
                continue
            d_ = costs[x_, y_] + dist[x, y]
            if d_ < dist[(x_, y_)]:
                dist[(x_, y_)] = d_
                prev[(x_, y_)] = (x, y)
                heapq.heappush(q, (d_, (x_, y_)))
        visited.add((x, y))

    return dist[sink]

# Part 1
print(dijkstra(costs, (0, 0), (costs.shape[0] - 1, costs.shape[1] - 1)))

# Part 2
bias = np.array([
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 6],
    [3, 4, 5, 6, 7],
    [4, 5, 6, 7, 8],
])
costs_v2 = np.tile(costs, bias.shape)
bias = bias.repeat(costs.shape[0], axis=0).repeat(costs.shape[1], axis=1)
assert costs_v2.shape == bias.shape
costs_v2[:, :] = ((costs_v2[:, :] - 1 + bias) % 9 + 1)
print(dijkstra(costs_v2, (0, 0), (costs_v2.shape[0] - 1, costs_v2.shape[1] - 1)))
