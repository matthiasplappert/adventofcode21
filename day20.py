import numpy as np
from tqdm import tqdm


def convert_char_to_int(char):
    assert char in ["#", "."]
    return int(char == "#")


def parse_rules(rules):
    assert len(rules) == 512
    return list(map(convert_char_to_int, rules))


def print_grid(grid):
    for row in grid:
        print("".join(["#" if x else "." for x in row]))


def get_area(x, y):
    return [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),

        (x, y - 1),
        (x, y),
        (x, y + 1),

        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]


def is_valid_coordinate(x, y, shape):
    if x < 0 or y < 0 or x >= shape[0] or y >= shape[1]:
        return False
    return True


def apply_rules(grid, rules, infinity_region):
    coordinates = [(x, y) for x in range(grid.shape[0]) for y in range(grid.shape[1])]
    new_grid = np.zeros(grid.shape, dtype=int)
    for x, y in coordinates:
        key = ""
        for (x_, y_) in get_area(x, y):
            if not is_valid_coordinate(x_, y_, grid.shape):
                key += str(infinity_region)
            else:
                key += str(grid[x_, y_])
        assert len(key) == 9
        idx = int(key, 2)
        new_grid[x, y] = rules[idx]

    idx = int(str(infinity_region) * 9, 2)
    new_infinity_region = rules[idx]

    return new_grid, new_infinity_region


# Get inputs.
with open("day20.txt", "r") as f:
    rules, grid = f.read().split("\n\n")
rules = parse_rules(rules)
grid = np.array([list(map(convert_char_to_int, l)) for l in grid.strip().splitlines()])
infinity_region = convert_char_to_int(".")

# Part 1
curr_grid = grid
curr_infinity_region = infinity_region
for _ in tqdm(range(2)):
    curr_grid = np.pad(curr_grid, 2, mode="constant", constant_values=curr_infinity_region)
    curr_grid, curr_infinity_region = apply_rules(curr_grid, rules, curr_infinity_region)
print(np.sum(curr_grid))

# Part 2
curr_grid = grid
curr_infinity_region = infinity_region
for _ in tqdm(range(50)):
    curr_grid = np.pad(curr_grid, 2, mode="constant", constant_values=curr_infinity_region)
    curr_grid, curr_infinity_region = apply_rules(curr_grid, rules, curr_infinity_region)
print(np.sum(curr_grid))
