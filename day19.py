import numpy as np
from tqdm import tqdm
from collections import defaultdict
from dataclasses import dataclass
import heapq


MAX_UNITS = 1000


def get_permutations():
    return np.array([
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
        ],

        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ],

        [
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
        ],
        [
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
        ],
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ],
    ])


def parse_block(block: str):
    assert block.startswith("--- scanner")
    return np.array([[int(x) for x in l.strip().split(",")] for l in block.splitlines()[1:]])


def dijkstra(vertices, source, sink):
    visited = set()
    q = [(0, source)]
    prev = {}
    while q and sink not in visited:
        d, v = heapq.heappop(q)
        if v in visited:
            continue
        visited.add(v)

        for (x_, y_) in vertices:
            if x_ != v:
                continue
            if y_ in visited:
                continue
            d_ = 1 + d
            prev[y_] = x_
            heapq.heappush(q, (d_, y_))

    path = [sink]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return list(zip(path[:-1], path[1:]))


@dataclass
class Transformation:
    rotation: np.ndarray
    translation: np.ndarray

    def __init__(self, rotation, translation):
        self.rotation = np.array(rotation)
        self.translation = np.array(translation)

    def __call__(self, x):
        return (x @ self.rotation) + self.translation

    def inverse(self):
        # R^-1 = R^T for transformations. For the inverse, the affine part needs to be rotated as well.
        return Transformation(self.rotation.T, -self.rotation @ self.translation)


# Load data.
with open("day19.txt", "r") as f:
    scanners = list(map(parse_block, f.read().split("\n\n")))

# TODO: the exercise says there are 24 rotations but I think there are 48?
directions = [np.diag((x, y, z)) for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]]
permutations = get_permutations()
rotations = []
for direction in directions:
    rotations += (direction @ permutations).tolist()
rotations = np.array(rotations)

# Find all transformations between overlapping points. We will
# use those (forward and inverse) to then find a path from (0, scanner_idx).
# Once we have a path, we can concatenate all transformations to translate
# points into the same coordinate system.
transformations = {}
for idx1 in tqdm(range(len(scanners) - 1)):
    for idx2 in range(idx1 + 1, len(scanners)):
        scanner1 = scanners[idx1]
        scanner2 = scanners[idx2]
        for rotation in rotations:
            translated_scanner2 = scanner2 @ rotation
            delta_counts = defaultdict(int)
            for row in translated_scanner2:
                deltas = scanner1 - row[None, :]
                for delta in deltas:
                    if np.max(np.abs(delta)) > 2 * MAX_UNITS:
                        continue
                    delta_counts[tuple(delta)] += 1
            for delta, count in delta_counts.items():
                if count >= 12:
                    transformation = Transformation(rotation, delta)
                    transformations[(idx1, idx2)] = transformation
                    transformations[(idx2, idx1)] = transformation.inverse()

                    # Sanity-check that transformations work as expected (forward and inverse).
                    num_matches = 0
                    for row in transformation(scanner2):
                        num_matches += np.sum(np.all(row[None, :] == scanner1, axis=1))
                    assert num_matches, f"forward failed {num_matches}"
                    num_matches = 0
                    for row in transformation.inverse()(scanner1):
                        num_matches += np.sum(np.all(row[None, :] == scanner2, axis=1))
                    assert num_matches, f"reverse failed {num_matches}"

# Transform all points into coordinate system wrt scanner 0.
points = set()
for idx, scanner in enumerate(scanners):
    if idx == 0:
        for row in scanner:
            points.add(tuple(row))
        continue

    path = dijkstra(transformations.keys(), 0, idx)
    assert path[0][0] == 0
    assert path[-1][1] == idx
    transformed_scanner = scanner
    for (idx1, idx2) in reversed(path):
        transformation = transformations[(idx1, idx2)]
        transformed_scanner = transformation(transformed_scanner)
    for row in transformed_scanner:
        points.add(tuple(row))

# Part 1
print(len(points))

# Part 2
locations = []
for idx in range(len(scanners)):
    path = dijkstra(transformations.keys(), 0, idx)
    location = np.zeros(3)
    for (x, y) in reversed(path):
        transformation = transformations[(x, y)]
        location = transformation(location)
    locations.append(location)

distances = []
for idx1 in range(len(scanners) - 1):
    for idx2 in range(idx1, len(scanners)):
        location1 = locations[idx1]
        location2 = locations[idx2]
        distances.append(np.abs(location1 - location2).sum())
print(int(np.max(distances)))
