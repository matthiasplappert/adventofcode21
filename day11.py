import numpy as np


def get_neighbors(x, y):
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x + 1, y + 1),
    ]


def is_valid_neighbor(shape, coordinate):
    if coordinate[0] < 0 or coordinate[0] >= shape[0]:
        return False
    if coordinate[1] < 0 or coordinate[1] >= shape[1]:
        return False
    return True


with open("day11.txt", "r") as f:
    grid = np.array([[int(c) for c in x.strip()] for x in f.readlines()])
print(grid.shape)

num_flashes_per_step = []
synced_steps = []
for step in range(1000):
    grid[:, :] += 1
    flash_mask = np.zeros(grid.shape, dtype=bool)

    def update_state():
        did_update = False
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] <= 9:
                    # Nothing do do here.
                    continue
                if flash_mask[x, y]:
                    continue
                neighbors = np.array(list(filter(
                    lambda x: is_valid_neighbor(grid.shape, x),
                    get_neighbors(x, y)
                )))
                flash_mask[x, y] = True
                grid[neighbors[:, 0], neighbors[:, 1]] += 1
                did_update = True
        return did_update

    did_update = update_state()
    while did_update:
        did_update = update_state()
    grid[grid > 9] = 0  # reset everybody that flashed
    num_flashes_per_step.append(np.sum(flash_mask))
    if np.all(flash_mask):
        synced_steps.append(step)

# Part 1
print(np.sum(num_flashes_per_step[:100]))

# Part 2
print(synced_steps[0] + 1)
