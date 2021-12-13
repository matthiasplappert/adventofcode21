import numpy as np


def parse_point_line(l):
    x, y = l.strip().split(",")
    return int(x), int(y)


def count_unique_points(points):
    s = set()
    for x, y in points:
        s.add((x, y))
    return len(s)


def _fold(points, A, b, mask_idx):
    translated_points = points + b
    mask = (translated_points[:, :] > 0)[:, mask_idx][:, None]
    mirrored_points = (A @ translated_points.T).T - b
    combined_points = mask * mirrored_points + (1 - mask) * points
    return combined_points.astype(int)


def fold_vertically(points, x):
    b = np.array([-x, 0])
    A = np.eye(2)
    A[0, 0] = -1
    return _fold(points, A, b, 0)


def fold_horizontally(points, y):
    b = np.array([0, -y])
    A = np.eye(2)
    A[1, 1] = -1
    return _fold(points, A, b, 1)


def rasterize_points(points):
    xmax = int(np.max(points[:, 0], axis=0))
    ymax = int(np.max(points[:, 1], axis=0))
    grid = np.zeros((ymax + 1, xmax + 1), dtype=int)
    grid[points[:, 1], points[:, 0]] = 1
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            print("##" if grid[y, x] else "  ", end="")
        print()


with open("day13.txt") as f:
    points, instructions = f.read().split("\n\n")
points = np.array(list(map(parse_point_line, points.splitlines())))
print(points.shape)

for instruction in instructions.splitlines():
    lhs, rhs = instruction.strip().split(" ")[-1].split("=")
    if lhs == "y":
        points = fold_horizontally(points, int(rhs))
    elif lhs == "x":
        points = fold_vertically(points, int(rhs))
    else:
        raise ValueError("Unknown instruction: {}".format(instruction))
    print(count_unique_points(points))
rasterize_points(points)
