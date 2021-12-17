from typing import Tuple
from tqdm import tqdm
import numpy as np


def parse_input(s):
    lhs, rhs = s.strip().split(", ")
    lhs = lhs.split(": ")[1]
    assert lhs.startswith("x=")
    assert rhs.startswith("y=")

    xmin, xmax = [int(x) for x in lhs[2:].split("..")]
    ymin, ymax = [int(y) for y in rhs[2:].split("..")]
    assert xmin < xmax
    assert ymin < ymax
    return [[xmin, xmax], [ymin, ymax]]


class Trajectory:
    velocity: Tuple[int, int]
    position: Tuple[int, int]

    def __init__(self, velocity: Tuple[int, int]):
        self.velocity = velocity
        self.position = (0, 0)

    def step(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.velocity = (
            self.velocity[0] - 1 if self.velocity[0] > 0 else self.velocity[0] + 1 if self.velocity[0] < 0 else 0,
            self.velocity[1] - 1,
        )

    def can_still_hit_target(self, target_area):
        # Handle x-axis first.
        if self.velocity[0] > 0 and self.position[0] > target_area[0][1]:
            # We have positive x velocity and we are past the target x.
            return False
        if self.velocity[0] < 0 and self.position[0] < target_area[0][0]:
            # We have negative x velocity and we are past the target x.
            return False
        if self.velocity[0] == 0 and (self.position[0] < target_area[0][0] or self.position[0] > target_area[0][1]):
            # We have no x velocity and we are outside the target x.
            return False

        # Now handle y-axis.
        if self.velocity[1] >= 0:
            # We cannot decide yet as we still have positive velocity in y direction.
            return True
        assert self.velocity[1] < 0
        if self.position[1] < target_area[1][0]:
            # The y velocity is negative and we're out of the target area's y direction -> can't make it anymore
            return False
        return True

    def is_within_target(self, target_area):
        if self.position[0] < target_area[0][0] or self.position[0] > target_area[0][1]:
            return False
        if self.position[1] < target_area[1][0] or self.position[1] > target_area[1][1]:
            return False
        return True



with open("day17.txt", "r") as f:
    target_area = parse_input(f.read())


velocities = [(x, y) for x in range(0, 1000) for y in range(-1000, 1000)]
max_pos = []
successful_velocities = set()
for vel in tqdm(velocities):
    traj = Trajectory(vel)
    pos = []
    while traj.can_still_hit_target(target_area) and not traj.is_within_target(target_area):
        traj.step()
        pos.append(traj.position)
    if traj.is_within_target(target_area):
        max_pos.append(np.max(pos, axis=0)[1])
        successful_velocities.add(vel)

# Part 1
print(np.max(max_pos))

# Part 2
print(len(successful_velocities))
