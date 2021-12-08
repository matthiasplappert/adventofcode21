import numpy as np


def cost_part1(ds):
    return np.sum(ds)


def cost_part2(ds):
    # \sum_{i=1}^n i = n(n+1)/2 (thanks kleiner Gauss!)
    return np.sum(ds * (ds + 1) / 2)


with open("day7.txt", "r") as f:
    xs = np.array(
        [int(x) for x in f.read().strip().split(",")]
    )
print(xs.shape)

xmin = xs.min()
xmax = xs.max()
costs = []
cost_fn = cost_part2  # use cost_part1 for part 1
for candidate_x in range(xmin, xmax + 1):
    ds = np.abs(xs - candidate_x)
    cost = cost_fn(ds)
    costs.append(cost)
print(int(np.min(costs)))
