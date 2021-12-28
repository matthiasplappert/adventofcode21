from typing import Tuple, List
import numpy as np


def parse_range(r: str) -> Tuple[int, int]:
    r = r[2:]
    lhs, rhs = r.strip().split("..")
    return int(lhs), int(rhs) + 1


def parse_line(l: str) -> Tuple[bool, List[Tuple[int, int]]]:
    status, ranges = l.strip().split()
    assert status in ["on", "off"]
    return status == "on", list(map(parse_range, ranges.split(",")))


def normalize_range(r: Tuple[int, int], min, max) -> Tuple[int, int]:
    assert r[0] < r[1]
    r = np.clip(r, min, max)
    return (r[0] - min, r[1] - min)


with open("day22.txt", "r") as f:
    instructions = list(map(parse_line, f.readlines()))

state = np.zeros(shape=(101, 101, 101), dtype=bool)
for status, (xs, ys, zs) in instructions:
    xs = normalize_range(xs, -50, 50)
    ys = normalize_range(ys, -50, 50)
    zs = normalize_range(zs, -50, 50)
    state[xs[0]:xs[1], ys[0]:ys[1], zs[0]:zs[1]] = status
print(np.sum(state))
