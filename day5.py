import numpy as np


def parse_line(line):
    line = line.strip()
    lhs, rhs = line.split(" -> ")
    x, y = lhs.split(",")
    x_, y_ = rhs.split(",")
    return ((int(x), int(y)), (int(x_), int(y_)))


def normalize_line(line):
    lhs, rhs = line
    if np.any(rhs - lhs < 0):
        return rhs, lhs
    return lhs, rhs


# Parse data.
with open("day5.txt", "r") as f:
    data = np.array([parse_line(l) for l in f.readlines()])
    data = np.array([normalize_line(l) for l in data])
print(data.shape)

# Find maximum of coordinate system (origin is always (0, 0)).
maxx = max(np.max(data[:, 0, 0]), np.max(data[:, 1, 0]))
maxy = max(np.max(data[:, 0, 1]), np.max(data[:, 1, 1]))

# Create grid and count.
consider_diagonal = True  # set to False for first part
counts = np.zeros((maxx + 1, maxy + 1), dtype=np.int32)
for line in data:
    x, y = line[0]
    x_, y_ = line[1]
    is_diagonal = (x != x_ and y != y_)
    if is_diagonal:
        if not consider_diagonal:
            continue
        xd = x_ - x
        yd = y_ - y
        assert np.abs(xd) == np.abs(yd)
        num_steps = np.abs(xd) + 1
        diag = np.zeros((num_steps, num_steps), dtype=np.int32)
        np.fill_diagonal(diag, 1)
        minx = min(x, x_)
        maxx = max(x, x_)
        miny = min(y, y_)
        maxy = max(y, y_)
        if x < x_ and y < y_:
            pass
        elif x < x_ and y > y_:
            diag = diag[::-1, :]
        elif x > x_ and y < y_:
            diag = diag[:, ::-1]
        elif x > x_ and y > y_:
            diag = diag[::-1, ::-1]
        counts[minx:maxx + 1, miny:maxy + 1] += diag
    else:
        is_flipped = x > x_ or y > y_
        if is_flipped:
            x_, x = x, x_
            y_, y = y, y_
        assert x <= x_ and y <= y_
        counts[x:x_ + 1, y:y_ + 1] += 1

#print(counts.T)
print(np.sum(counts > 1))
