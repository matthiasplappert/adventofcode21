from enum import Enum
from typing import List
import numpy as np


class Type(Enum):
    EMPTY = 0
    DOWN = 1
    RIGHT = 2


def parse_line(l: str) -> List[int]:
    out = []
    for c in l.strip():
        if c == ".":
            out.append(Type.EMPTY.value)
        elif c == ">":
            out.append(Type.RIGHT.value)
        elif c == "v":
            out.append(Type.DOWN.value)
        else:
            raise ValueError(f"Unknown character {c}")
    return out


def print_grid(grid):
    for row in grid:
        for c in row:
            if c == Type.EMPTY.value:
                print(".", end="")
            elif c == Type.RIGHT.value:
                print(">", end="")
            elif c == Type.DOWN.value:
                print("v", end="")
        print()


def perform_moves(grid, offset, type):
    reset_coordinates = []
    move_to_coordinates = []
    for x, y in [(x, y) for x in range(grid.shape[0]) for y in range(grid.shape[1])]:
        if grid[x, y] != type.value:
            continue
        x_ = (x + offset[0]) % grid.shape[0]
        y_ = (y + offset[1]) % grid.shape[1]
        if grid[x_, y_] == Type.EMPTY.value:
            reset_coordinates.append((x, y))
            move_to_coordinates.append((x_, y_))
    assert len(reset_coordinates) == len(move_to_coordinates)
    if len(reset_coordinates) == 0:
        return False

    reset_coordinates = np.array(reset_coordinates)
    move_to_coordinates = np.array(move_to_coordinates)
    grid[reset_coordinates[:, 0], reset_coordinates[:, 1]] = Type.EMPTY.value
    grid[move_to_coordinates[:, 0], move_to_coordinates[:, 1]] = type.value
    return True


with open("day25.txt", "r") as f:
    grid = np.array(list(map(parse_line, f.readlines())))
print(grid.shape)

did_move = True
step = 0
while did_move:
    did_move1 = perform_moves(grid, (0, 1), Type.RIGHT)
    did_move2 = perform_moves(grid, (1, 0), Type.DOWN)
    did_move = did_move1 or did_move2
    step += 1
print(step)
