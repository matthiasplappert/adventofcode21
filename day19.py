from typing import Dict, Optional, Tuple, List
import numpy as np
from tqdm import tqdm
from collections import defaultdict
from dataclasses import dataclass
import heapq


MAX_UNITS = 1000


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
        # R^-1 = R^T for rotations. For the inverse, the affine part needs to be rotated as well.
        return Transformation(self.rotation.T, -self.rotation @ self.translation)


def apply_transformation_chain(chain, x):
    for transformation in chain:
        x = transformation(x)
    return x


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


def dijkstra(vertices: List[Tuple[int, int]], source: int) -> Dict[int, List[Tuple[int, int]]]:
    nodes = set(x for x, _ in vertices) | set(y for _, y in vertices)
    visited = set()
    q = [(0, source)]
    prev = {}
    while q:
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

    paths = {}
    for node in nodes:
        if node == source:
            path = [0, 0]
        else:
            path = [node]
            while path[-1] != source:
                path.append(prev[path[-1]])
            path.reverse()
        paths[node] = list(zip(path[:-1], path[1:]))
    return paths


def find_transformation(points1, points2, rotations) -> Optional[Transformation]:
    for rotation in rotations:
        # Rotate points2 into a different coordinate system, which is the candidate
        # rotation.
        points2_ = points2 @ rotation

        # Now check how far away each point in the translated points2_ is
        # from all other points in points1. If there are >=12 points with
        # the same offset, this is the missing translation.
        offset_counts = defaultdict(int)
        for point2_ in points2_:
            offsets = points1 - point2_[None, :]
            for offset in offsets:
                if np.max(np.abs(offset)) > 2 * MAX_UNITS:
                    # Too far away; both scanners could not have measured this point
                    # since their measurment regions don't overlap.
                    continue
                offset_counts[tuple(offset)] += 1
                if offset_counts[tuple(offset)] >= 12:
                    return Transformation(rotation, offset)

    return None


def get_num_matches(points, ref_points):
    num_matches = 0
    for point in points:
        num_matches += np.sum(np.all(point[None, :] == ref_points, axis=1))
    return num_matches


# Load data.
with open("day19.txt", "r") as f:
    all_points = list(map(parse_block, f.read().split("\n\n")))
num_scanners = len(all_points)

# TODO: the exercise says there are 24 rotations but this generates 48 (it was unclear
# to me if coordinate systems can mirror, so I included those). This part was stated in
# a very confusing way in the task description.
directions = [np.diag((x, y, z)) for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]]
permutations = get_permutations()
rotations = []
for direction in directions:
    rotations += (direction @ permutations).tolist()
rotations = np.array(rotations)

# Find all transformations between overlapping points. We will
# use those (forward and inverse) to then find a path from (0, scanner_idx).
# Once we have a path, we can concatenate all transformations to translate
# points into the same coordinate system. Also, include the identity transformation
# here for simplicity.
transformations: Dict[Tuple[int, int], Transformation] = {
    (0, 0): Transformation(np.eye(3), np.zeros(3))
}
for idx1 in tqdm(range(num_scanners - 1)):
    for idx2 in range(idx1 + 1, num_scanners):
        points1 = all_points[idx1]
        points2 = all_points[idx2]

        transformation = find_transformation(points1, points2, rotations)
        if transformation is None:
            continue
        # We keep botht the forward and inverse rotation because we need to find
        # a path from (0, scanner_idx) for scanner_idx in range(num_scanners). Some
        # of them will only be reachable via the inverse transformation.
        transformations[(idx2, idx1)] = transformation
        transformations[(idx1, idx2)] = transformation.inverse()

        # Sanity-check that transformations work as expected (forward and inverse).
        assert get_num_matches(transformations[(idx2, idx1)](points2), points1) >= 12
        assert get_num_matches(transformations[(idx1, idx2)](points1), points2) >= 12

# Find path between scanner 0 to all other scanners. We use this to construct a transformation
# chain that allows us to move from the coordinate of scanner_idx to the coordinate of scanner 0.
# (i.e. it applies it in reverse from scanner_idx -> 0).
transformation_chains = {}
paths = dijkstra(list(transformations.keys()), 0)
for scanner_idx in range(num_scanners):
    chain = []
    for (idx1, idx2) in reversed(paths[scanner_idx]):
         chain.append(transformations[idx2, idx1])
    transformation_chains[scanner_idx] = chain

# Transform all points into coordinate system wrt scanner 0.
unique_points = set()
for idx, points in enumerate(all_points):
    chain = transformation_chains[idx]
    points = apply_transformation_chain(chain, points)
    for point in points:
        unique_points.add(tuple(point))

# Part 1
print(len(unique_points))

# Part 2
locations = []
for idx in range(num_scanners):
    location = np.zeros(3)
    chain = transformation_chains[idx]
    location = apply_transformation_chain(chain, location)
    locations.append(location)
distances = []
for idx1 in range(num_scanners - 1):
    for idx2 in range(idx1, num_scanners):
        location1 = locations[idx1]
        location2 = locations[idx2]
        distances.append(np.abs(location1 - location2).sum())
print(int(np.max(distances)))
